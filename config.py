from dotenv import load_dotenv
import os, pathlib

BASE_DIR = pathlib.Path(__file__).parent
load_dotenv(BASE_DIR / ".env", override=True)

TG_TOKEN      = os.getenv("TG_TOKEN")
TG_SECRET     = os.getenv("TG_SECRET")
OPENROUTER_KEY= os.getenv("OPENROUTER_KEY")
CANVA_KEY     = os.getenv("CANVA_KEY")
TEMPLATE_ID   = os.getenv("TEMPLATE_ID")

TG_API = f"https://api.telegram.org/bot{TG_TOKEN}"

SYSTEM_PROMPT = (
    "You are a data extractor that converts raw Italian restaurant menus "
    "into structured JSON exactly matching the schema provided."
)
