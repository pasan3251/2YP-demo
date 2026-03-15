import frappe

def create_workflows():
    """
    Creates the required Workflows programmatically:
    1. Application Evaluation Workflow (for PG Applicant)
    2. Progress Report Workflow (for PG Progress Report)
    """

    # Ensure required Roles exist
    roles = [
        "PG Coordinator",
        "AR",
        "Head of Department",
        "PG Student",
        "Supervisor",
        "System Manager"
    ]
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role
            }).insert(ignore_permissions=True)
            frappe.db.commit()

    # Ensure required Workflow States exist
    states = [
        "Draft",
        "Pending AR Review",
        "Pending HoD & FHDC Review",
        "Interview Scheduled",
        "Pending Proposal Evaluation",
        "Senate Ratification",
        "Approved & Registered",
        "Rejected",
        "Submitted to Supervisor",
        "Forwarded to HoD / FHDC",
        "Panel Evaluated"
    ]

    for state in states:
        if not frappe.db.exists("Workflow State", state):
            frappe.get_doc({
                "doctype": "Workflow State",
                "workflow_state_name": state
            }).insert(ignore_permissions=True)
            frappe.db.commit()

    # Ensure required Workflow Actions exist
    actions = [
        "Submit",
        "Review",
        "Forward",
        "Schedule Interview",
        "Evaluate Proposal",
        "Ratify",
        "Approve",
        "Reject",
        "Return for Revision",
        "Evaluate"
    ]

    # In older Frappe versions, Workflow Action is just the action name string in the DocType, 
    # but in v13+ it is a standard DocType to define actions.
    if frappe.get_meta("Workflow Action Master") if frappe.db.exists("DocType", "Workflow Action Master") else None:
        for action in actions:
            if not frappe.db.exists("Workflow Action Master", action):
                frappe.get_doc({
                    "doctype": "Workflow Action Master",
                    "workflow_action_name": action
                }).insert(ignore_permissions=True)
                frappe.db.commit()


    # 1. Application Evaluation Workflow
    if not frappe.db.exists("Workflow", "Application Evaluation Workflow"):
        wf1 = frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Application Evaluation Workflow",
            "document_type": "PG Applicant",
            "is_active": 1,
            "override_status": 1, # Useful to sync workflow state with document status
            "send_email_alert": 0,
            "states": [
                {
                    "state": "Draft",
                    "doc_status": 0,
                    "allow_edit": "PG Coordinator"
                },
                {
                    "state": "Pending AR Review",
                    "doc_status": 0,
                    "allow_edit": "AR"
                },
                {
                    "state": "Pending HoD & FHDC Review",
                    "doc_status": 0,
                    "allow_edit": "Head of Department"
                },
                {
                    "state": "Senate Ratification",
                    "doc_status": 0,
                    "allow_edit": "System Manager"
                },
                {
                    "state": "Approved & Registered",
                    "doc_status": 1,
                    "allow_edit": "PG Coordinator"
                },
                {
                    "state": "Rejected",
                    "doc_status": 2,
                    "allow_edit": "PG Coordinator"
                }
            ],
            "transitions": [
                {
                    "state": "Draft",
                    "action": "Submit",
                    "next_state": "Pending AR Review",
                    "allowed": "PG Coordinator"
                },
                {
                    "state": "Pending AR Review",
                    "action": "Forward",
                    "next_state": "Pending HoD & FHDC Review",
                    "allowed": "AR"
                },
                {
                    "state": "Pending HoD & FHDC Review",
                    "action": "Ratify",
                    "next_state": "Senate Ratification",
                    "allowed": "Head of Department"
                },
                {
                    "state": "Pending HoD & FHDC Review",
                    "action": "Reject",
                    "next_state": "Rejected",
                    "allowed": "Head of Department"
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
                }
            ]
        })
        wf1.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Application Evaluation Workflow Created.")


    # 2. Progress Report Workflow
    if not frappe.db.exists("Workflow", "Progress Report Workflow"):
        wf2 = frappe.get_doc({
            "doctype": "Workflow",
            "workflow_name": "Progress Report Workflow",
            "document_type": "PG Progress Report",
            "is_active": 1,
            "override_status": 1,
            "states": [
                {
                    "state": "Draft",
                    "doc_status": 0,
                    "allow_edit": "PG Student"
                },
                {
                    "state": "Submitted to Supervisor",
                    "doc_status": 0,
                    "allow_edit": "Supervisor"
                },
                {
                    "state": "Forwarded to HoD / FHDC",
                    "doc_status": 0,
                    "allow_edit": "Head of Department"
                },
                {
                    "state": "Panel Evaluated",
                    "doc_status": 1,
                    "allow_edit": "PG Coordinator"
                }
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
                    "action": "Forward",
                    "next_state": "Forwarded to HoD / FHDC",
                    "allowed": "Supervisor"
                },
                {
                    "state": "Submitted to Supervisor",
                    "action": "Return for Revision",
                    "next_state": "Draft",
                    "allowed": "Supervisor"
                },
                {
                    "state": "Forwarded to HoD / FHDC",
                    "action": "Evaluate",
                    "next_state": "Panel Evaluated",
                    "allowed": "Head of Department"
                }
            ]
        })
        wf2.insert(ignore_permissions=True)
        frappe.db.commit()
        print("Progress Report Workflow Created.")


def after_install():
    """
    Hook to run after the app is installed to setup preliminary data.
    """
    create_workflows()
