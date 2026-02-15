import shutil

from fastapi import APIRouter, UploadFile

from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Images"])


@router.post("images")
async def upload_image(image: UploadFile):
    image_path = f"src/static/images/{image.filename}"
    with open(image_path, "wb+") as file:
        shutil.copyfileobj(image.file, file)

    resize_image.delay(image_path)
