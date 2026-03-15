import frappe
from frappe.utils import add_days, today, getdate

def check_progress_report_deadlines():
    """
    Scheduled hourly or daily. It evaluates all Active MPhil/PhD students
    and compares `date_of_registration` + terms to current date.
    Sends reminders if Reports are missing.
    """
    current_date = getdate(today())
    
    # Check all active students
    records = frappe.get_all("PG Student Record", 
                             filters={"status": "Active", "enrollment_type": ["in", ["Full Time", "Part Time"]]},
                             fields=["name", "date_of_registration", "email", "student_name", "programme"])
                             
    for rec in records:
        if not rec.date_of_registration:
            continue
            
        days_active = (current_date - getdate(rec.date_of_registration)).days
        
        # 1. Monthly Reminder Logic
        if days_active > 0 and days_active % 30 == 0:
            send_reminder_email(rec, "Monthly")
            
        # 2. Half-Yearly Reminder Logic (Approx 180 days interval)
        if days_active > 0 and days_active % 180 == 0:
             # Check if they have an active pending report
             has_report = frappe.db.exists("PG Progress Report", {"student_record": rec.name, "report_type": "Half-Yearly", "docstatus": ["<", 2]})
             if not has_report:
                 send_reminder_email(rec, "Half-Yearly")
                 
        # 3. Yearly Reminder Logic (Approx 365 days)
        if days_active > 0 and days_active % 365 == 0:
             # Similar checking logic for missing reports
             has_yearly_report = frappe.db.exists("PG Progress Report", {"student_record": rec.name, "report_type": "Yearly", "docstatus": ["<", 2]})
             if not has_yearly_report:
                 send_reminder_email(rec, "Yearly")


def send_reminder_email(student_rec, interval_type):
    """
    Dispatch Frappe email using standard templates
    """
    subject = f"Friendly Reminder: {interval_type} Progress Report Due"
    message = f"""
    Dear {student_rec.student_name},
    <br><br>
    This is an automated notification from the PG Management System.
    Please ensure you submit your {interval_type} progress report into the system on time.
    Your registration type is {student_rec.programme}.
    <br><br>
    Regards,
    PG Coordinator's Office
    """
    try:
        frappe.sendmail(recipients=[student_rec.email], subject=subject, message=message)
    except Exception as e:
        frappe.log_error(f"Failed to send reminder for student {student_rec.name}", "Scheduled Notifications Failure")
