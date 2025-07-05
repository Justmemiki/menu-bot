from flask import Flask, request, abort
from services.openai_helper import parse_menu
from services.canva_helper import create_design, export_pdf
from config import TG_API, TG_SECRET
import requests

app = Flask(__name__)


# Dizionario per tracciare lo stato di ogni utente
user_status = {}

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

    # Prendi lo stato attuale dell'utente (default: "active" se non esiste)
    status = user_status.get(chat, "active")

    # Gestione comandi /start, /stop, /help
    # Comando /help deve funzionare SEMPRE
    if text.lower() == "/help":
        send_text(chat,
                  "ℹ️ **Guida rapida:**\n"
                  "1️⃣ Invia /start per iniziare.\n"
                  "2️⃣ Invia il testo del menu (puoi copiare e incollare!)\n"
                  "3️⃣ Riceverai il PDF del menu pronto!\n"
                  "\n"
                  "Per fermare il bot per te: invia /stop.\n"
                  "Se hai problemi o ti serve il menu subito, scrivi a: nome@email.it o @username su Telegram."
                  )
        return "ok"

    # Comando /start: riattiva l'utente
    if text.lower() == "/start":
        user_status[chat] = "active"
        send_text(chat, "Inviami il testo del menu, ti restituisco il PDF.")
        return "ok"

    # Comando /stop: ferma il bot per quell'utente
    if text.lower() == "/stop":
        user_status[chat] = "stopped"
        send_text(chat,
                  "⏹️ Il bot è stato fermato per te!\n"
                  "Per farlo ripartire, contatta l’amministratore.\n"
                  "Se ti serve il menu PDF subito, chiedi la generazione manuale a: nome@email.it o scrivi su Telegram a @username."
                  )
        return "ok"

    # Se lo stato è stopped, blocca tutto (tranne /help)
    if status == "stopped":
        send_text(chat,
                  "⏹️ Il bot è fermo per te.\n"
                  "Per assistenza o per riattivare il servizio, contatta l’amministratore."
                  )
        return "ok"

    # Comandi sconosciuti (iniziano con /)
    if text.startswith("/"):
        send_text(chat, "Comando non riconosciuto. Inviami solo il testo del menu o /help!")
        return "ok"

    # Messaggio vuoto
    if not text:
        send_text(chat, "Messaggio vuoto! Inviami il testo del menu.")
        return "ok"


        # Elaborazione menu
    send_text(chat, "⏳ Elaboro il menu…")
    try:
        data = parse_menu(text)  # DeepSeek
        dsg_id = create_design(data)  # Canva
        pdf = export_pdf(dsg_id)
        send_pdf(chat, pdf)
    except Exception as e:
        send_text(chat, f"Errore nell'elaborazione del menu. Riprova più tardi!\n({e})")
        print(e)
    return "ok"
