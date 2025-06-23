import requests, time
from config import CANVA_KEY, TEMPLATE_ID

HEAD = {"Authorization": f"Bearer {CANVA_KEY}"}

def create_design(vars_: dict) -> str:
    r = requests.post(
        "https://api.canva.com/v1/designs",
        json={"template_id": TEMPLATE_ID, "variables": vars_},
        headers=HEAD
    )
    r.raise_for_status()
    return r.json()["id"]

def export_pdf(design_id: str) -> bytes:
    url = f"https://api.canva.com/v1/designs/{design_id}/exports"
    r = requests.post(url, json={"format": "pdf"}, headers=HEAD)
    r.raise_for_status()
    exp_id = r.json()["id"]

    for _ in range(20):            # 10-s max
        status = requests.get(f"{url}/{exp_id}", headers=HEAD).json()
        if status["state"] == "finished":
            return requests.get(status["download_url"]).content
        time.sleep(0.5)
    raise TimeoutError("Canva export timed out")
