import frappe
from frappe import _

def success_response(message, data=None):
    resp = {"success": True, "message": message}
    if data is not None:
        if isinstance(data, list):
            resp["data"] = data
            resp["count"] = len(data)
        else:
            resp["data"] = data
    return resp

def error_response(message, status_code=400):
    frappe.local.response['http_status_code'] = status_code
    return {"success": False, "message": message}

# --- EVENTS API ---

@frappe.whitelist(allow_guest=False)
def list_student_events(student_email=None):
    user = frappe.session.user
    target_email = student_email or user

    if target_email != user and "PG Student" in frappe.get_roles(user):
        return error_response("Unauthorized", 403)

    try:
        data = frappe.get_all("PG Academic Event", 
            filters={"linked_student": target_email}, 
            fields=["name", "event_title", "event_type", "due_date", "status"]
        )
        return success_response("Events fetched successfully", data)
    except Exception as e:
        return error_response(str(e), 500)

@frappe.whitelist(allow_guest=False)
def list_upcoming_events():
    user = frappe.session.user
    # If student, only see their own
    is_student = "PG Student" in frappe.get_roles(user)
    filters = {"status": ["in", ["Scheduled", "Upcoming", "Due Today"]]}
    if is_student:
        filters["linked_student"] = user
        
    try:
        data = frappe.get_all("PG Academic Event", filters=filters, fields=["name", "event_title", "event_type", "due_date", "linked_student", "status"])
        return success_response("Upcoming events fetched", data)
    except Exception as e:
        return error_response(str(e), 500)

@frappe.whitelist(allow_guest=False)
def list_overdue_events():
    user = frappe.session.user
    is_student = "PG Student" in frappe.get_roles(user)
    filters = {"status": ["in", ["Overdue", "Escalated"]]}
    if is_student:
         filters["linked_student"] = user
         
    try:
        data = frappe.get_all("PG Academic Event", filters=filters, fields=["name", "event_title", "event_type", "due_date", "linked_student", "status", "escalated_flag"])
        return success_response("Overdue events fetched", data)
    except Exception as e:
        return error_response(str(e), 500)

@frappe.whitelist(allow_guest=False)
def mark_event_completed(event_name):
    try:
        if not frappe.has_permission("PG Academic Event", "write"):
            return error_response("Unauthorized", 403)
            
        event = frappe.get_doc("PG Academic Event", event_name)
        event.completed_flag = 1
        event.status = "Completed"
        event.save(ignore_permissions=False)
        return success_response(f"{event_name} marked as completed.", {"event": event_name})
    except Exception as e:
        return error_response(str(e), 500)

# --- NOTIFICATIONS API ---

@frappe.whitelist(allow_guest=False)
def list_user_notifications(user_email=None):
    user = frappe.session.user
    target = user_email or user
    
    if target != user and "System Manager" not in frappe.get_roles(user) and "PG Coordinator" not in frappe.get_roles(user):
        return error_response("Unauthorized", 403)
        
    try:
        data = frappe.get_all("PG Notification Log",
            filters={"recipient_user": target},
            fields=["name", "subject", "notification_type", "sent_timestamp", "delivery_status"],
            order_by="creation desc",
            limit_page_length=50
        )
        return success_response("Notifications fetched", data)
    except Exception as e:
        return error_response(str(e), 500)

@frappe.whitelist(allow_guest=False)
def fetch_document_notifications(doctype, docname):
    if "PG Student" in frappe.get_roles(frappe.session.user):
        return error_response("Unauthorized for generic document notification fetches", 403)
        
    try:
        data = frappe.get_all("PG Notification Log",
            filters={"related_doctype": doctype, "related_document_name": docname},
            fields=["name", "recipient_user", "subject", "sent_timestamp", "delivery_status"]
        )
        return success_response("Document notifications fetched", data)
    except Exception as e:
        return error_response(str(e), 500)

@frappe.whitelist(allow_guest=False)
def resend_notification(notification_name):
    if "PG Coordinator" not in frappe.get_roles(frappe.session.user) and "System Manager" not in frappe.get_roles(frappe.session.user):
         return error_response("Only administrators can resend notifications manually.", 403)
         
    try:
        log = frappe.get_doc("PG Notification Log", notification_name)
        if log.delivery_status != "Sent":
            log.dispatch_email()
            return success_response("Notification resent natively", {"new_status": log.delivery_status})
        return success_response("Already sent successfully", {})
    except Exception as e:
         return error_response(str(e), 500)

# --- REPOSITORY API ---

@frappe.whitelist(allow_guest=False)
def list_student_documents(student_email=None):
    user = frappe.session.user
    target = student_email or user
    if target != user and "PG Student" in frappe.get_roles(user):
         return error_response("Unauthorized", 403)
         
    # Obey internal repository fields safely natively bypassing standard DB logic 
    filters = {"linked_student": target}
    if "PG Student" in frappe.get_roles(user):
        filters["visible_to_student"] = 1
        
    try:
        data = frappe.get_all("PG Document Repository",
            filters=filters,
            fields=["name", "document_title", "document_type", "file_attachment", "uploaded_date"]
        )
        return success_response("Student documents fetched", data)
    except Exception as e:
        return error_response(str(e), 500)

@frappe.whitelist(allow_guest=False)
def fetch_workflow_documents(workflow_doctype, workflow_docname):
    try:
        # Check standard document read access internally via has_permission
        if not frappe.has_permission(workflow_doctype, "read", doc=workflow_docname):
            return error_response("Unauthorized to view parent workflow", 403)
            
        filters = {"source_workflow": workflow_doctype, "active_flag": 1}
        
        user = frappe.session.user
        roles = frappe.get_roles(user)
        if "PG Student" in roles: filters["visible_to_student"] = 1
        if "PG Examiner" in roles: filters["visible_to_examiner"] = 1
        
        data = frappe.get_all("PG Document Repository", filters=filters, fields=["name", "document_title", "document_type", "file_attachment", "uploaded_date"])
        return success_response("Workflow documents fetched", data)
    except Exception as e:
        return error_response(str(e), 500)

@frappe.whitelist(allow_guest=False)
def fetch_visible_documents():
    try:
        # Standard RBAC natively overrides
        data = frappe.get_list("PG Document Repository",
            fields=["name", "document_title", "document_type", "file_attachment", "uploaded_date"]
        )
        return success_response("Visible documents fetched", data)
    except Exception as e:
        return error_response(str(e), 500)
