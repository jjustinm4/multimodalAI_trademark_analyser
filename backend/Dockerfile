FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# libcairo2 + fonts: needed by cairosvg to render SVG logos for CLIP
RUN apt-get update && apt-get install -y python3.11 python3-pip libcairo2 fonts-dejavu-core && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# WordNet for the descriptiveness check (baked in so first boot needs no download)
RUN python3 -m nltk.downloader -d /usr/share/nltk_data wordnet omw-1.4

COPY . .

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
