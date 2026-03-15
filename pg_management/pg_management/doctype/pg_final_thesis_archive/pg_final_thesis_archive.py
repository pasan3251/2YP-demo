# Copyright (c) 2024, Department of Computer Engineering and contributors
import frappe
from frappe.model.document import Document

class PGFinalThesisArchive(Document):
    def after_insert(self):
        try:
            student_email = getattr(self, "linked_pg_student_record", None)
            recipients = []
            if student_email:
                recipients.append(student_email)
                
            coordinators = frappe.get_all("Has Role", filters={"role": "PG Coordinator"}, fields=["parent"])
            recipients.extend([u.parent for u in coordinators])
            
            if recipients:
                frappe.sendmail(
                    recipients=recipients,
                    subject=f"Notice: Final Thesis Archived for {self.linked_pg_student_record}",
                    message=f"The final corrected thesis for linkage {self.linked_thesis_submission} has successfully been officially archived within the Post Graduate Registry. Reference number: {self.archive_identifier}.",
                    delayed=False
                )
        except Exception as e:
            frappe.log_error(f"Failed to send Archive notifications: {e}")
            
        try:
            if getattr(self, "linked_thesis_submission", None):
                thesis = frappe.get_doc("PG Thesis Submission", self.linked_thesis_submission)
                reg_id = thesis.student_registration
                record_id = thesis.pg_student_record
                
                if reg_id:
                    frappe.db.set_value("PG Student Registration", reg_id, "enrollment_status", "Examination Completed")
                    
                if record_id:
                    frappe.db.set_value("PG Student Record", record_id, "enrollment_status", "Ready for Graduation")
        except Exception as e:
            frappe.log_error(f"Failed to update Student Lifecycle Status on Archive: {e}")
