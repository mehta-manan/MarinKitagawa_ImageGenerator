import asyncio

import logging
logger = logging.getLogger(__name__)

from constants.comfyui import IMAGE_GENERATION_WAIT_TIME, POLLING_INTERVAL, MAX_POLLING_ATTEMPTS
from clients.comfyui_base import ComfyUIBaseClient

class _ComfyUIHTTPClient(ComfyUIBaseClient):
    def __init__(self):
        super().__init__()

    async def _poll_image(self, prompt_id):
        logger.info(f"Waiting for {IMAGE_GENERATION_WAIT_TIME} seconds before starting to poll for outputs.")
        await asyncio.sleep(IMAGE_GENERATION_WAIT_TIME)
        
        logger.info(f"Starting to poll for image generation with prompt_id: {prompt_id}")
        
        for attempt in range(MAX_POLLING_ATTEMPTS):
            logger.info(f"Polling attempt {attempt + 1}/{MAX_POLLING_ATTEMPTS} for prompt_id: {prompt_id}")
            
            image = self._retrieve_image(prompt_id)
            if image:
                return image
            
            logger.warning(f"No outputs found for prompt_id: {prompt_id}. Waiting for {POLLING_INTERVAL} seconds before next polling attempt.")
            await asyncio.sleep(POLLING_INTERVAL)
            
        logger.error(f"Timeout reached for prompt_id: {prompt_id}. No outputs found after {MAX_POLLING_ATTEMPTS} attempts.")
        return None
    
    async def _generate_image(self, prompt_id, client_id=None):
        image = await self._poll_image(prompt_id)
        return image

comfyui_http_client = _ComfyUIHTTPClient()