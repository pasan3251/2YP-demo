import frappe

ROLE_PORTAL_MAP = {
    "PG Student":            "/app/pg-student-portal",
    "PG Supervisor":         "/app/pg-supervisor-portal",
    "PG Examiner":           "/app/pg-examiner-portal",
    "PG Coordinator":        "/app/pg-coordinator-portal",
    "PG Head of Department": "/app/pg-department-portal",
}


def user_login_redirect(login_manager):
    """on_session_creation hook.

    Frappe calls this after a successful login.
    frappe.session.user is set at this point.
    frappe.local.response['home_page'] is read by the JS login handler
    and used as: window.location.href = home_page
    So this must be a full /app/<slug> path.
    """
    user = frappe.session.user
    if user in ("Administrator", "Guest"):
        return
    roles = frappe.get_roles(user)
    for role, path in ROLE_PORTAL_MAP.items():
        if role in roles:
            frappe.local.response["home_page"] = path
            return
