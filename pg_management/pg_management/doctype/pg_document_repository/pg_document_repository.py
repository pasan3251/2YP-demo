from frappe.model.document import Document
import frappe

class PGDocumentRepository(Document):
    def validate(self):
        # 1. Ensure file integrity
        if not self.file_attachment:
            frappe.throw("A document must invariably have a file attachment connected.")
            
        # 2. Strong Confidentiality Hardening
        if self.confidential_flag:
            self.visible_to_student = 0
            self.visible_to_panel = 0
