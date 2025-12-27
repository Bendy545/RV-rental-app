import tkinter as tk
from tkinter import messagebox


class RvTypeDialog:
    def __init__(self, parent, rv_type_service, mode="add", rv_type_data=None):
        self.rv_type_service = rv_type_service
        self.mode = mode
        self.rv_type_data = rv_type_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add RV Type" if mode == "add" else "Edit RV Type")
        self.dialog.geometry("450x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"450x300+{x}+{y}")

        self._create_form()

    def _create_form(self):
        title_text = "Add new RV Type" if self.mode == "add" else "Edit RV Type"
        title_frame = tk.Frame(self.dialog, bg="#9C27B0", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black"
        ).pack(pady=12)

        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(padx=30, pady=20, fill="both", expand=True)

        tk.Label(
            form_frame,
            text="Type Name *:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="black"
        ).pack(anchor="w")

        self.name_entry = tk.Entry(form_frame, width=50, font=("Arial", 10))
        self.name_entry.pack(pady=5, fill="x")

        tk.Label(
            form_frame,
            text="Description *:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="black"
        ).pack(anchor="w", pady=(10, 0))

        self.desc_entry = tk.Entry(form_frame, width=50, font=("Arial", 10))
        self.desc_entry.pack(pady=5, fill="x")

        if self.mode == "edit" and self.rv_type_data:
            self.type_id = self.rv_type_data[0]
            self.name_entry.insert(0, self.rv_type_data[1])
            self.desc_entry.insert(0, self.rv_type_data[2])

        tk.Label(
            form_frame,
            text="* Required fields",
            font=("Arial", 8, "italic"),
            fg="black",
            bg="white"
        ).pack(anchor="w", pady=(10, 0))

        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Save",
            command=self.save,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=25,
            pady=8,
            width=10,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=25,
            pady=8,
            width=10,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        self.name_entry.focus()

    def save(self):
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()

        errors = []
        if not name:
            errors.append("Name is required")
        if not description:
            errors.append("Description is required")

        if errors:
            messagebox.showerror("Validation error", "Please fix: \n\n" + "\n".join(errors))
            return

        try:
            if self.mode == "add":
                self.rv_type_service.create_rv_type(name, description)
                messagebox.showinfo("Success", "RV type added successfully")
            else:
                self.rv_type_service.update_rv_type(self.type_id, name, description)
                messagebox.showinfo("Success", "RV type updated successfully")

            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")