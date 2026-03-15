import frappe
import json
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

@frappe.whitelist(allow_guest=False)
def get_student_status(registration_number):
    try:
        # Require 'PG Coordinator' or 'PG Head of Department' or 'PG Supervisor' or specific student.
        user = frappe.session.user
        
        if not frappe.db.exists("PG Student Record", registration_number):
            return error_response(_("Student Record Not Found"), 404)
            
        doc = frappe.get_doc("PG Student Record", registration_number)
        
        # Simple security check if student attempts to view another
        if "PG Student" in frappe.get_roles(user) and doc.email != user:
             return error_response(_("Not authorized to view this record"), 403)
        
        return success_response("Student Record Fetched", {
            "student_name": doc.student_name,
            "registration_number": doc.registration_number,
            "programme": doc.programme,
            "status": getattr(doc, "status", None),
            "enrollment_status": doc.enrollment_status
        })
    except Exception as e:
        frappe.log_error(message=str(e), title="API Error: get_student_status")
        return error_response(_("Internal Server Error"), 500)

@frappe.whitelist(allow_guest=True)
def submit_external_application(applicant_data):
    """
    API endpoint for external website to submit applicant data natively.
    """
    try:
        if isinstance(applicant_data, str):
            data = json.loads(applicant_data)
        else:
            data = applicant_data
            
        doc = frappe.get_doc({
            "doctype": "PG Applicant",
            "applicant_name": data.get("applicant_name"),
            "email": data.get("email"),
            "mobile": data.get("mobile"),
            "programme": data.get("programme"),
            "research_topic": data.get("research_topic")
        })
        doc.insert(ignore_permissions=True)
        return success_response(_("Application submitted successfully"), {"applicant_id": doc.name})
    except Exception as e:
        frappe.log_error(message=frappe.get_traceback(), title="External Application Submission Error")
        return error_response(_("Failed to submit application: ") + str(e), 400)
