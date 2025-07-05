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

    # Gestione comandi /start, /stop, /help
    if text == "/start":
        send_text(chat, "Inviami il testo del menu, ti restituisco il PDF.")
        return "ok"
    elif text.strip().lower() == "/stop":
        send_text(chat, "Il bot è stato fermato. Se vuoi ripartire, scrivi /start.")
        return "ok"
    elif text.strip().lower() == "/help":
        send_text(chat,
                  "Per usare questo bot:\n1️⃣ Invia /start per iniziare.\n2️⃣ Invia il testo del menu (anche solo copiando e incollando!)\n3️⃣ Riceverai il PDF del menu pronto!\n\nScrivi solo il menu, senza altri comandi.")
        return "ok"
    elif text.startswith("/"):
        send_text(chat, "Comando non riconosciuto. Inviami solo il testo del menu!")
        return "ok"
    else:
        send_text(chat, "⏳ Elaboro il menu…")
        data   = parse_menu(text)          # DeepSeek
        dsg_id = create_design(data)       # Canva
        pdf    = export_pdf(dsg_id)
        send_pdf(chat, pdf)
        try:
            data = parse_menu(text)  # DeepSeek
            dsg_id = create_design(data)  # Canva
            pdf = export_pdf(dsg_id)
            send_pdf(chat, pdf)
        except Exception as e:
            send_text(chat, f"Errore nell'elaborazione del menu. Riprova più tardi!\n({e})")
            print(e)
        return "ok"

