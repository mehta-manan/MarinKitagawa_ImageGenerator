import os
import json
import asyncio
import websockets

import logging
logger = logging.getLogger(__name__)

from constants.comfyui import IMAGE_OUTPUT_NODE_INDEX, IMAGE_GENERATION_RELAX_TIME
from clients.comfyui_base import ComfyUIBaseClient

class _ComfyUIWSClient(ComfyUIBaseClient):
    def __init__(self):
        super().__init__()
        self._ws = os.getenv('WS')
        self._uri = f"{self._ws}://{self._server_address}/ws"
    
    def _is_execution_done(self, message, prompt_id):
        if message.get("type") != "progress_state":
            return False

        data = message.get("data", {})

        if data.get("prompt_id") != prompt_id:
            return False

        node = data.get("nodes", {}).get(str(IMAGE_OUTPUT_NODE_INDEX))

        return node is not None and node.get("state") == "finished"
    
    async def _wait_until_done(self, prompt_id, client_id):
        async with websockets.connect(f"{self._uri}?client_id={client_id}") as ws:
            while True:
                message = json.loads(await ws.recv())

                if self._is_execution_done(message, prompt_id):
                    #  prevent the race between WebSocket completion and /history becoming available.
                    logger.info(f"Waiting for history to be available for prompt_id: {prompt_id}")
                    await asyncio.sleep(IMAGE_GENERATION_RELAX_TIME)
                    break
    
    async def _generate_image(self, prompt_id, client_id=None):
        logger.info(f"Waiting for image to be generated with prompt_id: {prompt_id}, client_id: {client_id}")
        await self._wait_until_done(prompt_id, client_id)
        logger.info(f"Image is ready for prompt_id: {prompt_id}, client_id: {client_id}")
        
        image = self._retrieve_image(prompt_id)
        return image
            
comfyui_ws_client = _ComfyUIWSClient()
