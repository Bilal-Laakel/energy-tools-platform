# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import traceback

# Import de ton outil PV
from tools.pv_tool import pv_correction

app = FastAPI(title="Plateforme d'Outils Énergétiques")

# === Middleware CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pour autoriser tous les appels (OK en dev/test)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Endpoint API PV ===
@app.post("/pv-tool")
def pv_tool(latitude: float, longitude: float, tilt: float, azimuth: float):
    try:
        # Appel à ta fonction métier
        correction = pv_correction(latitude, longitude, tilt, azimuth)
        return correction
    except Exception as e:
        # 🔥 Log détaillé pour Render
        print("=== ERREUR BACKEND /pv-tool ===")
        print(f"Erreur: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {e}")

# === Frontend ===
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))

@app.get("/")
def serve_home():
    return FileResponse(os.path.join(frontend_path, "index.html"))

@app.get("/{file_name}")
def serve_page(file_name: str):
    file_path = os.path.join(frontend_path, file_name)

    # Servir les fichiers HTML existants
    if file_name.endswith(".html") and os.path.isfile(file_path):
        return FileResponse(file_path)

    # Si non trouvé, renvoyer index.html par défaut
    return FileResponse(os.path.join(frontend_path, "index.html"))



