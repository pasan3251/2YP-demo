# Postgraduate Student Management System
### Built on Frappe v17 + ERPNext v17

A web-based Postgraduate Student Management System covering the full academic
lifecycle — application, registration, progress monitoring, thesis examination,
and graduation — for MPhil, PhD, MSc, and MEng students.

---

## Quick Start

```bash
bench get-app pg_management https://github.com/pasan3251/2YP-demo.git
bench --site <your-site> install-app pg_management
bench --site <your-site> migrate
```

---

## Demo Accounts

| Role | Email | Password |
|---|---|---|
| Administrator | Administrator | admin |
| PG Student | student_audit1@demo.test | Demo@1234 |
| PG Supervisor | supervisor1@demo.test | Demo@1234 |
| PG Examiner | examiner1@demo.test | Demo@1234 |
| PG Coordinator | coordinator1@demo.test | Demo@1234 |
| PG Head of Department | hod1@demo.test | Demo@1234 |

---

## Prerequisites

- Docker + Docker Compose
- Frappe v17 + ERPNext v17 bench
- Python 3.11+, MariaDB 10.6+, Redis 6+

---

## Documentation

See the [`docs/`](docs/) directory for full documentation including:
- Architecture overview
- Student lifecycle process map
- Implementation guide
- Demo and deployment guide

---

## License

MIT
