from flask import Flask, request, abort
from services.openai_helper import parse_menu
from services.canva_helper import create_design, export_pdf
from config import TG_API, TG_SECRET
import requests

app = Flask(__name__)

def send_text(chat, txt):
    requests.post(f"{TG_API}/sendMessage", json={"chat_id": chat, "text": txt})

def send_pdf(chat, pdf):
    requests.post(f"{TG_API}/sendDocument",
                  data={"chat_id": chat},
                  files={"document": ("menu.pdf", pdf)})

@app.post("/telegram/<secret>")
def hook(secret):
    if secret != TG_SECRET:
        abort(403)
    upd = request.json
    msg = upd.get("message", {})
    chat = msg.get("chat", {}).get("id")
    text = msg.get("text", "")

    if text == "/start":
        send_text(chat, "Inviami il testo del menu, ti restituisco il PDF.")
        return "ok"

    send_text(chat, "⏳ Elaboro il menu…")
    data   = parse_menu(text)          # DeepSeek
    dsg_id = create_design(data)       # Canva
    pdf    = export_pdf(dsg_id)
    send_pdf(chat, pdf)
    return "ok"
