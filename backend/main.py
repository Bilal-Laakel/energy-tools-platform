# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from tools.pv_tool import pv_correction
import os

app = FastAPI(title="Plateforme d'Outils Énergétiques")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === API ===
@app.post("/pv-tool")
def pv_tool(latitude: float, longitude: float, tilt: float, azimuth: float):
    return pv_correction(latitude, longitude, tilt, azimuth)

# === FRONTEND ===
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))

@app.get("/")
def serve_home():
    """Charge la page d'accueil par défaut."""
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/{file_name}")
def serve_page(file_name: str):
    """Sert un fichier HTML spécifique, sinon redirige vers index.html."""
    file_path = os.path.join(frontend_path, file_name)

    # Si l'URL correspond à un fichier HTML existant
    if file_name.endswith(".html") and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Sinon, on revient à index.html
    return FileResponse(os.path.join(frontend_path, "index.html"))


