import tkinter as tk
from tkinter import messagebox
from decimal import Decimal

from src.app.services.accessory_service import (
    AccessoryValidationError,
    AccessoryNotFoundError,
    AccessoryDatabaseError,
    AccessoryServiceException
)

class AccessoryDialog:
    def __init__(self, parent, accessory_service, mode="add", accessory_data=None):
        self.accessory_service = accessory_service
        self.mode = mode
        self.accessory_data = accessory_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Accessory" if mode == "add" else "Edit Accessory")
        self.dialog.geometry("550x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (550 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (450 // 2)
        self.dialog.geometry(f"550x450+{x}+{y}")

        self._create_form()

    def _create_form(self):
        """
        Creates the accessory form UI.

        The form contains input fields for:
        - Accessory name
        - Description
        - Price per day
        """
        title_text = "Add New Accessory" if self.mode == "add" else "Edit Accessory"
        title_frame = tk.Frame(self.dialog, bg="#FF5722", height=50)
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

        tk.Label(form_frame, text="Name *:", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w")
        self.name_entry = tk.Entry(form_frame, width=50, font=("Arial", 10))
        self.name_entry.pack(pady=5, fill="x")

        tk.Label(form_frame, text="Description *:", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w", pady=(10, 0))
        self.desc_entry = tk.Entry(form_frame, width=50, font=("Arial", 10))
        self.desc_entry.pack(pady=5, fill="x")

        tk.Label(form_frame, text="Price per Day *:", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w", pady=(10, 0))

        price_frame = tk.Frame(form_frame, bg="white")
        price_frame.pack(fill="x", pady=5)

        tk.Label(price_frame, text="$", font=("Arial", 12, "bold"), bg="white", fg="black").pack(side="left")
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
            relief="solid",
            borderwidth=1
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
            relief="solid",
            borderwidth=1
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
        if errors:
            messagebox.showerror("Validation Error", "Please fix:\n\n" + "\n".join(errors))
            return

        try:
            try:
                price = Decimal(price_str)
                if price <= 0:
                    messagebox.showerror("Validation Error","Price must be greater than zero")
                    return
            except Exception:
                messagebox.showerror("Validation Error","Price must be a valid number (e.g., 10.50)")
                return

            if self.mode == "add":
                self.accessory_service.create_accessory(name, description, price)
                messagebox.showinfo("Success", "Accessory added successfully!")
            else:
                self.accessory_service.update_accessory(self.accessory_id,name,description,price)
                messagebox.showinfo("Success", "Accessory updated successfully!")

            self.dialog.destroy()

        except AccessoryValidationError as e:
            messagebox.showerror("Validation Error", str(e))

        except AccessoryNotFoundError as e:
            messagebox.showerror("Not Found",f"The accessory could not be found.\n\n{str(e)}\n\nPlease refresh and try again.")
            self.dialog.destroy()

        except AccessoryDatabaseError as e:
            error_msg = str(e)

            if "already exists" in error_msg.lower():
                messagebox.showerror("Duplicate Entry",f"An accessory with this name already exists.\n\nPlease choose a different name.")
            elif "referenced in active rentals" in error_msg.lower():
                messagebox.showerror("Cannot Delete","This accessory is currently being used in rentals and cannot be modified in a way that would break those references.")
            else:
                messagebox.showerror("Database Error",f"A database error occurred:\n\n{error_msg}\n\nPlease try again or contact support.")

        except AccessoryServiceException as e:
            messagebox.showerror("Error",f"An error occurred:\n\n{str(e)}\n\nPlease try again.")
