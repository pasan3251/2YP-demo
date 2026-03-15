from frappe.model.document import Document
import frappe
from frappe.utils import getdate, nowdate

class PGAcademicEvent(Document):
    def validate(self):
        if self.event_date and self.due_date and getdate(self.due_date) < getdate(self.event_date):
            frappe.throw("Due Date cannot be before the Event Date.")

        today = getdate(nowdate())

        if self.completed_flag and self.status not in ["Completed", "Cancelled"]:
            self.status = "Completed"
            if not self.completed_date:
                self.completed_date = today

        if not self.status or self.status in ["Scheduled", "Upcoming", "Due Today", "Overdue"]:
            due = getdate(self.due_date) if self.due_date else None
            
            # Auto-cancel irrelevant events for dormant students
            if getattr(self, "linked_pg_student_record", None):
                stu_status = frappe.db.get_value("PG Student Record", self.linked_pg_student_record, "enrollment_status")
                if stu_status in ["Withdrawn", "Cancelled", "Completed", "Alumni"]:
                    self.status = "Cancelled"
                    self.cancel_reason = f"Student is {stu_status}"
            
            if due and self.status not in ["Completed", "Cancelled"]:
                if due < today:
                    self.status = "Overdue"
                elif due == today:
                    self.status = "Due Today"
                else:
                    self.status = "Upcoming"
                    
    def generate_notification(self, notification_type, message_summary):
        try:
            log = frappe.new_doc("PG Notification Log")
            recipient = self.responsible_user or self.linked_student
            if not recipient and self.responsible_role:
                users = frappe.get_all("Has Role", filters={"role": self.responsible_role}, fields=["parent"])
                if users:
                    recipient = users[0].parent
                    
            if not recipient: return
            
            log.recipient_user = recipient
            log.recipient_email = frappe.db.get_value("User", recipient, "email") or recipient
            log.related_event = self.name
            log.notification_type = notification_type
            log.subject = f"{notification_type}: {self.event_title}"
            log.message_summary = message_summary
            log.delivery_channel = "Email"
            log.insert(ignore_permissions=True)
        except Exception as e:
            frappe.log_error(f"Event Notification Error: {e}")
