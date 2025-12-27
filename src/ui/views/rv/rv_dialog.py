import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
from datetime import datetime

class RvDialog:
    def __init__(self, parent, services, mode="add", rv_data=None):
        self.services = services
        self.rv_service = services['rv']
        self.brand_service = services['brand']
        self.rv_type_service = services['rv_type']
        self.mode = mode
        self.rv_data = rv_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add RV" if mode == "add" else "Edit RV")
        self.dialog.geometry("500x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (450 // 2)
        self.dialog.geometry(f"500x450+{x}+{y}")

        self._create_form()

    def _create_form(self):
        title_text = "Add New RV" if self.mode == "add" else "Edit RV"
        title_frame = tk.Frame(self.dialog, bg="#00BCD4", height=50)
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

        tk.Label(form_frame, text="License Plate (SPZ) *:", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w")
        self.spz_entry = tk.Entry(form_frame, width=50, font=("Arial", 10))
        self.spz_entry.pack(pady=5, fill="x")

        tk.Label(form_frame, text="Manufacture Date * (YYYY-MM-DD):", font=("Arial", 10, "bold"), bg="white", fg="black").pack(
            anchor="w", pady=(10, 0))
        self.date_entry = tk.Entry(form_frame, width=50, font=("Arial", 10))
        self.date_entry.pack(pady=5, fill="x")

        tk.Label(form_frame, text="Price per Day *:", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w",pady=(10, 0))
        price_frame = tk.Frame(form_frame, bg="white")
        price_frame.pack(fill="x", pady=5)
        tk.Label(price_frame, text="$", font=("Arial", 12, "bold"), bg="white").pack(side="left")
        self.price_entry = tk.Entry(price_frame, width=15, font=("Arial", 10))
        self.price_entry.pack(side="left", padx=5)

        tk.Label(form_frame, text="Brand *:", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w", pady=(10, 0))
        self.brand_var = tk.StringVar()
        self.brand_combo = ttk.Combobox(form_frame, textvariable=self.brand_var, state="readonly", font=("Arial", 10))
        self.brand_combo.pack(pady=5, fill="x")

        brands = self.brand_service.get_all_brands_with_ids()
        self.brands_dict = {f"{b[1]}": b[0] for b in brands}  # {name: id}
        self.brand_combo['values'] = list(self.brands_dict.keys())

        tk.Label(form_frame, text="RV Type *:", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w", pady=(10, 0))
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(form_frame, textvariable=self.type_var, state="readonly", font=("Arial", 10))
        self.type_combo.pack(pady=5, fill="x")

        types = self.rv_type_service.get_all_types_with_ids()
        self.types_dict = {f"{t[1]}": t[0] for t in types}  # {name: id}
        self.type_combo['values'] = list(self.types_dict.keys())

        if self.mode == "edit" and self.rv_data:
            self.rv_id = self.rv_data[0]
            self.spz_entry.insert(0, self.rv_data[1])
            self.date_entry.insert(0, self.rv_data[2])
            price_str = str(self.rv_data[3]).replace('$', '')
            self.price_entry.insert(0, price_str)
            self.brand_var.set(self.rv_data[4])
            self.type_var.set(self.rv_data[5])

        tk.Label(form_frame, text="* Required fields", font=("Arial", 8, "italic"), fg="black", bg="white").pack(anchor="w", pady=(10, 0))

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

        self.spz_entry.focus()

    def save(self):
        spz = self.spz_entry.get().strip()
        date_str = self.date_entry.get().strip()
        price_str = self.price_entry.get().strip()
        brand_name = self.brand_var.get()
        type_name = self.type_var.get()

        errors = []
        if not spz:
            errors.append("License plate is required")
        if not date_str:
            errors.append("Manufacture date is required")
        else:
            try:
                manufacture_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                errors.append("• Invalid date format (use YYYY-MM-DD)")
        if not price_str:
            errors.append("• Price is required")
        else:
            try:
                price = float(price_str)
                if price <= 0:
                    errors.append("Price must be positive")
            except ValueError:
                errors.append("Price must be a valid number")
        if not brand_name:
            errors.append("Brand is required")
        if not type_name:
            errors.append("RV type is required")

        if errors:
            messagebox.showerror("Validation Error", "Please fix:\n\n" + "\n".join(errors))
            return

        try:
            manufacture_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            price = Decimal(price_str)
            brand_id = self.brands_dict[brand_name]
            type_id = self.types_dict[type_name]

            if self.mode == "add":
                self.rv_service.create_new_rv(spz, manufacture_date, price, brand_id, type_id)
                messagebox.showinfo("Success", "RV added successfully!")
            else:
                self.rv_service.update_rv(self.rv_id, spz, manufacture_date, price, brand_id, type_id)
                messagebox.showinfo("Success", "RV updated successfully!")

            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
