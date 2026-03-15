app_name = "pg_management"
app_title = "Post Graduate Student Management System"
app_publisher = "Department of Computer Engineering"
app_description = "Managing MPhil, PhD, MSc, and MEng lifecycles."
app_email = "pgcoordinator.ce@eng.pdn.ac.lk"
app_license = "mit"

# Includes in <head>
# ------------------
# include js, css files in header of desk.html
# app_include_css = "/assets/pg_management/css/pg_management.css"
# app_include_js = "/assets/pg_management/js/pg_management.js"

# Includes in <head>
# ------------------
# include js, css files in header of web template
# web_include_css = "/assets/pg_management/css/pg_management.css"
# web_include_js = "/assets/pg_management/js/pg_management.js"

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
    "PG Applicant": {
        "validate": "pg_management.security_hooks.validate_applicant"
    },
    "PG Progress Report": {
        "validate": "pg_management.security_hooks.validate_progress_report",
        "on_update": "pg_management.notifications.validate_and_send_review_emails"
    }
}

# API setup
# --------
# REST API implementations exposed securely
override_whitelisted_methods = {
    "pg_management.api.get_student_status": "pg_management.api.get_student_status",
    "pg_management.api.submit_external_application": "pg_management.api.submit_external_application"
}

# Scheduled Tasks (Cron)
# ----------------------
scheduler_events = {
    "daily_long": [
        "pg_management.tasks.check_progress_report_deadlines"
    ]
}

# role security configuration 
# restricting specific doctypes to supervisors or students natively configured within Frappe RBAC

# Setup scripts to run after app installation
after_install = "pg_management.setup.after_install"


# --- Custom PG Login Routing ---

# Login redirect: sets home_page in login JSON response to /app/{slug}
# Frappe JS reads data.home_page and does window.location.href = home_page

# Role-based login redirect — sets the /app/ URL for Frappe's JS login handler
on_session_creation = 'pg_management.pg_management.portal_routing.user_login_redirect'
