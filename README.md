#§ 🥘 Dashboard 

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
### Crea un Container Ubuntu:
     
      - arch: amd64
      - cores: 1
      - features: nesting=1
      - hostname: dashboard
      - memory: 2048
      - net0: name=eth0,bridge=vmbr0,firewall=1,ip=dhcp
      - ostype: ubuntu
      - rootfs: local-lvm,size=20G
      - swap: 2048
      - unprivileged: 1

Sulla shell del nuovo Container su Proxmox:

`sudo nano /etc/ssh/sshd_config` <br>

Modificare i seguneti parametri:

     PermitRootLogin yes
     PasswordAuthentication yes
     PermitEmptyPasswords no
          
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
`sudo usermod -s /bin/bash dashboard` <br>
`sudo su - dashboard` <br>

### 2. Clona repository
`cd /opt/dashboard` <br>
`git clone https://github.com/turiliffiu/dashboard_project2.git .` <br>

Ora la struttura del progetto Django sarà disponibile sul server

## 🐍 4️⃣ — Creare l’ambiente virtuale e installare le dipendenze
### 1. Crea virtual environment
`python3.11 -m venv venv` <br>
`source venv/bin/activate` <br>

### 2. Installa dipendenze
`pip install --upgrade pip` <br>
`pip install -r requirements.txt` <br>


## ⚙️ 5️⃣ — Configurare Django
### Crea il file `.env`

`nano .env` <br>

Scrivi:

     DEBUG=False
     SECRET_KEY=metti_una_tua_chiave_sicura    
     STATIC_ROOT=/opt/dashboard/staticfiles
     STATIC_URL=/static/

ATTENZIONE: togliere gli spazi a sx quando si fa il copia e incolla per creare il file `.env` e inserire una propria SECRET_KEY

### Esegui le migrazioni e raccogli statici
`python manage.py migrate` <br>
`python manage.py collectstatic --noinput` <br>
`python manage.py createsuperuser` <br>

NOTA: il superuser serve per entrare nell'appweb come amministratore quindi, se si vuole, si può usare come nome `admin`

### Popola il data base con dei file di esempio
`python manage.py populate_db` <br>
 
### Testa il server Django (verifica che funzioni)

ATTENZIONE: per testare in server in locale devi impostare `DEBUG=True` sul file `.env`

`python manage.py runserver 0.0.0.0:8000`


Apri il browser e vai su:

`http://IP_del_server:8000`

Se vedi il tuo sito Django → funziona!

## 🔥 6️⃣ — Esegui con Gunicorn

Interrompi il server di sviluppo (CTRL+C) e installa Gunicorn:

`pip install gunicorn`


Prova a eseguire l’app:

`gunicorn --bind 0.0.0.0:8000 dashboard_project.wsgi`


(sostituisci nome_progetto con quello della tua cartella Django principale — quella dove c’è settings.py)

## 🌐 7️⃣ — Configura Nginx come reverse proxy

Crea un file di configurazione da utente `root`:

`nano /etc/nginx/sites-available/dashboard`

Inserisci:

     upstream dashboard {
         server 127.0.0.1:8000 fail_timeout=0;
     }
     
     server {
         listen 80;
         server_name 192.168.1.xxx dashboard.local;  # Sostituisci xxx con il tuo IP
         
         client_max_body_size 10M;
         
         # File statici (CSS, JS, immagini)
         location /static/ {
             alias /opt/dashboard/staticfiles/;
             expires 30d;
             add_header Cache-Control "public, immutable";
         }
         
         # Tutte le altre richieste vanno a Gunicorn
         location / {
             proxy_pass http://dashboard;
             proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
             proxy_set_header Host $host;
             proxy_set_header X-Forwarded-Proto $scheme;
             proxy_redirect off;
             
             # Timeout per richieste lunghe
             proxy_connect_timeout 300;
             proxy_send_timeout 300;
             proxy_read_timeout 300;
         }
         
         # Log
         access_log /var/log/nginx/dashboard_access.log;
         error_log /var/log/nginx/dashboard_error.log;
     }

# Attiva la configurazione
`ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/` <br>
`rm /etc/nginx/sites-enabled/default` <br>
`chmod -R 755 /opt/dashboard/staticfiles` <br>
`chown -R dashboard:dashboard /opt/dashboard/staticfiles` <br>
`nginx -t` <br>
`systemctl restart nginx` <br>
`systemctl status nginx` <br>

Torna all'utente dashboard:

`sudo su - dashboard` <br>
`cd /opt/dashboard` <br>
`source venv/bin/activate` <br>  

Avvia Gunicorn:

`gunicorn --bind 127.0.0.1:8000 --workers 3 dashboard_project.wsgi:application` <br>


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
