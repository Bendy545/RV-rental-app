import tkinter as tk
from tkinter import messagebox

class CustomerDialog:
    def __init__(self, parent, customer_service, mode="add", customer_data=None):
        self.customer_service = customer_service
        self.mode = mode
        self.customer_data = customer_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Customer" if mode == "add" else "Edit Customer")
        self.dialog.geometry("450x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"450x350+{x}+{y}")

        self._create_form()

    def _create_form(self):
        title_text = "Add New Customer" if self.mode == "add" else "Edit Customer"
        title_frame = tk.Frame(self.dialog, bg="#2196F3", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        title = tk.Label(
            title_frame,
            text=title_text,
            font=("Arial", 18, "bold"),
            bg="#2196F3",
            fg="white"
        )
        title.pack(pady=15)

        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(padx=30, pady=20, fill="both", expand=True)

        tk.Label(
            form_frame,
            text="Name *:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(row=0, column=0, sticky="w", pady=10)

        self.name_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.name_entry.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

        tk.Label(
            form_frame,
            text="Surname *:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(row=1, column=0, sticky="w", pady=10)

        self.surname_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.surname_entry.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        tk.Label(
            form_frame,
            text="Email *:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(row=2, column=0, sticky="w", pady=10)

        self.email_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.email_entry.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

        tk.Label(
            form_frame,
            text="Phone *:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).grid(row=3, column=0, sticky="w", pady=10)

        self.tel_entry = tk.Entry(form_frame, width=30, font=("Arial", 10))
        self.tel_entry.grid(row=3, column=1, pady=10, padx=10, sticky="ew")

        form_frame.grid_columnconfigure(1, weight=1)

        if self.mode == "edit" and self.customer_data:
            self.customer_id = self.customer_data[0]
            self.name_entry.insert(0, self.customer_data[1])
            self.surname_entry.insert(0, self.customer_data[2])
            self.email_entry.insert(0, self.customer_data[3])
            self.tel_entry.insert(0, self.customer_data[4])

        note = tk.Label(
            form_frame,
            text="* Required fields",
            font=("Arial", 8, "italic"),
            fg="gray",
            bg="white"
        )
        note.grid(row=4, column=0, columnspan=2, sticky="w", pady=(5, 0))

        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(pady=15)

        save_btn = tk.Button(
            button_frame,
            text="Save",
            command=self.save,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=25,
            pady=8,
            width=12,
            cursor="hand2",
            relief="flat"
        )
        save_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bg="#757575",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=25,
            pady=8,
            width=12,
            cursor="hand2",
            relief="flat"
        )
        cancel_btn.pack(side="left", padx=5)

        self.name_entry.focus()

    def validate_form(self):
        errors = []

        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        email = self.email_entry.get().strip()
        tel = self.tel_entry.get().strip()

        if not name:
            errors.append("Name is required")

        if not surname:
            errors.append("Surname is required")

        if not email:
            errors.append("Email is required")
        elif '@' not in email or '.' not in email:
            errors.append("Invalid email format (must contain @ and .)")

        if not tel:
            errors.append("Phone is required")
        elif len(tel) < 9:
            errors.append("Phone must be at least 9 digits")

        return errors

    def save(self):
        errors = self.validate_form()
        if errors:
            messagebox.showerror("Validation Error", "Please fix the following errors:\n\n" + "\n".join(errors))
            return

        name = self.name_entry.get().strip()
        surname = self.surname_entry.get().strip()
        email = self.email_entry.get().strip()
        tel = self.tel_entry.get().strip()

        try:
            if self.mode == "add":
                self.customer_service.create_customer(name, surname, email, tel)
                messagebox.showinfo("Success", "Customer added successfully!")
            else:
                self.customer_service.update_customer(
                    self.customer_id,
                    name=name,
                    surname=surname,
                    email=email,
                    tel=tel
                )
                messagebox.showinfo("Success", "Customer updated successfully!")

            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")