from fastapi import APIRouter, UploadFile, File
import os
import shutil
from datetime import datetime

from utils.file_utils import is_pdf, convert_pdf_to_images
from services.ocr_service import extract_text_from_image
from services.llm_service import get_summary_and_entities

router = APIRouter()

UPLOAD_DIR = "archivos/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Guarda temporalmente el archivo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = ""

    if is_pdf(file_path):
        images = convert_pdf_to_images(file_path, UPLOAD_DIR)
        for image_path in images:
            extracted_text += extract_text_from_image(image_path) + "\n"
    else:
        extracted_text = extract_text_from_image(file_path)

    llm_result = get_summary_and_entities(extracted_text)

    return {
        "filename": file.filename,
        "timestamp": datetime.now().isoformat(),
        "text": extracted_text.strip(),
        "summary": llm_result["summary"],
        "entities": llm_result["entities"]
    }
