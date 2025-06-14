# Reto Backend – OCR + IA (FastAPI + Mistral "ollama")

**Autor: Santiago Naranjo Sanchez**

Este repositorio resuelve el desafío técnico de construir una API capaz de:

1. **Procesar documentos PDF e imágenes** mediante OCR (Tesseract).
2. **Generar un resumen** y **extraer entidades clave** usando un modelo LLM local (Mistral vía Ollama).
3. Mantener un **historial** de documentos procesados y exponerlo vía API.
4. Servir un **frontend mínimo** para subir archivos y visualizar resultados.

---

## 🌐 Demo rápida

| Recurso               | URL por defecto                                          | Qué verás                                                     |
| --------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| Frontend              | [http://localhost:8000](http://localhost:8000)           | Formulario para subir PDF/imagen y la tabla *Historial*.      |
| Documentación Swagger | [http://localhost:8000/docs](http://localhost:8000/docs) | Prueba los endpoints `POST /api/upload` y `GET /api/history`. |

---

## 📂 Estructura del proyecto

```
Reto_backend_IA/
├── app/                # Código FastAPI
│   ├── api/            # Rutas (endpoints)
|   |── frontend        # index.html, assets
│   ├── services/       # OCR y LLM helper functions
│   └── main.py         # Instancia FastAPI + montaje frontend          
├── archivos/           # PDFs, imágenes subidas y history.json
├── Dockerfile          # Imagen de la API + Tesseract
├── docker-compose.yml  # Levanta API + Ollama
└── requirements.txt    # Dependencias Python
```

> **Nota**: el OCR guarda los PDFs y las imágenes tal cual se reciben en `archivos/uploads/`; el archivo `archivos/history.json` almacena el texto extraído, el resumen y las entidades de cada documento.

---

## 🚀 Puesta en marcha

### 1. Clonar el proyecto

```bash
git clone https://github.com/santiagoNS2/Reto_Backend-IA_savant.git
cd Reto_Backend-IA_savant
```

### 2. Ejecución más sencilla: **Docker Compose**

```bash
docker compose up --build
```

Esto construye la imagen de la API y arranca dos contenedores:

| Servicio | Imagen          | Puerto   | Descripción                                  |
| -------- | --------------- | -------- | -------------------------------------------- |
| `web`    | reto-backend-ia | **8000** | FastAPI + Frontend                           |
| `ollama` | ollama/ollama   | 11434    | Servidor Ollama cargando el modelo *Mistral* |

> La primera vez, `ollama` ejecuta `ollama pull mistral`, puede tardar unos minutos.

### 3. Ejecución manual (sin Compose)

1. **Ollama**

   ```bash
   # Terminal A
   ollama serve &
   ollama pull mistral   # descarga el modelo (~4 GB)
   ```
2. **API**

   ```bash
   # Terminal B
   docker build -t reto-backend-ia .
   docker run -p 8000:8000 \
     -e OLLAMA_URL=http://host.docker.internal:11434 \
     reto-backend-ia
   ```

(Usa `host.docker.internal` para que el contenedor vea el host donde corre Ollama.)

---

## 🖥️ Uso del Frontend

1. Abre [http://localhost:8000](http://localhost:8000).
2. Haz clic en **“Elegir archivo”** y selecciona un PDF o imagen.
3. Pulsa **“Subir y Procesar”**.
4. La sección **Resultado Reciente** muestra el resumen y las entidades del archivo.
5. Más abajo, **Historial** lista todos los documentos procesados (nombre, fecha, resumen y entidades).

---

## 🔧 Cambiar de modelo LLM

Si dispones de más recursos y quieres usar otro modelo acelerado GPU o más grande:

1. Descarga el modelo con `ollama pull <modelo>` (ej. `llama3`).
2. Edita \`\` → línea 5:

   ```python
   MODEL_NAME = "llama3"  # antes: "mistral"
   ```
3. Reconstruye la imagen y vuelve a levantar los contenedores.

---

## ⚙️ Requisitos para ejecución local (sin Docker)

| Tipo          | Versión mínima                                           |
| ------------- | -------------------------------------------------------- |
| Python        |  3.11                                                    |
| Tesseract OCR |  5.x + paquetes `tesseract-ocr-spa`, `tesseract-ocr-eng` |
| Poppler       | Para `pdf2image`                                         |
| Ollama        | ≥ 0.1.34                                                 |

Instala dependencias Python:

```bash
pip install -r requirements.txt
```

Arranca Ollama y luego `uvicorn app.main:app --reload` para desarrollo.

---

## 🔮 ¿Qué usaría en producción y por qué?

> **Pregunta del reto:** “*Documenta claramente qué usarías en producción (ej. OpenAI, Gemini, etc.)*”.

| Opción                                       | Ventajas clave                                                                                                                                                          | Desventajas                                                                                                       |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **OpenAI GPT‑4o**                            | Precisión SOTA en comprensión+razonamiento; funciones de "tool calling"; latencia global baja (regiones múltiples); ecosistema maduro (embeddings, moderation, vision). | Código cerrado; exige enviar datos fuera de la org; precio superior a modelos open‑source si la escala es grande. |
| **Google Gemini 1.5 Pro**                    | Context window masivo (1 M tokens); buen *multimodal*; integración nativa con Google Cloud.                                                                             | Aún en beta en algunos países; ecosistema de plugins más pequeño.                                                 |
| **DeepSeek‑V2 67B**                          | Modelo open‑source mixto (inglés‑chino) con excelente rendimiento en benchmarks; licencia Apache 2; menor tamaño que Llama‑3 70B ⇒ +rápido y menos RAM.                 | Comunidad aún pequeña; soporte multilingüe (ES) más limitado; requiere operar infraestructura GPU propia.         |
| **Open‑source (Llama‑3 70B, Mixtral 8x22B)** | Datos on‑prem; personalización vía LoRA; coste variable ≈ 0 una vez desplegado.                                                                                         | Requiere operar infraestructura GPU y MLOps; menor desempeño en tareas complejas que GPT‑4o.                      |

**Si el precio no es limitante**, elegiría **GPT‑4o** para la versión de producción porque entrega:

1. **Máxima precisión** en generación de resúmenes y NER sin finos ajustes.
2. **Latencia global** con redundancia (Azure OpenAI + OpenAI).
3. **Mantenimiento casi nulo** (no hay que actualizar pesos ni escalar clusters GPU).

Para escenarios **on‑prem** o con datos altamente sensibles, migraría a **Llama‑3 70B** o **DeepSeek‑V2 67B** desplegados en Kubernetes con vLLM.

\--------|----------------|-------------|
\| **OpenAI GPT‑4o** | Precisión SOTA en comprensión+razonamiento; funciones de "tool calling"; latencia global baja (regiones múltiples); ecosistema maduro (embeddings, moderation, vision). | Código cerrado; exige enviar datos fuera de la org; precio superior a modelos open‑source si la escala es grande. |
\| **Google Gemini 1.5 Pro** | Context window masivo (1 M tokens); buen *multimodal*; integración nativa con Google Cloud. | Aún en beta en algunos países; ecosistema de plugins más pequeño. |
\| **Open‑source (Llama‑3 70B, Mixtral 8x22B)** | Datos on‑prem; personalización vía LoRA; coste variable ≈ 0 una vez desplegado. | Requiere operar infraestructura GPU y MLOps; menor desempeño en tareas complejas que GPT‑4o. |

**Si el precio no es limitante**, elegiría **GPT‑4o** para la versión de producción porque entrega:

1. **Máxima precisión** en generación de resúmenes y NER sin finos ajustes.
2. **Latencia global** con redundancia (Azure OpenAI + OpenAI).
3. **Mantenimiento casi nulo** (no hay que actualizar pesos ni escalar clusters GPU).

Para escenarios **on‑prem** o con datos altamente sensibles, migraría a **Llama‑3 70B** desplegado en Kubernetes con vLLM.

---




