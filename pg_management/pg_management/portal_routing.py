import frappe

# URL slug map for each PG role (must match workspace DB names)
ROLE_PORTAL_MAP = {
    "PG Student":             "/app/pg-student-portal",
    "PG Supervisor":          "/app/pg-supervisor-portal",
    "PG Examiner":            "/app/pg-examiner-portal",
    "PG Coordinator":         "/app/pg-coordinator-portal",
    "PG Head of Department":  "/app/pg-department-portal",
}


def get_redirect_for_role(user=None):
    """Return the /app/ portal URL for a user based on roles, or None for admin."""
    if not user:
        user = frappe.session.user
    if user in ("Administrator", "Guest"):
        return None
    roles = frappe.get_roles(user)
    for role, url in ROLE_PORTAL_MAP.items():
        if role in roles:
            return url
    return None


def user_login_redirect(login_manager):
    """on_session_creation hook.

    Sets home_page in the Frappe JSON login response.  The Frappe v17 JS login
    handler reads ``data.home_page`` and does ``window.location.href = home_page``
    which means this must be a full /app/<route> path.
    """
    target = get_redirect_for_role()
    if target:
        frappe.local.response["home_page"] = target


def strict_route_protection(bootinfo):
    """boot_session hook.

    Frappe calls this when the browser boots (page reload / new tab).
    ``bootinfo.home_page`` is read by Frappe's router as a *workspace name*
    (NOT a full /app/ path).  E.g. for /app/pg-student-portal the workspace
    name is 'pg-student-portal'.
    """
    user = frappe.session.user
    target = get_redirect_for_role(user)
    if target:
        # Strip the leading /app/ to get the workspace name slug
        workspace_slug = target.replace("/app/", "", 1)
        bootinfo.home_page = workspace_slug
