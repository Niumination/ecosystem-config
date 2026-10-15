#!/usr/bin/env python3
"""
weathernext_gayo.py — High-precision Agro-Climate & Disaster Early Warning CLI
for Aceh Tengah / Dataran Tinggi Gayo.

Integrates ECMWF high-resolution meteorological streams (baseline for WeatherNext 3)
with domain logic for Arabica coffee cultivation and hydro-meteorological disaster mitigation.
"""

import sys
import json
import urllib.request
import urllib.error
from datetime import datetime

# Subdistricts / Key Agro-ecological Zones in Aceh Tengah
LOCATIONS = {
    "bebesan": {"name": "Bebesan (Kemili / Sentral)", "lat": 4.6275, "lon": 96.8491, "elev": 1250},
    "takengon": {"name": "Takengon Kota", "lat": 4.6300, "lon": 96.8450, "elev": 1200},
    "kebayakan": {"name": "Kebayakan", "lat": 4.6500, "lon": 96.8500, "elev": 1220},
    "luttawar": {"name": "Lut Tawar (Pesisir Danau)", "lat": 4.6100, "lon": 96.8800, "elev": 1200},
    "bintang": {"name": "Bintang (Hulu Peusangan)", "lat": 4.5800, "lon": 96.9500, "elev": 1210},
    "pegasing": {"name": "Pegasing (Sentra Kopi)", "lat": 4.5800, "lon": 96.8200, "elev": 1300},
    "bies": {"name": "Bies", "lat": 4.5900, "lon": 96.7800, "elev": 1350},
    "kutepanang": {"name": "Kute Panang (Highland Kopi)", "lat": 4.6800, "lon": 96.7900, "elev": 1450},
    "silihnara": {"name": "Silih Nara (Angkup)", "lat": 4.6100, "lon": 96.7200, "elev": 1100},
    "ketol": {"name": "Ketol (Zona Sesar Aktif)", "lat": 4.7500, "lon": 96.7500, "elev": 950},
    "atulintang": {"name": "Atu Lintang (Kopi Organik)", "lat": 4.4500, "lon": 96.8200, "elev": 1400},
    "jagongjeget": {"name": "Jagong Jeget (Plato Selatan)", "lat": 4.3800, "lon": 96.8000, "elev": 1450},
    "celala": {"name": "Celala (Lereng Barat)", "lat": 4.5000, "lon": 96.6500, "elev": 1200},
    "rusipantara": {"name": "Rusip Antara (Perbatasan)", "lat": 4.4000, "lon": 96.5500, "elev": 1050},
    "linge": {"name": "Linge (Isaq / Savana)", "lat": 4.4200, "lon": 97.0200, "elev": 900},
}

def fetch_weather(lat: float, lon: float):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,wind_direction_10m&"
        f"hourly=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m,direct_normal_irradiance&"
        f"daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max&"
        f"timezone=Asia%2FJakarta&forecast_days=3"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "WeatherNextGayo/1.0 (Niumination Ecosystem)"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())

def assess_coffee_microclimate(temp: float, rh: int, rain: float, solar_rad: float):
    # Coffee Arabica optimal temperature: 15°C - 24°C
    temp_status = "Optimal"
    if temp < 15.0:
        temp_status = "Cenderung Dingin (Pertumbuhan Lambat)"
    elif temp > 24.0:
        temp_status = "Terlalu Panas (Risiko Kematangan Prematur / Hama PBKo)"

    # Leaf Rust (Hemileia vastatrix) & Fungal Risk: High RH (>85%) + Temp 18-24°C
    if rh >= 85 and 18.0 <= temp <= 25.0:
        rust_risk = "TINGGI (Waspada Jamur Karat Daun / Hemileia vastatrix)"
    elif rh >= 75:
        rust_risk = "SEDANG (Pantau sirkulasi naungan pohon peneduh)"
    else:
        rust_risk = "RENDAH (Kondisi relatif kering/terkendali)"

    # Post-harvest Drying (Penjemuran Gabah/Green Bean)
    if rain > 0.1:
        drying_window = "TIDAK DISARANKAN (Hujan turun - Tutup kubah para-para/terpal)"
    elif solar_rad > 300.0 and rh < 75:
        drying_window = "SANGAT BAIK (Radiasi matahari cukup kuat, penjemuran optimal)"
    elif solar_rad > 150.0:
        drying_window = "CUKUP (Penjemuran lambat, periksa kelembapan berkala)"
    else:
        drying_window = "MINIMAL (Mendung/rendah radiasi)"

    return {
        "temperature_c": temp,
        "temperature_status": temp_status,
        "relative_humidity_pct": rh,
        "leaf_rust_risk": rust_risk,
        "drying_recommendation": drying_window,
    }

def assess_disaster_risk(current_rain: float, daily_rain_sum: float, wind_speed: float, loc_key: str):
    alerts = []
    
    # Landslide (Longsor) threshold for steep mountainous terrains
    landslide_risk = "RENDAH"
    if daily_rain_sum >= 50.0 or current_rain >= 15.0:
        landslide_risk = "BAHAYA TINGGI (Saturasi tanah jenuh, lereng kopi curam rawan longsor)"
        alerts.append("PERINGATAN DINI: Potensi longsor di lereng perkebunan dan tebing jalan lintas.")
    elif daily_rain_sum >= 25.0 or current_rain >= 5.0:
        landslide_risk = "WASPADA (Hujan sedang kontinu, waspadai retakan tanah)"
        alerts.append("WASPADA: Tingkat curah hujan dapat memicu pergerakan tanah di lereng curam.")

    # Flood / Lake overflow risk
    lake_risk = "NORMAL"
    if loc_key in ["luttawar", "bintang", "kebayakan", "takengon"]:
        if daily_rain_sum >= 40.0:
            lake_risk = "WASPADA LUAPAN (Daerah Tangkapan Air Danau Lut Tawar & DAS Peusangan terisi deras)"
            alerts.append("WASPADA: Debit air Danau Lut Tawar / hilir sungai Peusangan meningkat.")

    # Wind gust risk
    wind_risk = "NORMAL"
    if wind_speed >= 35.0:
        wind_risk = "BAHAYA (Angin kencang, pohon pelindung kopi berisiko tumbang)"
        alerts.append("BAHAYA ANGIN: Kurangi aktivitas di bawah pohon peneduh lamtoro/suren yang tinggi.")
    elif wind_speed >= 20.0:
        wind_risk = "SEDANG"

    return {
        "current_rain_mm": current_rain,
        "forecast_rain_sum_mm": daily_rain_sum,
        "wind_speed_kmh": wind_speed,
        "landslide_risk": landslide_risk,
        "lake_overflow_risk": lake_risk,
        "wind_risk": wind_risk,
        "alerts": alerts,
    }

def analyze_location(loc_key: str):
    loc = LOCATIONS.get(loc_key.lower())
    if not loc:
        raise ValueError(f"Lokasi '{loc_key}' tidak ditemukan. Pilihan: {', '.join(LOCATIONS.keys())}")

    data = fetch_weather(loc["lat"], loc["lon"])
    curr = data["current"]
    hourly = data["hourly"]
    daily = data["daily"]

    # current or nearest hour solar irradiance
    solar_rad = hourly.get("direct_normal_irradiance", [0])[0] if hourly.get("direct_normal_irradiance") else 0.0
    daily_rain_sum = daily.get("precipitation_sum", [0.0])[0]

    coffee_assessment = assess_coffee_microclimate(
        temp=curr["temperature_2m"],
        rh=curr["relative_humidity_2m"],
        rain=curr["precipitation"],
        solar_rad=solar_rad
    )

    disaster_assessment = assess_disaster_risk(
        current_rain=curr["precipitation"],
        daily_rain_sum=daily_rain_sum,
        wind_speed=curr["wind_speed_10m"],
        loc_key=loc_key.lower()
    )

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M WIB"),
        "location": loc["name"],
        "coordinates": {"lat": loc["lat"], "lon": loc["lon"], "elevation_m": loc["elev"]},
        "coffee_analysis": coffee_assessment,
        "disaster_mitigation": disaster_assessment,
        "daily_forecast": {
            "max_temp": daily["temperature_2m_max"][0],
            "min_temp": daily["temperature_2m_min"][0],
            "rain_prob_pct": daily["precipitation_probability_max"][0],
            "total_rain_mm": daily["precipitation_sum"][0],
        }
    }

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "bebesan"
    as_json = "--json" in sys.argv
    if as_json:
        target = [a for a in sys.argv[1:] if a != "--json"][0] if len(sys.argv) > 2 else "bebesan"

    try:
        res = analyze_location(target)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if as_json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return

    print("================================================================")
    print(f" ☕ GAYO AGRO-CLIMATE & MITIGASI BENCANA (WeatherNext Pipeline)")
    print("================================================================")
    print(f" Lokasi: {res['location']} (Elevasi: ~{res['coordinates']['elevation_m']} mdpl)")
    print(f" Waktu Analisis: {res['timestamp']}")
    print("----------------------------------------------------------------")
    print(f" 🌡️  Suhu Aktual: {res['coffee_analysis']['temperature_c']}°C ({res['coffee_analysis']['temperature_status']})")
    print(f" 💧 Kelembapan Relatif: {res['coffee_analysis']['relative_humidity_pct']}%")
    print(f" 🌧️  Curah Hujan Saat Ini: {res['disaster_mitigation']['current_rain_mm']} mm/jam")
    print(f" 🌬️  Kecepatan Angin: {res['disaster_mitigation']['wind_speed_kmh']} km/jam")
    print("----------------------------------------------------------------")
    print(" [ANALISIS PERTANIAN KOPI ARABIKA]")
    print(f" • Risiko Karat Daun: {res['coffee_analysis']['leaf_rust_risk']}")
    print(f" • Rekomendasi Penjemuran: {res['coffee_analysis']['drying_recommendation']}")
    print("----------------------------------------------------------------")
    print(" [ANALISIS MITIGASI BENCANA HIDROMETEOROLOGI]")
    print(f" • Risiko Tanah Longsor: {res['disaster_mitigation']['landslide_risk']}")
    print(f" • Risiko Luapan Danau/DAS: {res['disaster_mitigation']['lake_overflow_risk']}")
    if res['disaster_mitigation']['alerts']:
        for alt in res['disaster_mitigation']['alerts']:
            print(f" ⚠️  {alt}")
    else:
        print(" • Peringatan Ekstrem: Tidak ada sinyal ancaman darurat saat ini.")
    print("----------------------------------------------------------------")
    print(f" Prakiraan Hari Ini: Min {res['daily_forecast']['min_temp']}°C / Max {res['daily_forecast']['max_temp']}°C, "
          f"Peluang Hujan {res['daily_forecast']['rain_prob_pct']}%, Total Hujan {res['daily_forecast']['total_rain_mm']} mm")
    print("================================================================")

if __name__ == "__main__":
    main()
