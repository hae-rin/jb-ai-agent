from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.routes import care_agent, simulation, doc_reader, products, bucket_list, voice_phishing, profile

app = FastAPI(title="안심케어 AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(care_agent.router,      prefix="/api")
app.include_router(simulation.router,      prefix="/api")
app.include_router(doc_reader.router,      prefix="/api")
app.include_router(products.router,        prefix="/api")
app.include_router(bucket_list.router,     prefix="/api")
app.include_router(voice_phishing.router,  prefix="/api")
app.include_router(profile.router,         prefix="/api")

# React 빌드 결과물 서빙 (npm run build 후 사용)
_DIST = Path(__file__).parent.parent / "frontend" / "dist"
if _DIST.exists():
    app.mount("/assets", StaticFiles(directory=_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        return FileResponse(_DIST / "index.html")
