# PROJECT_SUMMARY.md — Postgraduate Student Management System

---

## Section 1 — Project Overview

A **web-based Postgraduate Student Management System** built as a custom Frappe application on top of **Frappe Framework v17** and **ERPNext v17**.

The system manages the full academic lifecycle for postgraduate students (MPhil, PhD, MSc, MEng) at a university department — from initial application and admission through annual registration, progress monitoring, thesis examination, and final graduation. All roles access the system through **role-specific Workspace dashboards** via the Frappe Desk browser interface.

**Technology:** Python, Frappe Framework v17, MariaDB, Redis, Docker  
**Access:** Browser-based at `http://localhost:8080` (Frappe Desk SPA)  
**Deployment:** Docker Compose with Frappe's official docker setup

---

## Section 2 — Roles

| Role | Responsibilities |
|---|---|
| **PG Student** | Submit applications, view registration status, submit progress reports, track thesis status |
| **PG Supervisor** | Evaluate proposals, monitor assigned students, approve progress reports, recommend for examination |
| **PG Examiner** | Receive thesis examination assignments, submit evaluation reports, record viva outcomes |
| **PG Coordinator** | Manage all applications, coordinate renewals, assign examiners, run system-wide reports |
| **PG Head of Department** | Approve admission decisions, oversee departmental performance, final thesis approvals |

---

## Section 3 — Custom DocTypes (15 total)

### Application Module
| DocType | Description |
|---|---|
| **PG Application** | Student application to a postgraduate programme |
| **Research Proposal** | Research proposal linked to an application |
| **Proposal Evaluation** | Supervisor/examiner evaluation of a research proposal |
| **PG Admission Decision** | HoD's final admission decision on an application |

### Registration Module
| DocType | Description |
|---|---|
| **PG Student Registration** | Formal registration record after admission |
| **PG Registration Renewal** | Annual academic year renewal for an active student |

### Progress Monitoring Module
| DocType | Description |
|---|---|
| **PG Progress Report** | Monthly self-report submitted by the student |
| **PG Review Panel** | Panel of academic reviewers assigned per semester |
| **PG Progress Evaluation** | Formal panel evaluation report for a student's progress |

### Thesis Examination Module
| DocType | Description |
|---|---|
| **PG Thesis Submission** | Student's formal thesis submission record |
| **PG Examiner Assignment** | Assignment of an examiner to a specific thesis |
| **PG Thesis Evaluation** | Examiner's written evaluation and viva outcome |
| **PG Final Thesis Archive** | Approved thesis archived at graduation |

### Supporting DocTypes
| DocType | Description |
|---|---|
| **PG Academic Event** | System-wide events (panels, deadlines, vivas) tracked centrally |
| **PG Notification Log** | Audit trail of all automated notifications sent |
| **PG Document Repository** | Centralised store for research documents and publications |

---

## Section 4 — Workflows (4 total)

| Workflow | States | Purpose |
|---|---|---|
| **Application & Proposal Evaluation** | 12 states | Manages student application from submission through proposal evaluation and admission decision |
| **Registration & Annual Renewal** | 8 states | Tracks student registration activation, annual renewal, and lapse conditions |
| **Progress Monitoring** | 11 states | Covers monthly report submission, panel assignment, evaluation, and escalation |
| **Thesis Examination** | 15 states | Full thesis lifecycle — submission, examiner assignment, evaluation, viva, corrections, and archival |

---

## Section 5 — Portals / Workspaces (5 total)

| Portal | Role | Contents |
|---|---|---|
| **PG Student Portal** | PG Student | My Applications, My Registration, Progress Reports, Thesis Status, Notifications |
| **PG Supervisor Portal** | PG Supervisor | My Students, Proposal Evaluations, Progress Reviews, Thesis Assignments |
| **PG Examiner Portal** | PG Examiner | Assigned Theses, Evaluation Reports, Viva Schedule |
| **PG Coordinator Portal** | PG Coordinator | All Applications, All Registrations, Examiner Assignments, System Reports, Expiring Renewals |
| **PG Department Portal** | PG Head of Department | Department Overview, Admission Decisions, Thesis Approvals, System Dashboards |

Each portal includes **number cards** (KPIs), **shortcut links**, and **query reports** scoped to the role's data access.

---

## Section 6 — Other Features

- **Automated Notifications & Reminders** — Scheduled daily tasks send email alerts for expiring registrations, overdue progress reports, and upcoming examination deadlines via Frappe's scheduler
- **Academic Event Engine** — Central `PG Academic Event` DocType logs all significant system events; dashboard widgets surface upcoming events per role
- **Document Repository** — `PG Document Repository` provides auto-mirrored research docs and publications with role-based read/write access
- **Reports & Dashboards** — 12+ custom query reports (PG Applications Overview, Registrations Pending Verification, Overdue Renewals, Thesis Examinations in Progress, etc.)
- **Demo Data** — Full set of seeded demo users, applications, registrations, progress records, and thesis submissions for all 5 roles
- **REST API Endpoints** — `pg_management.api.*` exposes key operations for external integrations (submit application, get student status, etc.)

---

## Section 7 — Known Issues / In Progress

| Issue | Status |
|---|---|
| **Portal routing on login** — Frappe v17 SPA router interprets the `role_home_page` hook value as a `Workspaces/` URL, causing a 404 on first login. Manual navigation to `/app/pg-student-portal` works correctly. | Fix in progress — `on_session_creation` hook approach being finalised |
| **Thesis archival → graduation flow** — Intermediate correction and re-submission states are implemented; the final graduation status cascade has been integrated but requires end-to-end retest | Partially complete |
| **Git push requires GitHub PAT** — The app is committed locally but push requires a Personal Access Token (repo scope) to be supplied at push time | User action required |

---

## Section 8 — Tech Stack

| Component | Version |
|---|---|
| Frappe Framework | v17 |
| ERPNext | v17 |
| Python | 3.10+ (3.14.2 in current container) |
| MariaDB | 10.6 |
| Redis | 6+ |
| Docker + Docker Compose | Latest |
| bench (Frappe CLI) | 5.29.1 |
