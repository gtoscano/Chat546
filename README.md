# Chat546 — LLM/NLP Sandbox for CSC/AI 446/546 (CUA)

> **Educational Use**  
> Chat546 is a course-backed experimentation space to prototype, test, and evaluate Large Language Models (LLMs) and other NLP approaches for **CSC/AI/DA 446/546** at **The Catholic University of America**. It is designed for rapid iteration in a teaching/research context and is not intended as a “lock-it-down” production service.

---

## 🎯 Purpose

- Provide a **hands-on sandbox** to try prompts, RAG, fine-tuning/evals, and small demos.
- Support **class projects** that need background jobs (Celery), queues (RabbitMQ), caching (Redis), and a web UI (Django).
- Encourage **reproducibility, ethics, and privacy** in applied AI work.

---

## 🧱 Stack & Services

- **Django** (web app & APIs) — served behind **Nginx**
- **PostgreSQL** (database)
- **Celery** (background workers) + **Celery Beat** (scheduled tasks)
- **RabbitMQ** (message broker)
- **Redis** (cache/results)
- **Flower** (Celery monitoring UI)

---

## 🚀 Quick Start

### 1) Prerequisites

- Docker & Docker Compose
- Bash shell

### 2) Clone & Build

```bash
git clone https://github.com/gtoscano/Chat546.git
cd Chat546
docker compose build --no-cache
```

### 3) Configure Environment

Create a `variables.env` in the project root. This sample mirrors typical class needs; adjust as necessary.

```ini
# --- Broker/Backend ---
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
AMQP_HOST=rabbitmq
AMQP_USERNAME=guest
AMQP_PASSWORD=guest
AMQP_PORT=5672
AMQP_VHOST=/

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=1
REDIS_DB_OPT=1
REDIS_DB_CELERY=1
REDIS_DB_RESULT=2
REDIS_DB_CACHE=3
CELERY_BROKER=redis://redis:6379/1
CELERY_BACKEND=redis://redis:6379/2

# --- Database ---
DB_HOST=postgres
DB_ENGINE=django.db.backends.postgresql
DB_PORT=5432
POSTGRES_DB=chat546
POSTGRES_USER=postgres
POSTGRES_PASSWORD=CHANGE_ME

# --- Django bootstrap (optional automation) ---
DJANGO_SUPERUSER_FIRST_NAME=Admin
DJANGO_SUPERUSER_LAST_NAME=User
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=CHANGE_ME
CREATE_SUPERUSER=True
RUN_INIT_SCRIPT=True

# --- Hosting / Misc ---
ALLOWED_HOSTS=localhost,127.0.0.1,chat.toscano.ai
SECURE_SSL_REDIRECT=True
HOST_IP=127.0.0.1
HOST_NAME=chat546-local
PARENT_DIR=/app
DOCKER_GID=996
```

### 4) Launch

```bash
docker compose up -d
```

Open:

- App: [http://localhost/](http://localhost/) (or your domain)
- Flower: [http://localhost:5556](http://localhost:5556)

> Healthcheck: the web service exposes `GET /health/` (HTTP 200) for basic readiness.

---

## 🔧 Nginx & TLS

- Default domain example in `nginx/conf.d/default.conf` is `chat.toscano.ai`. Change to your host if needed.
- HTTPS block expects certs at:

  - `/etc/nginx/certs/origin.crt`
  - `/etc/nginx/certs/origin.key`

Mount your certs into `./certs` (already volume-mapped in compose) or comment out the TLS server block until you add them.

---

## 🧪 Typical Class Workflows

- **Prompting & RAG**: add endpoints/notebooks that call providers or local models, log prompts/responses, and track evals.
- **Background jobs**: run dataset preprocessing, batch evaluations, or scoring with Celery (`SERVICE_TYPE=celery` in compose).
- **Scheduling**: Celery Beat for periodic tasks (index refreshes, nightly eval runs).
- **Monitoring**: Flower UI for inspecting tasks, queues, and workers.

---

## 🧰 Useful Commands

Scale services (example):

```bash
docker compose up -d --scale web=3 --scale celery=5
```

View logs:

```bash
docker compose logs -f web
docker compose logs -f nginx
docker compose logs -f celery
```

Run management commands:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --noinput
```

---

## 🩺 Troubleshooting

**Nginx starts but site is unreachable**

- Ensure port mappings match internal Nginx listeners. If Nginx listens on 80/443, map `80:80`, `443:443`.

**TLS errors on startup**

- If the 443 server block references missing cert files, comment out the HTTPS server or add valid certs.

**Permissions on logs**

- Ensure `./nginx/logs/` exists and is writable by the container:

  ```bash
  mkdir -p nginx/logs
  chmod 755 nginx/logs
  ```

**Web healthcheck failing**

- Confirm the app listens on `:8080` in the web container and that `/health/` returns HTTP 200.

---

## 🔒 Data & Ethics

- Do **not** upload real PII or sensitive data.
- Follow course guidance on dataset licensing, citation, and model usage.
- When sharing results, include your **method, parameters, and seeds** for reproducibility.

---

## 🤝 Contributing

PRs and improvements are welcome—especially docs, examples, and eval scripts that help classmates learn faster.

---

## 📜 Acknowledgments

Parts of the structure and setup steps were adapted from a prior course project README.&#x20;

---

**Happy building—and see you in CSC/AI/DA 446/546!**
