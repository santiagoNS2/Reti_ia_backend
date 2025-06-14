from pathlib import Path
from typing import List
from pdf2image import convert_from_path

def is_pdf(file_path: str) -> bool:
    return Path(file_path).suffix.lower() == ".pdf"

def convert_pdf_to_images(pdf_path: str, output_folder: str) -> List[str]:
    pages = convert_from_path(pdf_path)
    image_paths = []
    for i, page in enumerate(pages):
        image_path = f"../archivos/page{i}.png"
        page.save(image_path, "PNG")
        image_paths.append(image_path)
    return image_paths