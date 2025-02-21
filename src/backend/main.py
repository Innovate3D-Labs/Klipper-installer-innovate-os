from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

from src.backend.api import install_routes, printer_routes

app = FastAPI()

# CORS-Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API-Routen einbinden
app.include_router(install_routes.router, prefix="/api/v1")
app.include_router(printer_routes.router, prefix="/api/v1")

# Frontend-Dateien einbinden
frontend_path = Path(__file__).parent.parent.parent / "frontend" / "dist"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
else:
    print(f"WARNUNG: Frontend-Verzeichnis nicht gefunden: {frontend_path}")

# Debug-Route
@app.get("/debug/paths")
async def debug_paths():
    """Debug-Route um Pfade zu überprüfen"""
    return {
        "current_file": __file__,
        "frontend_path": str(frontend_path),
        "frontend_exists": frontend_path.exists(),
        "frontend_contents": os.listdir(str(frontend_path)) if frontend_path.exists() else None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
