# -*- coding: utf-8 -*-
import requests

def pv_correction(latitude: float, longitude: float, tilt: float, azimuth: float) -> dict:
    """
    Calcule la production PV spécifique (kWh/kWp/an) et le facteur de correction
    en utilisant l'API PVGIS en temps réel.
    """
    url = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc"
    params = {
        "lat": latitude,
        "lon": longitude,
        "angle": tilt,
        "aspect": azimuth,
        "peakpower": 1,
        "loss": 14,
        "outputformat": "json"
    }

    # Requête API PVGIS
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Vérification que les données attendues existent
    try:
        production_annuelle = data["outputs"]["totals"]["fixed"]["E_y"]
    except KeyError:
        raise ValueError("Réponse PVGIS invalide. Données manquantes.")

    # Inclinaison optimale (si disponible)
    inclinaison_optimale = data.get("inputs", {}).get("angle", None)

    # Calcul du facteur de correction (ici on renvoie simplement 100% car PVGIS donne la valeur directe)
    facteur_correction = 100.0

    return {
        "production_annuelle_kWh_kWp": round(production_annuelle, 2),
        "inclinaison_utilisee": tilt,
        "azimuth_utilise": azimuth,
        "inclinaison_optimale": inclinaison_optimale,
        "facteur_correction": facteur_correction
    }