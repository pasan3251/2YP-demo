import frappe

def create_roles():
    roles = [
        {"role_name": "PG Coordinator", "desk_access": 1, "description": "Administrator for Postgraduate Coordinator"},
        {"role_name": "PG Head of Department", "desk_access": 1, "description": "Administrator for Head of Department"},
        {"role_name": "PG Supervisor", "desk_access": 1, "description": "Internal or External Supervisor"},
        {"role_name": "PG Examiner", "desk_access": 1, "description": "Internal or External Examiner"},
        {"role_name": "PG Student", "desk_access": 1, "description": "Candidate or Applicant"}
    ]
    
    for r in roles:
        if not frappe.db.exists("Role", {"role_name": r["role_name"]}):
            doc = frappe.new_doc("Role")
            doc.update(r)
            doc.insert(ignore_permissions=True)
            print(f"Created Role: {r['role_name']}")
        else:
            print(f"Role already exists: {r['role_name']}")
    frappe.db.commit()

