import requests
from fastapi import APIRouter
from fastapi import HTTPException
from datetime import datetime


router = APIRouter()

weather_API = "https://goweather.herokuapp.com"


def get_weather_fast(city: str = "stockholm"):
    try:
        res = requests.get(f"{weather_API}/weather/{city}", timeout=5)

        # Börje does some sanity checks, thats good!
        if res.status_code != 200:
            return HTTPException(
                status_code=res.status_code,
                detail="Sorry, didn't find that city for some reason",
            )

        res = res.json()
        if "temperature" not in res or "description" not in res:
            return HTTPException(
                status_code=400,
                detail="Sorry, didn't find that city for some reason",
            )

        temp = res.get("temperature")
        desc = res.get("description")
        return f"{temp}, {desc}"

    except Exception:
        return HTTPException(
            status_code=500, detail="Woppsi daisy, something went wrong"
        )


@router.get("/{city}")
async def get_weather(city: str = "stockholm"):
    try:
        weather = get_weather_fast(city)
        if isinstance(weather, HTTPException):
            return weather
        return {"status": "success", "weather": weather}

    except Exception:
        return HTTPException(
            status_code=500, detail="Woppsi daisy, something went wrong"
        )

    except HTTPException as e:
        return e


@router.post("/{city}")
async def save_weather(city: str = "stockholm"):
    try:
        weather = get_weather_fast(city)
        if isinstance(weather, HTTPException):
            return weather

        today = datetime.now().strftime("%Y-%m-%d")
        with open(f"/file-storage/weather/{city}-{today}.txt", "w+") as f:
            f.write(weather)

        return {"status": "success", "weather": weather}

    except Exception:
        return HTTPException(
            status_code=500, detail="Woppsi daisy, something went wrong"
        )
