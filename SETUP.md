# SETUP.md — Postgraduate Student Management System
## Full Environment Setup Guide

---

## Section 1 — Prerequisites

Ensure the following are installed on your machine before proceeding:

| Software | Purpose | Download |
|---|---|---|
| **Docker Desktop** | Runs all containers (Frappe, MariaDB, Redis) | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) |
| **Git** | Source control and repo cloning | [git-scm.com](https://git-scm.com/downloads) |
| **Python 3.10+** | Required for bench CLI and scripts | [python.org](https://www.python.org/downloads/) |
| **Terminal** | PowerShell (Windows) / bash (Linux/macOS) | Built into OS |

---

## Section 2 — Verify Your Environment

Run these commands to confirm everything is installed before proceeding:

```bash
# Verify Docker is running
docker --version
docker compose version

# Verify Git
git --version

# Verify Python
python3 --version
```

Expected output:
- Docker: `Docker version 24.x.x` or later
- Docker Compose: `Docker Compose version v2.x.x` or later
- Git: `git version 2.x.x`
- Python: `Python 3.10.x` or later

> **Windows note:** Make sure Docker Desktop is running before executing any `docker` commands.

---

## Section 3 — Clone the Repository

```bash
# 1. Clone the official Frappe Docker setup
git clone https://github.com/frappe/frappe_docker.git
cd frappe_docker

# 2. Clone the pg_management app into the apps/ folder
git clone https://github.com/pasan3251/2YP-demo.git apps/pg_management
```

> The `apps/pg_management` directory will be automatically mounted into the container.

---

## Section 4 — Start the Docker Environment

```bash
# Start all containers in the background
docker compose up -d
```

> **Note:** The first run may take **5–10 minutes** as Docker pulls the Frappe, MariaDB, and Redis images. Subsequent starts are fast (under 30 seconds).

To confirm all containers are running:

```bash
docker compose ps
```

Look for `backend`, `frontend`, `db`, and `redis` containers all showing `Up`.

---

## Section 5 — Install the App on the Frappe Site

```bash
# Enter the backend container
docker compose exec backend bash

# Inside the container — install the app on your site
bench --site your.site.name install-app pg_management

# Run database migrations
bench --site your.site.name migrate

# Clear all caches
bench --site your.site.name clear-cache
```

> Replace `your.site.name` with your actual Frappe site name (e.g. `phd.local`).
> 
> If you're unsure of your site name, run: `bench --site all list-apps`

---

## Section 6 — Access the System

Once installation is complete, open your browser:

| URL | `http://localhost:8080` |
|---|---|
| **Default Admin Login** | Username: `admin` / Password: `admin` |

You will land on the Frappe Desk. From there you can navigate to any workspace or DocType via the sidebar or search bar (`Ctrl+J`).

---

## Section 7 — Demo Accounts

The following demo user accounts are pre-configured with role-specific portal access:

| Email | Password | Role | Portal |
|---|---|---|---|
| student_audit1@demo.test | Demo@1234 | PG Student | PG Student Portal |
| supervisor1@demo.test | Demo@1234 | PG Supervisor | PG Supervisor Portal |
| examiner1@demo.test | Demo@1234 | PG Examiner | PG Examiner Portal |
| coordinator1@demo.test | Demo@1234 | PG Coordinator | PG Coordinator Portal |
| hod1@demo.test | Demo@1234 | PG Head of Department | PG Department Portal |
| admin | admin | System Administrator | Full Frappe Desk |

---

## Section 8 — Continuing Development

### Stop and restart the environment

```bash
# Stop all containers
docker compose down

# Restart
docker compose up -d
```

### Run bench commands

```bash
# Access the container shell
docker compose exec backend bash

# Then run any bench command, e.g.:
bench --site your.site.name migrate
bench --site your.site.name clear-cache
bench --site your.site.name console
```

### Edit app files

App source files are mounted from the host into the container. You can edit them directly in your editor at:

```
frappe_docker/apps/pg_management/
```

Changes are reflected immediately for Python (with a worker restart). For JS/CSS changes:

```bash
docker compose exec backend bash -c "cd /home/frappe/frappe-bench && bench build"
```

### Push changes to GitHub

```bash
docker compose exec backend bash -c "cd /home/frappe/frappe-bench/apps/pg_management && git add . && git commit -m 'your commit message' && git push origin main"
```

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `docker compose up` hangs | Ensure Docker Desktop is running; check `docker ps` |
| Site not found error | Run `bench --site all list-apps` to confirm site name |
| Permission errors on files | Run `docker compose exec backend chown -R frappe:frappe /home/frappe/frappe-bench` |
| Port 8080 already in use | Stop other services using port 8080, or edit `docker-compose.yml` to change port mapping |
| `bench migrate` fails | Check Python traceback; ensure all DocType JSON files are valid |
