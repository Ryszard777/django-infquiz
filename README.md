#  Django INFquiz

Prosta aplikacja webowa (Django, PostgreSQL, Nginx, Docker).  
Umożliwia rozwiązywanie egzaminów teoretycznych dla kwalifikacji **INF.02**, **INF.03** i **INF.04**  
z automatycznym zapisem wyników, aby śledzić swój postęp w nauce.

---

## 1.  Wymagania

Przed uruchomieniem upewnij się, że masz zainstalowane:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Sprawdź wersje:
```bash
docker --version
docker compose version
```

---

## 2. Uruchomienie aplikacji

Sklonuj repozytorium:
```bash
git clone https://github.com/Ryszard777/django-infquiz.git
cd django-infquiz
```

Pierwsze uruchomienie:
```bash
docker compose up --build
```

To polecenie:
- zbuduje obrazy Dockera,
- uruchomi bazę PostgreSQL,
- poczeka, aż baza wystartuje,
- wykona migracje i `collectstatic`,
- uruchomi Gunicorna i Nginxa.

---

## 3. Uruchomianie, zatrzymanie i czyszczenie
Uruchomienie kontenera po zbudowaniu:
```bash
docker compose up
```

Zatrzymanie kontenerów:
Aby zatrzymać kontener naciśnij w terminalu `CTRL+C` po uruchomieniu.

Zatrzymanie i usunięcie danych bazy:
```bash
docker compose down -v
```

---
## 4. Dostęp do aplikacji

Po uruchomieniu przejdź do:
```
http://localhost
```

- Strona główna aplikacji: `http://localhost`
- Panel administracyjny Django: `http://localhost/admin`

Aby utworzyć użytkownika do panelu admina:
```bash
docker compose exec web python manage.py createsuperuser
```

---

## 5. Dane i trwałość bazy

Dane PostgreSQL są zapisywane w trwałym wolumenie Dockera:
```
db_data:/var/lib/postgresql/data
```

Dzięki temu baza zachowuje dane nawet po restarcie kontenerów.

Dodatkowo dane z pliku `baza.sql` są importowane automatycznie przy pierwszym uruchomieniu kontenera bazy danych.

Jeśli pojawią się problemy z pobieraniem pytań z bazy danych, sprawdź zawartość tabeli `Questions` w panelu administracyjnym Django.

---

## 6. Struktura projektu

```
├── backend/                # Kod aplikacji Django
├── nginx/                  # Konfiguracja serwera Nginx
├── baza.sql                # Dane startowe bazy (importowane automatycznie)
├── start.sh                # Skrypt startowy (migracje + collectstatic)
├── Dockerfile              # Konfiguracja obrazu Django
├── docker-compose.yaml     # Definicje wszystkich kontenerów
├── requirements.txt        # Wymagane pakiety Pythona
└── README.md
```

---


## 7. Technologie

- **Django** – framework webowy (Python)
- **PostgreSQL** – baza danych
- **Gunicorn** – serwer WSGI dla Django
- **Nginx** – reverse proxy i serwowanie plików statycznych
- **Docker & Docker Compose** – konteneryzacja całego środowiska

---