import requests
from fastapi import APIRouter
from fastapi import HTTPException
from datetime import datetime


router = APIRouter()

dnd_api_url = "https://www.dnd5eapi.co/api"


def get_ability_desc(ability: str = "cha"):
    try:
        res = requests.get(f"{dnd_api_url}/ability-scores/{ability}", timeout=5)
        # Börje does some sanity checks, thats good!
        if res.status_code != 200:
            return HTTPException(
                status_code=res.status_code,
                detail="Sorry, didn't find that ability for some reason",
            )
        res = res.json()
        if "desc" not in res:
            return HTTPException(
                status_code=400,
                detail="Sorry, didn't find that ability for some reason",
            )
        return "".join(res.get("desc"))

    except Exception:
        return HTTPException(
            status_code=500, detail="Woppsi daisy, something went wrong"
        )


@router.get("/ability/{ability}")
async def get_dnd_ability_desc(ability: str = "cha"):
    try:
        desc = get_ability_desc(ability)
        if isinstance(desc, HTTPException):
            return desc
        return {"status": "success", "abilityDesc": desc}

    except Exception:
        return HTTPException(
            status_code=500, detail="Woppsi daisy, something went wrong"
        )
    except HTTPException as e:
        return e


@router.post("/ability/{ability}")
async def save_dnd_ability_desc(ability: str = "cha"):
    try:
        desc = get_ability_desc(ability)
        if isinstance(desc, HTTPException):
            return desc

        today = datetime.now().strftime("%Y-%m-%d")
        with open(f"/file-storage/dnd/{ability}-{today}.txt", "w+") as f:
            f.write(desc)

        return {"status": "success", "abilityDesc": desc}

    except Exception:
        return HTTPException(
            status_code=500, detail="Woppsi daisy, something went wrong"
        )
