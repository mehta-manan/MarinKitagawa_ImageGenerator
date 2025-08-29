import json
import base64
import sys
import time
from urllib import request
import os
from dotenv import load_dotenv
import random

load_dotenv()
COMFY_HOST = os.getenv("COMFY_HOST")

workflow = "./ComfyUI/API_workflow/txt2image_Lora_MK_API.json"

with open(workflow, "r", encoding="utf-8") as f:
    workflow = json.load(f)

def log(msg):
    print(f"[DEBUG] {msg}", file=sys.stderr, flush=True)

def queue_prompt(prompt):
    data = json.dumps({"prompt": prompt}).encode('utf-8')
    req = request.Request(f"{COMFY_HOST}/prompt", data=data)
    with request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get_history(prompt_id):
    with request.urlopen(f"{COMFY_HOST}/history/{prompt_id}") as resp:
        return json.loads(resp.read().decode())

def get_image(file):
    url = f"{COMFY_HOST}/view?filename={file['filename']}&subfolder={file['subfolder']}&type={file['type']}"
    log(f"Fetching image from {url}")
    with request.urlopen(url) as resp:
        return resp.read()

if __name__ == "__main__":
    prompt_text = sys.argv[1] if len(sys.argv) > 1 else ""
    log(f"Prompt text: {prompt_text}")
    workflow["6"]["inputs"]["text"] = prompt_text
    workflow["3"]["inputs"]["seed"] = random.randint(0, 999999999999999)

    try:
        result = queue_prompt(workflow)
        prompt_id = result["prompt_id"]
        log(f"Queued prompt_id: {prompt_id}")
    except Exception as e:
        log(f"Queue prompt failed: {e}")
        print(json.dumps({"error": f"queue_failed: {str(e)}"}), flush=True)
        sys.exit(1)

    # wait for comfy to finish
    log("Sleeping 150 seconds to allow ComfyUI to generate images...")
    time.sleep(150)
    max_extra_checks = 60
    outputs = None

    for i in range(max_extra_checks):
        log(f"Polling history (attempt {i+1}/{max_extra_checks})...")
        history = get_history(prompt_id)
        if prompt_id in history and "outputs" in history[prompt_id]:
            outputs = history[prompt_id]["outputs"]
            log("Found outputs in history")
            break
        time.sleep(4)

    if not outputs:
        log("Timeout: No outputs after polling")
        print(json.dumps({"error": "timeout"}), flush=True)
        sys.exit(1)

    for node_id in outputs:
        log(f"Checking node_id {node_id}")
        if "images" in outputs[node_id]:
            log(f"Found images in node {node_id}")
            file = outputs[node_id]["images"][0]
            log(f"Image file info: {file}")
            img_bytes = get_image(file)
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")
            print(json.dumps({"image": img_b64}), flush=True)   # ✅ always output JSON
            sys.exit(0)

    log("No image found in outputs")
    print(json.dumps({"error": "no_image"}), flush=True)
    sys.exit(1)
