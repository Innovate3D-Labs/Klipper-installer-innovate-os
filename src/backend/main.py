from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from .api import printer_routes, install_routes, interface_routes

app = FastAPI(title="Klipper Installer API")

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
app.mount("/assets", StaticFiles(directory="../dist/assets"), name="static")

# API Routes werden später hinzugefügt
@app.get("/")
async def root():
    return FileResponse("../dist/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
