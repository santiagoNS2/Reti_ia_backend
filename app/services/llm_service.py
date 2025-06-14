import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
MODEL_NAME = "mistral"  # Puedes cambiar a mistral o el que cargaste

def ask_ollama(prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
    )
    response.raise_for_status()

    data = response.json()
    return data.get("response", "")

def get_summary_and_entities(text: str) -> dict:
    summary_prompt = f"Resume el siguiente texto:\n\n{text}"
    entities_prompt = f"Extrae las entidades clave (personas, organizaciones, lugares, fechas) del siguiente texto:\n\n{text}"

    summary = ask_ollama(summary_prompt)
    entities = ask_ollama(entities_prompt)

    return {
        "summary": summary.strip(),
        "entities": entities.strip()
    }