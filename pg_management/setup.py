import frappe
from frappe.utils import getdate, today

def create_all_workflows():
    """
    Creates all 4 required Workflows:
    1. Application Evaluation Workflow (PG Applicant)
    2. Progress Report Workflow (PG Progress Report)
    3. Registration Workflow (PG Student Registration)
    4. Registration Renewal Workflow (PG Registration Renewal)
    Note: Thesis Submission Workflow already exists - skip it
    """

    # Ensure required Workflow States exist
    states_needed = [
        "Draft",
        "Pending AR Review",
        "Pending HoD & FHDC Review",
        "Senate Ratification",
        "Approved & Registered",
        "Rejected",
        "Submitted to Supervisor",
        "Forwarded to HoD / FHDC",
        "Panel Evaluated",
        "Pending Coordinator Review",
        "Pending HoD Approval",
        "Active",
        "Renewal Pending",
        "Renewal Approved",
        "Renewal Rejected",
        "Lapsed",
    ]
    for state in states_needed:
        if not frappe.db.exists("Workflow State", state):
            frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": state
            }).insert(ignore_permissions=True, ignore_links=True)
    frappe.db.commit()

    # Ensure required Roles exist
    roles_needed = [
        "PG Coordinator",
        "PG Student",
        "PG Supervisor",
        "PG Head of Department",
        "System Manager"
    ]
    for role in roles_needed:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role
            }).insert(ignore_permissions=True, ignore_links=True)
    frappe.db.commit()

    # ── 1. Application Evaluation Workflow ────────────────────────────────────
    if not frappe.db.exists("Workflow", "Application Evaluation Workflow"):
        frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Application Evaluation Workflow",
            "document_type": "PG Applicant",
            "is_active": 1,
            "override_status": 1,
            "send_email_alert": 0,
            "states": [
                {"state": "Draft",                    "doc_status": 0, "allow_edit": "PG Coordinator"},
                {"state": "Pending AR Review",         "doc_status": 0, "allow_edit": "PG Coordinator"},
                {"state": "Pending HoD & FHDC Review", "doc_status": 0, "allow_edit": "PG Head of Department"},
                {"state": "Senate Ratification",       "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "Approved & Registered",     "doc_status": 0, "allow_edit": "PG Coordinator"},
                {"state": "Rejected",                  "doc_status": 0, "allow_edit": "PG Coordinator"},
            ],
            "transitions": [
                {
                    "state": "Draft",
                    "action": "Submit for Review",
                    "next_state": "Pending AR Review",
                    "allowed": "PG Coordinator"
                },
                {
                    "state": "Pending AR Review",
                    "action": "Forward to HoD",
                    "next_state": "Pending HoD & FHDC Review",
                    "allowed": "PG Coordinator"
                },
                {
                    "state": "Pending AR Review",
                    "action": "Reject",
                    "next_state": "Rejected",
                    "allowed": "PG Coordinator"
                },
                {
                    "state": "Pending HoD & FHDC Review",
                    "action": "Forward to Senate",
                    "next_state": "Senate Ratification",
                    "allowed": "PG Head of Department"
                },
                {
                    "state": "Pending HoD & FHDC Review",
                    "action": "Reject",
                    "next_state": "Rejected",
                    "allowed": "PG Head of Department"
                },
                {
                    "state": "Senate Ratification",
                    "action": "Approve",
                    "next_state": "Approved & Registered",
                    "allowed": "System Manager"
                },
                {
                    "state": "Senate Ratification",
                    "action": "Reject",
                    "next_state": "Rejected",
                    "allowed": "System Manager"
                },
            ]
        }).insert(ignore_permissions=True, ignore_links=True)
        frappe.db.commit()
        print("Application Evaluation Workflow Created.")

    # ── 2. Progress Report Workflow ───────────────────────────────────────────
    if not frappe.db.exists("Workflow", "Progress Report Workflow"):
        frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Progress Report Workflow",
            "document_type": "PG Progress Report",
            "is_active": 1,
            "override_status": 1,
            "send_email_alert": 0,
            "states": [
                {"state": "Draft",                  "doc_status": 0, "allow_edit": "PG Student"},
                {"state": "Submitted to Supervisor", "doc_status": 0, "allow_edit": "PG Supervisor"},
                {"state": "Forwarded to HoD / FHDC","doc_status": 0, "allow_edit": "PG Head of Department"},
                {"state": "Panel Evaluated",         "doc_status": 0, "allow_edit": "PG Coordinator"},
                {"state": "Rejected",                "doc_status": 0, "allow_edit": "PG Coordinator"},
            ],
            "transitions": [
                {
                    "state": "Draft",
                    "action": "Submit",
                    "next_state": "Submitted to Supervisor",
                    "allowed": "PG Student"
                },
                {
                    "state": "Submitted to Supervisor",
                    "action": "Forward to HoD",
                    "next_state": "Forwarded to HoD / FHDC",
                    "allowed": "PG Supervisor"
                },
                {
                    "state": "Submitted to Supervisor",
                    "action": "Return for Revision",
                    "next_state": "Draft",
                    "allowed": "PG Supervisor"
                },
                {
                    "state": "Forwarded to HoD / FHDC",
                    "action": "Evaluate",
                    "next_state": "Panel Evaluated",
                    "allowed": "PG Head of Department"
                },
                {
                    "state": "Forwarded to HoD / FHDC",
                    "action": "Reject",
                    "next_state": "Rejected",
                    "allowed": "PG Head of Department"
                },
            ]
        }).insert(ignore_permissions=True, ignore_links=True)
        frappe.db.commit()
        print("Progress Report Workflow Created.")

    # ── 3. Student Registration Workflow ─────────────────────────────────────
    if not frappe.db.exists("Workflow", "Student Registration Workflow"):
        frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Student Registration Workflow",
            "document_type": "PG Student Registration",
            "is_active": 1,
            "override_status": 1,
            "send_email_alert": 0,
            "states": [
                {"state": "Draft",                    "doc_status": 0, "allow_edit": "PG Student"},
                {"state": "Pending Coordinator Review","doc_status": 0, "allow_edit": "PG Coordinator"},
                {"state": "Pending HoD Approval",     "doc_status": 0, "allow_edit": "PG Head of Department"},
                {"state": "Approved & Registered",    "doc_status": 0, "allow_edit": "PG Coordinator"},
                {"state": "Rejected",                 "doc_status": 0, "allow_edit": "PG Coordinator"},
            ],
            "transitions": [
                {
                    "state": "Draft",
                    "action": "Submit for Registration",
                    "next_state": "Pending Coordinator Review",
                    "allowed": "PG Student"
                },
                {
                    "state": "Pending Coordinator Review",
                    "action": "Forward to HoD",
                    "next_state": "Pending HoD Approval",
                    "allowed": "PG Coordinator"
                },
                {
                    "state": "Pending Coordinator Review",
                    "action": "Reject",
                    "next_state": "Rejected",
                    "allowed": "PG Coordinator"
                },
                {
                    "state": "Pending HoD Approval",
                    "action": "Approve",
                    "next_state": "Approved & Registered",
                    "allowed": "PG Head of Department"
                },
                {
                    "state": "Pending HoD Approval",
                    "action": "Reject",
                    "next_state": "Rejected",
                    "allowed": "PG Head of Department"
                },
            ]
        }).insert(ignore_permissions=True, ignore_links=True)
        frappe.db.commit()
        print("Student Registration Workflow Created.")

    # ── 4. Registration Renewal Workflow ─────────────────────────────────────
    if not frappe.db.exists("Workflow", "Registration Renewal Workflow"):
        frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Registration Renewal Workflow",
            "document_type": "PG Registration Renewal",
            "is_active": 1,
            "override_status": 1,
            "send_email_alert": 0,
            "states": [
                {"state": "Draft",            "doc_status": 0, "allow_edit": "PG Student"},
                {"state": "Renewal Pending",  "doc_status": 0, "allow_edit": "PG Coordinator"},
                {"state": "Renewal Approved", "doc_status": 0, "allow_edit": "PG Coordinator"},
                {"state": "Renewal Rejected", "doc_status": 0, "allow_edit": "PG Coordinator"},
            ],
            "transitions": [
                {
                    "state": "Draft",
                    "action": "Submit Renewal",
                    "next_state": "Renewal Pending",
                    "allowed": "PG Student"
                },
                {
                    "state": "Renewal Pending",
                    "action": "Approve Renewal",
                    "next_state": "Renewal Approved",
                    "allowed": "PG Coordinator"
                },
                {
                    "state": "Renewal Pending",
                    "action": "Reject Renewal",
                    "next_state": "Renewal Rejected",
                    "allowed": "PG Coordinator"
                },
            ]
        }).insert(ignore_permissions=True, ignore_links=True)
        frappe.db.commit()
        print("Registration Renewal Workflow Created.")
        
def after_install():
    create_all_workflows()