import logging

from fastapi import FastAPI

from routers import auth, tag, image, user

logging.basicConfig(
	level=logging.DEBUG,
	format="%(asctime)s - %(levelname)s - %(message)s",
	datefmt="%Y-%m-%d %H:%M"
)

# Set the logging level for pymongo and boto3 to WARNING to reduce verbosity
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("boto3").setLevel(logging.WARNING)
logging.getLogger("botocore").setLevel(logging.WARNING)
logging.getLogger("s3transfer").setLevel(logging.WARNING)

app = FastAPI()

app.include_router(tag.router, prefix="/api/v2/tags", tags=["tags"])
app.include_router(image.router, prefix="/api/v2/images", tags=["images"])
app.include_router(auth.router, prefix="/api/v2/auth", tags=["auth"])
app.include_router(user.router, prefix="/api/v2/user", tags=["user"])

@app.get("/")
async def root():
	return {"message" : "Hello from Marin Kitagawa Image Generator Server (FastAPI)!"}