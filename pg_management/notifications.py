import frappe

def validate_and_send_review_emails(doc, method=None):
    """
    Called on `on_update` document event for `PG Progress Report`.
    Fires off emails triggered by Workflow State changes.
    """
    if doc.is_new():
        return

    # Check if workflow state has dynamically changed in this session
    if not doc.has_value_changed("workflow_state"):
        return

    new_state = doc.get("workflow_state")

    if new_state == "Submitted to Supervisor":
        notify_supervisor(doc)
    elif new_state == "Forwarded to HoD / FHDC":
        notify_hod(doc)
    elif new_state == "Panel Evaluated":
        notify_student_of_completion(doc)


def notify_supervisor(doc):
    student = frappe.get_doc("PG Student Record", doc.student_record)
    
    # Check if student has supervisors assigned in child table
    if not student.supervisors:
        return
        
    supervisor_emails = []
    for sup in student.supervisors:
        # Get user email
        user = frappe.get_value("User", sup.supervisor, "email")
        if user:
            supervisor_emails.append(user)

    if supervisor_emails:
        subject = f"Progress Report Needs Review: {student.student_name}"
        message = f"""
        Dear Supervisor,
        <br><br>
        A {doc.report_type} progress report has been submitted by <b>{student.student_name}</b> 
        ({student.registration_number}) and is pending your review.
        <br><br>
        Please log into the PG Management System to append your feedback and forward the report.
        """
        frappe.sendmail(recipients=supervisor_emails, subject=subject, message=message)

def notify_hod(doc):
    # Find users with 'Head of Department' role
    users = frappe.get_all("Has Role", filters={"role": "Head of Department"}, fields=["parent"])
    hod_emails = []
    
    for u in users:
        email = frappe.get_value("User", u.parent, "email")
        if email:
            hod_emails.append(email)

    if hod_emails:
        subject = f"Progress Report Pending Approval: {doc.student_record}"
        message = f"""
        Dear Head of Department,
        <br><br>
        A {doc.report_type} progress report for {doc.student_record} has been forwarded by their Supervisor
        and requires your evaluation / panel scheduling.
        """
        frappe.sendmail(recipients=hod_emails, subject=subject, message=message)

def notify_student_of_completion(doc):
    student = frappe.get_doc("PG Student Record", doc.student_record)
    if student.email:
        subject = f"Progress Report Evaluated: {doc.report_type}"
        message = f"""
        Dear {student.student_name},
        <br><br>
        Your {doc.report_type} progress report has been fully evaluated by the panel.
        <br><br>
        <b>Panel Recommendation:</b> {doc.panel_recommendation}
        <br><br>
        You can view the full details linked to your student dashboard.
        """
        frappe.sendmail(recipients=[student.email], subject=subject, message=message)
