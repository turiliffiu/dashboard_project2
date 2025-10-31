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
### Crea una VM Ubuntu/Debian:

- CPU: 2 core

- RAM: 2–4 GB

- Disco: 10–20 GB

- Rete: NAT o Bridge con IP statico

### Dopo l’installazione:

Accedi via SSH o console:

`ssh utente@ip_server`

Aggiorna il sistema:

`sudo apt update && sudo apt upgrade -y`

## 🧰 2️⃣ — Installa i pacchetti necessari
`sudo apt install python3 python3-venv python3-pip git nginx -y`

## 🧬 3️⃣ — Clona il progetto da GitHub

Scegli dove metterlo, ad esempio in /var/www/:

cd /var/www/
sudo git clone https://github.com/<tuo-username>/<nome-repo>.git
sudo chown -R $USER:$USER <nome-repo>
cd <nome-repo>


Ora la struttura del progetto Django sarà disponibile sul server.

## 🐍 4️⃣ — Crea ambiente virtuale Python
python3 -m venv venv
source venv/bin/activate


Installa i pacchetti del progetto (devono essere elencati in requirements.txt):

pip install --upgrade pip
pip install -r requirements.txt

## ⚙️ 5️⃣ — Configura Django
1. Crea il file .env (se usi variabili d’ambiente)

Esempio:

DEBUG=False
SECRET_KEY=metti_una_chiave_sicura
ALLOWED_HOSTS=127.0.0.1,localhost,tuo-dominio.com
DATABASE_URL=sqlite:///db.sqlite3


(Non committare questo file su GitHub.)

2. Esegui le migrazioni e raccogli statici
python manage.py migrate
python manage.py collectstatic --noinput

3. Testa il server Django (verifica che funzioni)
python manage.py runserver 0.0.0.0:8000


Apri il browser e vai su:

http://IP_del_server:8000


Se vedi il tuo sito Django → funziona!

## 🔥 6️⃣ — Esegui con Gunicorn

Interrompi il server di sviluppo (CTRL+C) e installa Gunicorn:

pip install gunicorn


Prova a eseguire l’app:

gunicorn --bind 0.0.0.0:8000 nome_progetto.wsgi


(sostituisci nome_progetto con quello della tua cartella Django principale — quella dove c’è settings.py)

## 🌐 7️⃣ — Configura Nginx come reverse proxy

Crea un file di configurazione:

sudo nano /etc/nginx/sites-available/django_app


Inserisci:

server {
    listen 80;
    server_name tuo-dominio.com 192.168.x.x;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/<nome-repo>;
    }

    location / {
        include proxy_params;
        proxy_pass http://127.0.0.1:8000;
    }
}


Attiva la configurazione:

sudo ln -s /etc/nginx/sites-available/django_app /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx


Controlla se funziona aprendo:

http://IP_del_server


Dovresti vedere la tua app Django servita tramite Nginx ✅

## ⚙️ 8️⃣ — (Opzionale ma consigliato) Automatizza Gunicorn con systemd

Crea un servizio systemd:

sudo nano /etc/systemd/system/gunicorn.service


Contenuto:

[Unit]
Description=Gunicorn service per Django
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/<nome-repo>
Environment="PATH=/var/www/<nome-repo>/venv/bin"
ExecStart=/var/www/<nome-repo>/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 nome_progetto.wsgi:application

[Install]
WantedBy=multi-user.target


Avvia e abilita:

sudo systemctl start gunicorn
sudo systemctl enable gunicorn


Ora Gunicorn partirà automaticamente ad ogni riavvio del server 🎯
