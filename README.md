# 🥘 Dashboard 

Dashboard è un'applicazione web che permette di conservare e riutilizzare delle procedure operative con il semplice copia e incolla

## 🎯 Obiettivi principali

- primo

- secondo

## 🚀 PASSAGGI PRINCIPALI

✅ Preparare il server su Proxmox

🧱 Installare i pacchetti necessari (Python, Git, virtualenv, Nginx, ecc.)

📦 Clonare il progetto da GitHub

🐍 Creare l’ambiente virtuale e installare le dipendenze

⚙️ Configurare Django (migrazioni, static, .env)

🔥 Eseguire con Gunicorn

🌐 Esporre il sito con Nginx come reverse proxy

🧩 Automatizzare l’avvio con systemd

## 🪟 1️⃣ — Preparare il server su Proxmox
### Crea una VM Ubuntu/Debian:

- CPU: 2 core

- RAM: 2–4 GB

- Disco: 10–20 GB

- Rete: NAT o Bridge con IP statico

## 🧰 2️⃣ — Installare i pacchetti necessari
### SSH nella VM
`ssh admin@192.168.1.xxx` <br>

### 1. Aggiorna sistema
`sudo apt update && sudo apt upgrade -y` <br>

### 2. Installa Python 3.11
`sudo apt install python3.11 python3.11-venv python3.11-dev -y` <br>
`sudo apt install python3-pip build-essential libpq-dev -y` <br>

### 3. Installa NGINX
`sudo apt install nginx -y` <br>
`sudo systemctl enable nginx` <br>

### 4. Installa Redis
`sudo apt install redis-server -y` <br>
`sudo systemctl enable redis-server` <br>

### 5. Installa supervisor (per gestire processi)
`sudo apt install supervisor -y` <br>
`sudo systemctl enable supervisor` <br>

### 6. Installa Git
`sudo apt install git -y` <br>

### 7. Crea utente applicativo
`sudo adduser --system --group --home /opt/dashboard dashboard` <br>
`sudo mkdir -p /opt/dashboard` <br>
`sudo chown dashboard:dashboard /opt/dashboard` <br>

## 🧬 3️⃣ — Clonare il progetto da GitHub
### 1. Diventa utente dashboard
`sudo su - dashboard` <br>

### 2. Clona repository
`cd /opt/dashboard` <br>
`git clone https://github.com/turiliffiu/dashboard_project2.git` <br>

Ora la struttura del progetto Django sarà disponibile sul server

## 🐍 4️⃣ — Creare l’ambiente virtuale e installare le dipendenze
### 1. Crea virtual environment
`python3.11 -m venv venv` <br>
`source venv/bin/activate` <br>

### 2. Installa dipendenze
`pip install --upgrade pip` <br>
`pip install -r requirements.txt` <br>


## ⚙️ 5️⃣ — Configura Django
Crea il file .env 
`nano .env` <br>

Esempio:

`DEBUG=False` <br>
`SECRET_KEY=metti_una_chiave_sicura` <br>
`ALLOWED_HOSTS=127.0.0.1,localhost,tuo-dominio.com` <br>
`DATABASE_URL=sqlite:///db.sqlite3` <br>

### Esegui le migrazioni e raccogli statici
`python manage.py migrate` <br>
`python manage.py collectstatic --noinput` <br>
`python manage.py createsuperuser` <br>
 
### Testa il server Django (verifica che funzioni)
`python manage.py runserver 0.0.0.0:8000`


Apri il browser e vai su:

`http://IP_del_server:8000`

Se vedi il tuo sito Django → funziona!

## 🔥 6️⃣ — Esegui con Gunicorn

Interrompi il server di sviluppo (CTRL+C) e installa Gunicorn:

`pip install gunicorn`


Prova a eseguire l’app:

`gunicorn --bind 0.0.0.0:8000 nome_progetto.wsgi`


(sostituisci nome_progetto con quello della tua cartella Django principale — quella dove c’è settings.py)

## 🌐 7️⃣ — Configura Nginx come reverse proxy

Crea un file di configurazione:

`sudo nano /etc/nginx/sites-available/dashboard`

Inserisci:

     upstream dashboard {
         server 127.0.0.1:8000 fail_timeout=0;
     }
     
     server {
         listen 80;
         server_name 192.168.1.10 dashboard.local;
         
         client_max_body_size 10M;
         
         location /static/ {
             alias /opt/dashboard/app/staticfiles/;
             expires 30d;
             add_header Cache-Control "public, immutable";
         }
         
         location /media/ {
             alias /opt/dashboard/app/media/;
             expires 7d;
         }
         
         location / {
             proxy_pass http://dashboard;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header Host $host;
             proxy_redirect off;
         }
     }

# Abilita site
`sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/` <br>
`sudo nginx -t` <br>
`sudo systemctl restart nginx` <br>




Attiva la configurazione:

`sudo ln -s /etc/nginx/sites-available/django_app /etc/nginx/sites-enabled` <br>
`sudo nginx -t` <br>
`sudo systemctl restart nginx` <br>


Controlla se funziona aprendo:

`http://IP_del_server`


Dovresti vedere la tua app Django servita tramite Nginx ✅

## ⚙️ 8️⃣ — Automatizzazione Gunicorn con systemd

Crea un servizio systemd:

`sudo nano /etc/systemd/system/gunicorn.service`


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

`sudo systemctl start gunicorn` <br>
`sudo systemctl enable gunicorn` <br>


Ora Gunicorn partirà automaticamente ad ogni riavvio del server 🎯
