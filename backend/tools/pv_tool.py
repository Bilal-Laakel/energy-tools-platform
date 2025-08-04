# -*- coding: utf-8 -*-
import requests

def pv_correction(latitude: float, longitude: float, tilt: float, azimuth: float) -> dict:
    """
    Calcule le facteur de correction PV en utilisant l'API PVGIS via un proxy
    pour contourner les restrictions réseau de Render.
    """
    base_url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc"

    def call_pvgis(angle: float, aspect: float):
        # Passer par un proxy pour éviter les blocages CORS/timeout Render
        proxy_url = f"https://corsproxy.io/?{base_url}?lat={latitude}&lon={longitude}&angle={angle}&aspect={aspect}&peakpower=1&loss=14&outputformat=json"
        print(f"Appel PVGIS via proxy : {proxy_url}")
        response = requests.get(proxy_url, timeout=20)
        response.raise_for_status()
        return response.json()

    # --- Simulation réelle ---
    data_reelle = call_pvgis(tilt, azimuth)
    prod_reelle = data_reelle["outputs"]["totals"]["fixed"]["E_y"]

    # --- Simulation optimale ---
    data_opt = call_pvgis(35, 180)  # Inclinaison optimale 35°, azimuth plein sud
    prod_opt = data_opt["outputs"]["totals"]["fixed"]["E_y"]

    facteur_correction = (prod_reelle / prod_opt) * 100

    return {
        "production_annuelle_kWh_kWp": round(prod_reelle, 2),
        "production_optimale_kWh_kWp": round(prod_opt, 2),
        "inclinaison_utilisee": tilt,
        "azimuth_utilise": azimuth,
        "facteur_correction": round(facteur_correction, 2)
    }