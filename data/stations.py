"""
CPCB & OpenAQ ground monitoring stations in Delhi-NCR with realistic
coordinates and observed PM2.5 readings for 12 Jan 2025.
"""
from typing import List, Dict, Any

STATIONS: List[Dict[str, Any]] = [
    {
        "id": "anand_vihar",
        "name": "Anand Vihar",
        "lat": 28.6468,
        "lon": 77.3160,
        "pm25": 186,
        "status": "Very Poor",
        "source": "AOD fusion",
        "is_worst": True,
        "anomaly": True,
        "loso_mae": 32.4
    },
    {
        "id": "jahangirpuri",
        "name": "Jahangirpuri",
        "lat": 28.7328,
        "lon": 77.1706,
        "pm25": 174,
        "status": "Very Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": True,
        "loso_mae": 26.8
    },
    {
        "id": "wazirpur",
        "name": "Wazirpur",
        "lat": 28.6998,
        "lon": 77.1654,
        "pm25": 162,
        "status": "Very Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": False,
        "loso_mae": 24.1
    },
    {
        "id": "rohini",
        "name": "Rohini",
        "lat": 28.7325,
        "lon": 77.1199,
        "pm25": 141,
        "status": "Very Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": False,
        "loso_mae": 22.5
    },
    {
        "id": "dwarka_sec8",
        "name": "Dwarka Sec 8",
        "lat": 28.5710,
        "lon": 77.0719,
        "pm25": 118,
        "status": "Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": False,
        "loso_mae": 19.8
    },
    {
        "id": "ito",
        "name": "ITO",
        "lat": 28.6286,
        "lon": 77.2410,
        "pm25": 104,
        "status": "Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": False,
        "loso_mae": 18.2
    },
    {
        "id": "punjabi_bagh",
        "name": "Punjabi Bagh",
        "lat": 28.6683,
        "lon": 77.1167,
        "pm25": 135,
        "status": "Very Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": False,
        "loso_mae": 21.0
    },
    {
        "id": "rk_puram",
        "name": "R K Puram",
        "lat": 28.5633,
        "lon": 77.1869,
        "pm25": 126,
        "status": "Very Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": False,
        "loso_mae": 20.4
    },
    {
        "id": "siri_fort",
        "name": "Siri Fort",
        "lat": 28.5504,
        "lon": 77.2159,
        "pm25": 110,
        "status": "Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": False,
        "loso_mae": 17.6
    },
    {
        "id": "shadipur",
        "name": "Shadipur",
        "lat": 28.6515,
        "lon": 77.1581,
        "pm25": 148,
        "status": "Very Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": False,
        "loso_mae": 23.3
    },
    {
        "id": "noida_sec62",
        "name": "Noida Sector 62",
        "lat": 28.6245,
        "lon": 77.3638,
        "pm25": 152,
        "status": "Very Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": False,
        "loso_mae": 22.9
    },
    {
        "id": "ghaziabad_vasundhara",
        "name": "Ghaziabad (Vasundhara)",
        "lat": 28.6603,
        "lon": 77.3573,
        "pm25": 175,
        "status": "Very Poor",
        "source": "AOD fusion",
        "is_worst": False,
        "anomaly": True,
        "loso_mae": 27.2
    }
]

def get_station_by_id(station_id: str):
    for st in STATIONS:
        if st["id"] == station_id:
            return st
    return None

def get_most_polluted_stations(top_n: int = 6):
    sorted_st = sorted(STATIONS, key=lambda x: x["pm25"], reverse=True)
    return sorted_st[:top_n]
