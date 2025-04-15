# Pexip Policy Server (Django)

This project provides a modular Django-based external policy server for [Pexip Infinity](https://docs.pexip.com/admin/external_policy.htm), supporting:

- `/policy/v1/service/configuration`
- `/policy/v1/participant/properties`
- `/policy/v1/registrations/<alias>`

## 🚀 Features

- 🔐 Policy routing based on `local_alias`, `participant_type`, `remote_alias`, etc.
- 🧩 Modular logic in `policy/logic/`
- 🛠 Configurable via `config.py`
- 🐳 Dockerized for easy deployment

---

## 🛠 Setup

### Project Structure:
```
    pexip_policy/
    ├── settings.py             # Django settings
    ├── urls.py                 # Project URLs
    ├── wsgi.py
    policy/
    ├── views.py                # Main view for handling the policy requests
    ├── config.py               # Config for policies
    ├── logic/
    │   ├── registration.py     # Registration logic
    │   ├── participant.py      # Participant properties logic
    │   └── service.py          # Service configuration logic
```

### 🔧 Requirements

- Python 3.11+
- pip
- Docker (optional)

### 📦 Install

```bash
    pip install -r requirements.txt
    python manage.py runserver 0.0.0.0:8000
```

### API Endpoints
| Endpoint  | Method | Description |
| --- | --- | --- |
| /policy/v1/service/configuration | GET | Responds with VMR config |
| /policy/v1/participant/properties | GET | Participant-specific config |
| /policy/v1/registrations/<alias> | GET | Registration policy check |

### Configuration

Customize logic and rules in `policy/config.py`:

```
# Registration config
ALLOWED_REGISTRATION_DOMAINS = ["@example.com", "@trusted.net"]

# Service config
ROOM_CONFIG = {
    "sip:engineering@example.com": {
        "service_tag": "engineering-room",
        "name": "Engineering Room"
    },
    "sip:sales@example.com": {
        "service_tag": "sales-room",
        "name": "Sales Room"
    }
}
```

### Functionality

With the above config, we allow anyone to register using the @example.com or @trusted.net domains.

For service configuration if someone dials either sip:engineering@example.com (or just engineering) or sip:sales@example.com (or just sales), it will create a VMR with the name Engineering Room or Sales Room with individual service tags. Otherwise, create a Default Romm - {local_alias}

#### Database bits

```
python manage.py makemigrations
python manage.py migrate
python manage.py makemigrations policy
python manage.py migrate
```

Sync config from the config.py to the db:
```
    python manage.py sync_room_config
```
## ⚙️ Dynamic Configuration

Instead of hardcoding alias rules, you can now configure these via the Django Admin UI:

### RoomConfig (Service Configuration)
- Maps `local_alias` (e.g. `sip:sales@example.com`) to:
  - Room name
  - `service_tag`

### AllowedDomain (Registration Policy)
- Controls which domains (e.g. `@lorist.org`) are allowed to register

## 🧪 Syncing Static Config to Database

You can import your static config (`ROOM_CONFIG`, `ALLOWED_REGISTRATION_DOMAINS`) into the DB using:

```bash
python manage.py sync_room_config
python manage.py sync_allowed_domains
```

## 🔍 Validation Tools

Ensure consistency between `config.py` and the database:

```bash
python manage.py check_room_config_conflicts
```

## 🛠 Accessing Django Admin
```bash
python manage.py createsuperuser
```

Start the server and visit:
`http://localhost:8000/admin`

---

## Docker
### Build and run
```bash
    docker build -t pexip-policy .
    docker run -p 8000:8000 pexip-policy
```
### or use docker-compose
```bash
    docker-compose up --build
```