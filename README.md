# Trademark Examination PoC

A laptop-runnable proof of concept of a trademark examiner console: conflict search
(phonetic, semantic, visual, goods), weighted fusion, Nice classification, absolute grounds
screening, precedent retrieval, and an LLM-drafted examination report.

Everything runs on synthetic data generated at first boot. Nothing is trained; every matcher
uses a pretrained model or a deterministic algorithm. Not production code: no auth, no rate limiting.

## Run

```bash
# Terminal 1: start llama-server on the host (port 8080)
llm

# Terminal 2: start the stack
cd ~/development/agentic_trademark_analyser
docker compose up --build
```

First boot takes 5–10 minutes (image build, model download, seeding 5,000 marks + embeddings).
Watch for `Backend ready — models loaded, 5000 marks indexed`, then open http://localhost:3000.

Later boots skip seeding and start in about 30 seconds. To reseed from scratch:
`docker compose down -v && docker compose up --build`.

If llama-server is not running, everything works except the report, which falls back to a
template with a yellow banner. `GET /api/health` reports `llm: unreachable`.

## Requirements

- Docker + docker compose, NVIDIA Container Toolkit (for GPU embeddings)
- llama-server serving `gpt-oss-20b` on host port 8080
- 16 GB RAM

**Small GPUs:** MiniLM + CLIP need about 1 GB of VRAM. If llama-server already fills the GPU,
set `EMBEDDING_DEVICE: cpu` in `docker-compose.yml`. Seeding then takes a few minutes longer;
queries stay fast. The backend also falls back to CPU automatically when CUDA is unavailable.

## Services

| Service | Port | Role |
| --- | --- | --- |
| frontend (nginx) | 3000 | Examiner console; proxies `/api/*` to the backend |
| backend (FastAPI) | 8000 | API, matchers, embeddings, LLM calls. Docs at http://localhost:8000/docs |
| postgres (pgvector) | 5432 | Marks, HNSW vector indexes, precedent chunks, Nice reference entries |
| llama-server (host) | 8080 | Report drafting via the OpenAI-compatible API |

## API

| Method | Path | Purpose |
| --- | --- | --- |
| POST | `/api/analyze` | Full pipeline. Body: `{mark_text, goods_description, nice_class?, logo_file?}` (`logo_file` is base64 or a data URL; PNG, JPG or SVG) |
| GET | `/api/search?q=zentara` | Quick phonetic + semantic search |
| POST | `/api/classify` | `{goods_description}` → top-3 Nice classes |
| GET | `/api/marks` | Paginated corpus. Params: `page`, `page_size`, `q`, `nice_class`, `status`, `has_logo`, `sort`, `order` |
| GET | `/api/marks/{id}` | One mark |
| GET | `/api/health` | `{status, llm, db}` |

## Tuning fusion weights

Set `FUSION_W_PHONETIC`, `FUSION_W_SEMANTIC`, `FUSION_W_VISUAL`, `FUSION_W_GOODS` in
`docker-compose.yml` and restart the backend. With no logo, the visual weight is redistributed
proportionally (defaults become 0.375 / 0.375 / 0.25).

## Development

```bash
# Backend tests (no database needed)
cd backend && python -m pytest tests -q
RUN_MODEL_TESTS=1 python -m pytest tests -q   # also loads MiniLM + CLIP

# Frontend dev server with hot reload (proxies /api to localhost:8000)
cd frontend && npm install && npm run dev
```

## Implementation notes

- **Double Metaphone** comes from the `metaphone` package; `jellyfish` has Soundex but not Double Metaphone.
- **SVG rendering** for CLIP uses `cairosvg`, so the backend image installs `libcairo2` and DejaVu fonts.
- **WordNet** data is downloaded into the backend image at build time.
- **Startup** (wait for DB → Alembic migrations → seed if empty → load models) runs in the FastAPI
  lifespan, so the Dockerfile `CMD` stays a plain uvicorn launch.
- **Results** are kept in the browser's sessionStorage, keyed by the `/results/:id` route.
- **Prohibited-term matching** requires short acronyms (FBI, CIA, NASA) to match a whole word,
  so coined marks like "Ciatek" are not flagged for "CIA".
