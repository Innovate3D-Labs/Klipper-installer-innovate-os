from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path
from .api import printer_routes, install_routes, interface_routes

app = FastAPI(title="Klipper Installer API")

# Get the absolute path to the dist directory
DIST_DIR = Path(__file__).parent.parent.parent / "dist"

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(printer_routes.router, prefix="/api/v1")
app.include_router(install_routes.router, prefix="/api/v1")
app.include_router(interface_routes.router, prefix="/api/v1")

# Serve static files from dist directory
app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="static")

# Serve index.html
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    # Wenn die Anfrage mit /api beginnt, 404 zurückgeben
    if full_path.startswith("api/"):
        return {"detail": "Not Found"}
    
    index_path = DIST_DIR / "index.html"
    if not index_path.exists():
        return {"detail": f"Frontend not built. Please run 'npm run build' first. Expected path: {index_path}"}
    
    return FileResponse(str(index_path))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
