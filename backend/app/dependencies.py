"""ML model singletons. Loaded once at startup, shared by seeding and inference."""
import base64
import io
import logging
import threading

import numpy as np
from PIL import Image

from app.config import settings

log = logging.getLogger(__name__)

_lock = threading.Lock()
_device: str | None = None
_embedder = None
_clip_model = None
_clip_processor = None


def device() -> str:
    global _device
    if _device is None:
        import torch

        want = settings.embedding_device
        if want.startswith("cuda") and not torch.cuda.is_available():
            log.warning("EMBEDDING_DEVICE=%s but CUDA is unavailable; using CPU", want)
            want = "cpu"
        _device = want
    return _device


def load_models() -> None:
    global _embedder, _clip_model, _clip_processor
    with _lock:
        if _embedder is None:
            from sentence_transformers import SentenceTransformer

            _embedder = SentenceTransformer(settings.text_model, device=device())
        if _clip_model is None:
            from transformers import CLIPModel, CLIPProcessor

            _clip_model = CLIPModel.from_pretrained(settings.clip_model).to(device()).eval()
            _clip_processor = CLIPProcessor.from_pretrained(settings.clip_model)
    log.info("Models loaded on %s", device())


def embed_texts(texts: list[str], batch_size: int = 128) -> np.ndarray:
    """L2-normalised 384-dim MiniLM embeddings."""
    load_models()
    return _embedder.encode(
        texts, batch_size=batch_size, normalize_embeddings=True, show_progress_bar=False
    )


def embed_text(text: str) -> np.ndarray:
    return embed_texts([text])[0]


def embed_images(images: list[Image.Image], batch_size: int = 64) -> np.ndarray:
    """L2-normalised 512-dim CLIP image embeddings."""
    import torch

    load_models()
    out = []
    for i in range(0, len(images), batch_size):
        batch = images[i : i + batch_size]
        inputs = _clip_processor(images=batch, return_tensors="pt").to(device())
        with torch.no_grad():
            feats = _clip_model.get_image_features(**inputs)
        feats = feats / feats.norm(dim=-1, keepdim=True)
        out.append(feats.cpu().numpy())
    return np.concatenate(out) if out else np.zeros((0, 512), dtype=np.float32)


def svg_to_image(svg: str | bytes, size: int = 224) -> Image.Image:
    import cairosvg

    data = svg.encode() if isinstance(svg, str) else svg
    png = cairosvg.svg2png(bytestring=data, output_width=size, output_height=size, background_color="white")
    return Image.open(io.BytesIO(png)).convert("RGB")


def decode_logo(b64: str) -> Image.Image:
    """Decode a base64 (or data URL) PNG/JPG/SVG upload into an RGB PIL image."""
    mime = ""
    if b64.startswith("data:"):
        header, b64 = b64.split(",", 1)
        mime = header[5:].split(";")[0]
    raw = base64.b64decode(b64)
    head = raw[:512].lstrip().lower()
    if mime == "image/svg+xml" or head.startswith(b"<svg") or (head.startswith(b"<?xml") and b"<svg" in raw[:2048].lower()):
        return svg_to_image(raw)
    img = Image.open(io.BytesIO(raw))
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(bg, img)
    return img.convert("RGB")
