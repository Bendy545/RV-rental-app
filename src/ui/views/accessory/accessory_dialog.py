import tkinter as tk
from tkinter import messagebox
from decimal import Decimal

class AccessoryDialog:
    def __init__(self, parent, accessory_service, mode="add", accessory_data=None):
        self.accessory_service = accessory_service
        self.mode = mode
        self.accessory_data = accessory_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Accessory" if mode == "add" else "Edit Accessory")
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
        title_text = "Add New Accessory" if self.mode == "add" else "Edit Accessory"
        title_frame = tk.Frame(self.dialog, bg="#FF5722", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            bg="#FF5722",
            fg="white"
        ).pack(pady=12)

        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(padx=30, pady=20, fill="both", expand=True)

        tk.Label(form_frame, text="Name *:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w")
        self.name_entry = tk.Entry(form_frame, width=50, font=("Arial", 10))
        self.name_entry.pack(pady=5, fill="x")

        tk.Label(form_frame, text="Description *:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(10, 0))
        self.desc_entry = tk.Entry(form_frame, width=50, font=("Arial", 10))
        self.desc_entry.pack(pady=5, fill="x")

        tk.Label(form_frame, text="Price per Day *:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", pady=(10, 0))

        price_frame = tk.Frame(form_frame, bg="white")
        price_frame.pack(fill="x", pady=5)

        tk.Label(price_frame, text="$", font=("Arial", 12, "bold"), bg="white").pack(side="left")
        self.price_entry = tk.Entry(price_frame, width=15, font=("Arial", 10))
        self.price_entry.pack(side="left", padx=5)

        if self.mode == "edit" and self.accessory_data:
            self.accessory_id = self.accessory_data[0]
            self.name_entry.insert(0, self.accessory_data[1])
            self.desc_entry.insert(0, self.accessory_data[2])
            price_str = str(self.accessory_data[3]).replace('$', '')
            self.price_entry.insert(0, price_str)

        tk.Label(
            form_frame,
            text="* Required fields",
            font=("Arial", 8, "italic"),
            fg="gray",
            bg="white"
        ).pack(anchor="w", pady=(10, 0))

        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Save",
            command=self.save,
            bg="#4CAF50",
            fg="white",
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
            bg="#757575",
            fg="white",
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
        price_str = self.price_entry.get().strip()

        errors = []
        if not name:
            errors.append("Name is required")
        if not description:
            errors.append("Description is required")
        if not price_str:
            errors.append("Price is required")
        else:
            try:
                price = float(price_str)
                if price <= 0:
                    errors.append("Price must be positive")
            except ValueError:
                errors.append("Price must be a valid number")

        if errors:
            messagebox.showerror("Validation Error", "Please fix:\n\n" + "\n".join(errors))
            return

        try:
            price = Decimal(price_str)

            if self.mode == "add":
                self.accessory_service.create_accessory(name, description, price)
                messagebox.showinfo("Success", "Accessory added successfully")
            else:
                self.accessory_service.update_accessory(self.accessory_id, name, description, price)
                messagebox.showinfo("Success", "Accessory updated successfully")

            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")