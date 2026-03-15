from frappe.model.document import Document
import frappe

class PGNotificationLog(Document):
    def after_insert(self):
        self.dispatch_email()
        
    def dispatch_email(self):
        if self.delivery_channel == "Email" and self.recipient_email:
            try:
                frappe.sendmail(
                    recipients=[self.recipient_email],
                    subject=self.subject,
                    message=self.message_summary,
                    delayed=False
                )
                self.db_set("delivery_status", "Sent")
                self.db_set("sent_timestamp", frappe.utils.now())
            except Exception as e:
                self.db_set("delivery_status", "Failed")
                self.db_set("error_details", str(e))
                frappe.log_error(f"Notification Log Mail Failed {self.name}: {e}")
