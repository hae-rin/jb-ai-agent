import json
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
_FILE = Path("profile.json")

_DEFAULTS = {"age": 70, "income": 80, "asset": 20000, "expense": 150, "user_type": "고령층"}


class Profile(BaseModel):
    age: int = 70
    income: int = 80
    asset: int = 20000
    expense: int = 150
    user_type: str = "고령층"


@router.get("/profile", response_model=Profile)
def get_profile():
    if _FILE.exists():
        try:
            return Profile(**json.loads(_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    return Profile()


@router.post("/profile")
def save_profile(p: Profile):
    _FILE.write_text(p.model_dump_json(indent=2), encoding="utf-8")
    return {"ok": True}
