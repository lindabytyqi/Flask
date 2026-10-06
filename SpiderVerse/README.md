# SpiderVerse

Applicazione web full-stack Flask dedicata agli universi cinematografici di Spider-Man.

## Requisiti del progetto coperti

- **requirements.txt** completo e riproducibile.
- **`.env`** usato per `SECRET_KEY` e `DATABASE_URL`.
- **`.env.example`** documentato e pronto da copiare.
- **`.gitignore`** completo per ambiente virtuale, cache, database, segreti e file IDE.
- **Struttura modulare** con blueprints, models, templates, static, tests e migrations.
- **Database SQLite + Flask-SQLAlchemy + Flask-Migrate/Alembic** con migration reale in `migrations/versions/`.
- **Utenti e permessi** con registrazione/login/logout, ruoli `user` e `admin`, area admin e protezione delle modifiche API.
- **Test API/UI** con pytest.
- **Funzionalità**: universi, film, personaggi, relazioni molti-a-molti, ricerca, API REST CRUD, autenticazione e gestione ruoli.

## Tecnologie

Python, Flask, Flask-SQLAlchemy, Flask-Migrate, sessioni Flask, SQLite, HTML5, CSS3, JavaScript, REST API, pytest.

## Installazione

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
flask --app app db upgrade
python seed.py
python app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app app db upgrade
python seed.py
python app.py
```

Apri `http://127.0.0.1:5000`.

> `seed.py` ricrea da zero il database (`drop_all/create_all`) e inserisce tutti i dati demo. Per dimostrare le migrazioni al docente usa anche `flask --app app db upgrade` su un database vuoto.

## Variabili d'ambiente

Il file `.env` non va committato. La configurazione da condividere è in `.env.example`:

```env
SECRET_KEY=change-this-secret-key
DATABASE_URL=sqlite:///spiderverse.db
```

## Utenti demo

Dopo `python seed.py`:

- Admin: `admin@spiderverse.local` / `Admin123!`
- Utente: `user@spiderverse.local` / `User123!`

Permessi:

- `user`: navigazione, ricerca e lettura API.
- `admin`: tutti i permessi dell'utente + area `/admin/` + POST/PUT/DELETE delle API.

## API REST

Lettura pubblica:

```text
GET /api/characters
GET /api/characters/<id>
GET /api/movies
GET /api/movies/<id>
GET /api/universes
GET /api/universes/<id>
GET /api/search?q=Peter
```

Scrittura riservata agli amministratori autenticati:

```text
POST   /api/characters
PUT    /api/characters/<id>
DELETE /api/characters/<id>
POST   /api/movies
PUT    /api/movies/<id>
DELETE /api/movies/<id>
POST   /api/universes
PUT    /api/universes/<id>
DELETE /api/universes/<id>
```

## Migrazioni

La migration iniziale è già inclusa in `migrations/versions/0001_initial_schema.py`.

Comandi utili:

```bash
flask --app app db upgrade
flask --app app db migrate -m "descrizione modifica"
flask --app app db upgrade
flask --app app db downgrade
```

## Test

```bash
pytest -q
```

I test coprono:

- pagine UI principali;
- dettaglio personaggio;
- redirect/login;
- accesso negato a utenti normali nell'area admin;
- accesso admin;
- API GET pubbliche;
- API POST negate ad anonimi e utenti normali;
- API POST consentite agli admin;
- ricerca API.

## Struttura

```text
SpiderVerse/
├── app.py
├── config.py
├── decorators.py
├── seed.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
├── README.md
├── blueprints/
│   ├── main/
│   ├── characters/
│   ├── movies/
│   ├── universes/
│   ├── api/
│   ├── auth/
│   └── admin/
├── models/
├── migrations/
│   └── versions/
├── templates/
├── static/
├── tests/
└── instance/
```
