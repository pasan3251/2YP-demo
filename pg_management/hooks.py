app_name = "pg_management"
app_title = "Post Graduate Student Management System"
app_publisher = "Department of Computer Engineering"
app_description = "Managing MPhil, PhD, MSc, and MEng lifecycles."
app_email = "pgcoordinator.ce@eng.pdn.ac.lk"
app_license = "mit"
app_logo_url = "/assets/pg_management/images/logo.png"

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
        "validate": "pg_management.security_hooks.validate_applicant",
        "on_update": "pg_management.pg_events.handle_applicant"
    },
    "PG Progress Report": {
        "validate": "pg_management.security_hooks.validate_progress_report",
        "on_update": "pg_management.notifications.validate_and_send_review_emails"
    },
    "PG Student Registration": {
        "on_update": "pg_management.pg_events.handle_registration"
    },
    "PG Thesis Submission": {
        "on_update": "pg_management.pg_events.handle_thesis"
    },
    "File": {
        "after_insert": "pg_management.pg_events.handle_file_upload"
    }
}

# API setup
# --------
# REST API implementations exposed securely
override_whitelisted_methods = {
    "pg_management.api.get_student_status": "pg_management.api.get_student_status",
    "pg_management.api.submit_external_application": "pg_management.api.submit_external_application",
    "pg_management.api_events_repo.list_student_events": "pg_management.api_events_repo.list_student_events",
    "pg_management.api_events_repo.list_upcoming_events": "pg_management.api_events_repo.list_upcoming_events",
    "pg_management.api_events_repo.list_overdue_events": "pg_management.api_events_repo.list_overdue_events",
    "pg_management.api_events_repo.mark_event_completed": "pg_management.api_events_repo.mark_event_completed",
    "pg_management.api_events_repo.list_user_notifications": "pg_management.api_events_repo.list_user_notifications",
    "pg_management.api_events_repo.fetch_document_notifications": "pg_management.api_events_repo.fetch_document_notifications",
    "pg_management.api_events_repo.resend_notification": "pg_management.api_events_repo.resend_notification",
    "pg_management.api_events_repo.list_student_documents": "pg_management.api_events_repo.list_student_documents",
    "pg_management.api_events_repo.fetch_workflow_documents": "pg_management.api_events_repo.fetch_workflow_documents",
    "pg_management.api_events_repo.fetch_visible_documents": "pg_management.api_events_repo.fetch_visible_documents"
}

# Scheduled Tasks (Cron)
# ----------------------
scheduler_events = {
    "daily_long": [
        "pg_management.tasks.generate_progress_reports",
        "pg_management.tasks.process_academic_events"
    ]
}

# role security configuration 
# restricting specific doctypes to supervisors or students natively configured within Frappe RBAC

# Setup scripts to run after app installation
after_install = "pg_management.setup.after_install"


role_home_page = {
    "PG Student": "pg-student-portal",
    "PG Supervisor": "pg-supervisor-portal",
    "PG Examiner": "pg-examiner-portal",
    "PG Coordinator": "pg-coordinator-portal",
    "PG Head of Department": "pg-department-portal",
}

fixtures = [
    "Workflow",
    "Workflow State",
    "Workflow Action Master",
    "Custom Field",
    "Client Script",
    "Property Setter"
]