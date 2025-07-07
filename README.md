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
## 🌐 Architettura Cloud, Telecomunicazioni e Note Tecniche

### ☁️ **Cloud & Networking Overview**

Questo bot è progettato come microservizio **cloud-native**, con tutti i componenti principali distribuiti su infrastruttura gestita (PaaS) tramite [Render.com](https://render.com/).

#### **Componenti e flusso dati**

- **Render.com**  
  Ospita l'applicazione Python (Flask) e fornisce:
    - Endpoint HTTPS pubblico per il webhook Telegram.
    - Deploy automatico, scaling e gestione risorse.
    - IP pubblici statici per l'accesso alle API esterne (Canva, OpenRouter).

- **Flask**  
  Micro web framework Python che gestisce:
    - Routing delle richieste dal webhook Telegram.
    - Orchestrazione delle chiamate a OpenRouter (AI) e Canva API.

- **API Integration**
    - **Telegram Bot API:** ricezione/invio messaggi e documenti.
    - **OpenRouter/DeepSeek API:** parsing AI e conversione testo → dati strutturati.
    - **Canva API:** generazione e download PDF dal template.

#### **Topologia rete**

```text
Telegram User
    |
    v
Telegram Server <----> Render.com (Flask API) <----> OpenRouter API
                                  |
                                  +-----> Canva API
                                  
```

- Tutto il traffico è cifrato (**HTTPS**).
- Render gestisce IP pubblici statici per le richieste in uscita:
    - `52.41.36.82`
    - `54.191.253.12`
    - `44.226.122.3`
  (Visibili anche nella dashboard Render → Outbound IP Addresses)

#### Osservazioni tecniche & sicurezza
- **Zero server fisici**: l’intera applicazione è *serverless*; tutta la logica, l’hosting e la sicurezza di base sono delegati al cloud.
- **Gestione segreti**: variabili ambiente (.env) sono salvate nella dashboard Render, *mai* versionate su GitHub.
- **Monitoring**: puoi controllare i log, il traffico e le metriche in tempo reale direttamente su Render.
- **Scalabilità**: la piattaforma scala automaticamente (limiti: free tier = qualche secondo di "wake up" se inattivo).
- **Firewall/Whitelisting**: se necessario, puoi fornire gli IP pubblici Render a servizi esterni (es. Canva API) per configurare whitelist.

---

### 📈 Metriche di Rete e Log

- **Outbound Bandwidth**: monitorata da Render, utile per diagnosticare anomalie di traffico o errori di configurazione API.
- **HTTP Responses**: puoi controllare graficamente il carico generato dai tuoi utenti.

---
## 📖 Licenza

MIT License

---

**Per domande o supporto:**  
Apri una Issue oppure scrivi a [michele_piccolo@outlook.com](mailto:tuo@email.com).

---

