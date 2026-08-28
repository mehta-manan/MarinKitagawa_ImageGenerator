WORKFLOW_PATH = "templates/txt2image_Lora_MK_API.json"
IMAGE_OUTPUT_NODE_INDEX = 9

IMAGE_GENERATION_WAIT_TIME = 150  # seconds
POLLING_INTERVAL = 5  # seconds
MAX_POLLING_ATTEMPTS = 60
IMAGE_GENERATION_RELAX_TIME = 2 # seconds

SEED = {"NODE_INDEX": "3", "VALUE": "seed"}
TEXT = {"NODE_INDEX": "6", "VALUE": "text"}

MK_LORA_TRIGGER_WORDS = "marin_kitagawa1, marin1, kitagawa1, Marin Kitagawa"
DEFAULT_PROMPT = "best quality, masterpiece, 1girl, solo, looking at viewer, long hair, blush, smile, upper body, detailed background, outdoors, sunlight"

DEFAULT_TYPE = 'http'
SUPPORTED_TYPES = set([DEFAULT_TYPE, 'ws'])

SEED_MIN = 0
SEED_MAX = 999999999999999