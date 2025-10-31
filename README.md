# 🥘 Dashboard 

Dashboard è un'applicazione web che permette di conservare e riutilizzare delle procedure operative con il semplice copia e incolla

## Obiettivi principali

- primo

- secondo

## 🚀 PASSAGGI PRINCIPALI

✅ Preparare il server su Proxmox

🧱 Installare dipendenze (Python, Git, virtualenv, Nginx, ecc.)

📦 Clonare il progetto da GitHub

🐍 Creare l’ambiente virtuale e installare le dipendenze

⚙️ Configurare Django (migrazioni, static, .env)

🔥 Eseguire con Gunicorn

🌐 Esporre il sito con Nginx come reverse proxy

🧩 (Opzionale) Automatizzare l’avvio con systemd

## 🪟 1️⃣ — Preparazione VM su Proxmox
Crea una VM Ubuntu/Debian:

- CPU: 2 core

- RAM: 2–4 GB

- Disco: 10–20 GB

- Rete: NAT o Bridge con IP statico

* Dopo l’installazione: *

** Accedi via SSH o console: **

*** ssh utente@ip_server ***


Aggiorna il sistema:

sudo apt update && sudo apt upgrade -y
