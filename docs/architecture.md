# Postgraduate Student Management System — Architecture

## Overview
Role-based academic management system built on Frappe v17.

## Data Model
- **Application Module**: PG Application, Research Proposal, Proposal Evaluation, Admission Decision
- **Registration Module**: PG Student Registration, PG Registration Renewal
- **Progress Module**: PG Progress Report, PG Review Panel, PG Progress Evaluation
- **Thesis Module**: PG Thesis Submission, Examiner Assignment, Thesis Evaluation, Final Archive
- **Supporting**: PG Academic Event, Notification Log, Document Repository

## Workflows
4 multi-state Frappe Workflows covering the full student lifecycle.

## Roles
PG Student | PG Supervisor | PG Examiner | PG Coordinator | PG Head of Department
