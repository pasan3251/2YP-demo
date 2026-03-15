import frappe
from frappe import _

def validate_applicant(doc, method):
    """
    Hook tied to PG Applicant 'validate' event to secure internal fields.
    """
    # System administrator has full control. If not sys admin:
    if "System Manager" not in frappe.get_roles():
        
        # When applicant modifies their application
        if frappe.session.user == doc.owner:
            
            # If the application is already submitted, lock the document
            if doc.status not in ["Draft", "Application Received"]:
                frappe.throw(_("Applications that are past the draft stage cannot be edited."))
                
            # Prevent tampering with critical metadata internally driven
            if doc.has_value_changed('status') or doc.has_value_changed('decision_date'):
                frappe.throw(_("You cannot modify the Status or Decision Date."), frappe.PermissionError)

def validate_progress_report(doc, method):
    """
    Prevent students from altering Supervisor Feedback or Panel Recommendations.
    """
    # Skip validation for admins and coordinators
    if "System Manager" in frappe.get_roles() or "PG Coordinator" in frappe.get_roles():
        return

    # Skip validation for new documents (creation)
    if doc.is_new():
        return

    # For existing documents owned by the student
    if doc.owner == frappe.session.user:
        if doc.has_value_changed('supervisor_feedback') or doc.has_value_changed('panel_recommendation'):
            frappe.throw(_("You cannot alter Supervisor Feedback or Panel Recommendations."), frappe.PermissionError)

        if doc.status not in ["Draft", "Returned"]:
            frappe.throw(_("Report has already been submitted and is locked for student editing."))
