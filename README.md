# 📋 Menu Telegram Bot

Un **bot Telegram intelligente** che trasforma un menu inviato come testo in un PDF ben impaginato tramite template **Canva**, utilizzando l’AI (DeepSeek/OpenRouter) per estrarre automaticamente i dati strutturati. Il PDF viene restituito direttamente all’utente su Telegram.

---

## ✨ Funzionalità principali

- **Estrazione intelligente** del contenuto dei menu in linguaggio naturale, tramite LLM (DeepSeek via OpenRouter).
- **Generazione di PDF personalizzati** usando template Canva (tramite Canva API).
- **Risposta automatica su Telegram**: l’utente riceve il menu impaginato in PDF nella chat dove ha inviato il testo.
- **Facile configurazione** e deploy (localmente o su cloud: Render, Heroku, ecc).

---

## 🚀 Flusso di lavoro

1. **L’utente invia un menu** (testo) su Telegram al bot.
2. **Il bot trasforma il testo** in dati strutturati (JSON) tramite DeepSeek.
3. **Generazione del PDF**: i dati vengono inseriti in un template Canva tramite API.
4. **Risposta su Telegram**: il PDF viene inviato in chat.

---

## ⚡️ Setup rapido

1. **Clona la repository**
    ```bash
    git clone https://github.com/tuo-utente/menu-bot.git
    cd menu-bot
    ```

2. **Crea un ambiente virtuale e installa le dipendenze**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configura il file `.env`**
    - Copia `.env.example` in `.env` e inserisci le tue chiavi:
      ```dotenv
      TG_TOKEN=    # Token del bot Telegram
      TG_SECRET=   # Stringa segreta del webhook (inventata da te)
      OPENROUTER_KEY= # API Key OpenRouter (DeepSeek)
      CANVA_KEY=   # API Key Canva
      TEMPLATE_ID= # ID template Canva (es. tmpl_...)
      ```

4. **Avvia il bot in locale**
    ```bash
    export FLASK_APP=app.py
    flask run --port 8000
    ```

5. **Esporre localmente con ngrok** *(se vuoi ricevere messaggi Telegram su localhost)*
    ```bash
    ngrok http 8000
    ```
    Copia l’URL pubblico di ngrok.

6. **Registra il webhook su Telegram**
    ```bash
    curl -X POST "https://api.telegram.org/bot$TG_TOKEN/setWebhook" \
      -d "url=https://TUO-URL-PUBBLICO/telegram/TG_SECRET"
    ```

---

## 🎨 Personalizzazione del template Canva

1. **Crea o duplica un template su Canva**.
2. **Inserisci variabili**: usa le doppie graffe, es:  
   - `{{restaurant}}` (nome ristorante)
   - `{{dish_1}}`, `{{price_1}}`, `{{dish_2}}`, ... (piatti e prezzi)
3. **Ottieni l’ID del template**: copia il codice `tmpl_...` e incollalo in `.env` come `TEMPLATE_ID`.
4. **Configura le variabili** nel prompt del bot e nel codice, assicurandoti che i nomi delle chiavi JSON e delle variabili nel template Canva siano identici.

---

## 🧩 Variabili supportate

- `{{restaurant}}` — nome del ristorante
- `{{address}}` — indirizzo (opzionale)
- `{{date}}` — data (opzionale)
- `{{dish_1}}` ... `{{dish_10}}` — nome dei piatti (espandi a piacere)
- `{{price_1}}` ... `{{price_10}}` — prezzo dei piatti
- `{{note}}` — nota a piè pagina (opzionale)

Puoi aggiungere/espandere le variabili nel template e nel prompt di sistema.

---

## 🛠️ Troubleshooting & FAQ

- **Ricevo variabili vuote nel PDF**: assicurati che il menu inviato contenga abbastanza piatti/dati e che i nomi delle variabili corrispondano **esattamente**.
- **Errore Canva API**: controlla che la chiave sia valida, che i permessi (scope) siano corretti e che il TEMPLATE_ID esista.
- **Problemi con DeepSeek/OpenRouter**: verifica la chiave API e il modello selezionato nel file `openai_helper.py`.

---

## 📁 Struttura del progetto

- `app.py` — Entrypoint Flask, webhook Telegram, orchestrazione bot
- `services/openai_helper.py` — Parsing AI del menu tramite LLM (DeepSeek)
- `services/canva_helper.py` — Gestione design ed export PDF tramite Canva API
- `config.py` — Caricamento e gestione variabili d’ambiente
- `.env.example` — Esempio configurazione variabili
- `requirements.txt` — Dipendenze Python

---

## ☁️ Deploy su Render (o Heroku)

1. Fai push della repo su GitHub.
2. Crea un nuovo Web Service su [Render](https://render.com/) (o Heroku).
3. Inserisci le variabili ambiente come da `.env`.
4. Deploy & enjoy!

---

## 📖 Licenza

MIT License

---

**Per domande o supporto:**  
Apri una Issue oppure scrivi a [michele_piccolo@outlook.com](mailto:tuo@email.com).

---

