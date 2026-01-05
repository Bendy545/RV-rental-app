import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from src.app.services.rental_service import RentalDatabaseError, RentalValidationError

class RentalDialog:
    def __init__(self, parent, services):
        self.services = services
        self.rental_service = services['rental']
        self.customer_service = services['customer']
        self.rv_service = services['rv']

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New Rental")
        self.dialog.geometry("600x700")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"600x700+{x}+{y}")

        self._create_form()

    def _create_form(self):
        """
        Creates rental creation form UI.

        The form allows the user to:
        - Select a customer
        - Select an RV
        - Enter rental start and end dates
        - Select optional accessories and their quantities
        """
        title_frame = tk.Frame(self.dialog, bg="#673AB7", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="Create New Rental",
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black"
        ).pack(pady=12)

        content_frame = tk.Frame(self.dialog, bg="white")
        content_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(content_frame, bg="white")
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg="white")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        form_frame = tk.Frame(scrollable_frame, bg="white")
        form_frame.pack(padx=30, pady=20, fill="both", expand=True)

        tk.Label(form_frame, text="Customer *:", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w")
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(form_frame, textvariable=self.customer_var, state="readonly",font=("Arial", 10), width=60)
        self.customer_combo.pack(pady=5, fill="x")

        customers_full = self.customer_service.get_all_customers_with_ids()

        self.customers_dict = {f"{c[1]} {c[2]} ({c[3]})": c[0] for c in customers_full}
        self.customer_combo['values'] = list(self.customers_dict.keys())

        tk.Label(form_frame, text="RV *:", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w", pady=(10, 0))
        self.rv_var = tk.StringVar()
        self.rv_combo = ttk.Combobox(form_frame, textvariable=self.rv_var, state="readonly", font=("Arial", 10),width=60)
        self.rv_combo.pack(pady=5, fill="x")

        rvs = self.rv_service.get_all_rvs_formatted()
        self.rvs_dict = {f"{rv['spz']} - {rv['brand']} {rv['type']}": rv['id'] for rv in rvs}
        self.rv_combo['values'] = list(self.rvs_dict.keys())

        tk.Label(form_frame, text="Date From * (YYYY-MM-DD):", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w",pady=(10,0))
        self.date_from_entry = tk.Entry(form_frame, font=("Arial", 10), width=63)
        self.date_from_entry.pack(pady=5, fill="x")
        self.date_from_entry.insert(0, date.today().strftime("%Y-%m-%d"))

        tk.Label(form_frame, text="Date To * (YYYY-MM-DD):", font=("Arial", 10, "bold"), bg="white", fg="black").pack(anchor="w",pady=(10, 0))
        self.date_to_entry = tk.Entry(form_frame, font=("Arial", 10), width=63)
        self.date_to_entry.pack(pady=5, fill="x")

        tk.Label(
            form_frame,
            text="Select Accessories (Optional):",
            font=("Arial", 11, "bold"),
            bg="white",
            fg="black"
        ).pack(anchor="w", pady=(15, 5))

        acc_container = tk.Frame(form_frame, relief="groove", borderwidth=2, bg="white")
        acc_container.pack(fill="x", pady=5)

        accessory_service = self.services['accessory']
        accessories = accessory_service.get_all_accessories_with_ids()

        self.accessory_vars = {}
        self.accessory_qty_entries = {}

        if accessories:
            for acc in accessories:
                acc_id = acc[0]
                acc_name = acc[1]
                acc_desc = acc[2]
                acc_price = float(acc[3])

                acc_frame = tk.Frame(acc_container, bg="white")
                acc_frame.pack(fill="x", padx=10, pady=5)

                var = tk.BooleanVar()
                self.accessory_vars[acc_id] = var

                cb = tk.Checkbutton(
                    acc_frame,
                    text=f"{acc_name} - ${acc_price:.2f}/day",
                    variable=var,
                    font=("Arial", 9, "bold"),
                    bg="white"
                )
                cb.pack(side="left")

                tk.Label(
                    acc_frame,
                    text=f"({acc_desc})",
                    font=("Arial", 8, "italic"),
                    fg="black",
                    bg="white"
                ).pack(side="left", padx=(5, 10))

                tk.Label(acc_frame, text="Qty:", font=("Arial", 8), bg="white", fg="black").pack(side="left")
                qty_entry = tk.Entry(acc_frame, width=5, font=("Arial", 9))
                qty_entry.insert(0, "1")
                qty_entry.pack(side="left", padx=5)
                self.accessory_qty_entries[acc_id] = qty_entry
        else:
            tk.Label(
                acc_container,
                text="No accessories available",
                font=("Arial", 9, "italic"),
                fg="black",
                bg="white"
            ).pack(padx=10, pady=10)

        tk.Label(form_frame, text="* Required fields", font=("Arial", 8, "italic"), fg="black", bg="white").pack(anchor="w", pady=(10, 0))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Create Rental",
            command=self.save,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=25,
            pady=8,
            width=12,
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
            width=12,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

    def save(self):
        customer_str = self.customer_var.get()
        rv_str = self.rv_var.get()
        date_from_str = self.date_from_entry.get().strip()
        date_to_str = self.date_to_entry.get().strip()

        errors = []
        if not customer_str:
            errors.append("• Customer is required")
        if not rv_str:
            errors.append("• RV is required")
        if not date_from_str:
            errors.append("• Date from is required")
        else:
            try:
                date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
            except ValueError:
                errors.append("• Invalid date from format")
        if not date_to_str:
            errors.append("• Date to is required")
        else:
            try:
                date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()
            except ValueError:
                errors.append("• Invalid date to format")

        if errors:
            messagebox.showerror("Validation Error", "Please fix:\n\n" + "\n".join(errors))
            return

        try:
            date_from = datetime.strptime(date_from_str, "%Y-%m-%d").date()
            date_to = datetime.strptime(date_to_str, "%Y-%m-%d").date()
            customer_id = self.customers_dict[customer_str]
            rv_id = self.rvs_dict[rv_str]

            accessories_list = []
            for acc_id, var in self.accessory_vars.items():
                if var.get():
                    try:
                        qty = int(self.accessory_qty_entries[acc_id].get())
                        if qty > 0:
                            accessories_list.append({
                                'id_accessory': acc_id,
                                'amount': qty
                            })
                    except ValueError:
                        messagebox.showwarning("Invalid Quantity",f"Invalid quantity for accessory. Using default quantity of 1.")
                        accessories_list.append({'id_accessory': acc_id,'amount': 1})

            rental_id = self.rental_service.create_new_rental(
                date_from=date_from,
                date_to=date_to,
                id_customer=customer_id,
                id_rv=rv_id,
                accessories_list=accessories_list if accessories_list else None
            )

            if accessories_list:
                messagebox.showinfo("Success",f"Rental created successfully with {len(accessories_list)} accessory type(s)!\nRental ID: {rental_id if rental_id else 'N/A'}")
            else:
                messagebox.showinfo("Success",f"Rental created successfully!\nRental ID: {rental_id if rental_id else 'N/A'}")

            self.dialog.destroy()

        except RentalValidationError as e:
            messagebox.showwarning("Validation", str(e))

        except RentalDatabaseError as e:
            messagebox.showerror("Database Rejected", str(e))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create rental: {e}")


class StatusDialog:
    def __init__(self, parent, current_status):
        self.new_status = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Update Rental Status")
        self.dialog.geometry("350x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (450 // 2)
        self.dialog.geometry(f"350x450+{x}+{y}")

        self._create_ui(current_status)

    def _create_ui(self, current_status):
        """
        Creates the rental status selection UI.

        Displays the current rental status and allows the user
        to select a new status from predefined options.
        """
        title_frame = tk.Frame(self.dialog, bg="#FF9800", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="Update Rental Status",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black"
        ).pack(pady=12)

        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(padx=30, pady=20, fill="both", expand=True)

        tk.Label(
            form_frame,
            text=f"Current Status: {current_status}",
            font=("Arial", 10),
            bg="white",
            fg="black"
        ).pack(pady=(0, 15))

        tk.Label(
            form_frame,
            text="Select New Status:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="black"
        ).pack(anchor="w")

        self.status_var = tk.StringVar(value=current_status)
        statuses = ['reserved', 'active', 'finished', 'canceled']

        for status in statuses:
            tk.Radiobutton(
                form_frame,
                text=status.capitalize(),
                variable=self.status_var,
                value=status,
                font=("Arial", 10),
                bg="white"
            ).pack(anchor="w", pady=2)

        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Update",
            command=self.save,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=6,
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
            padx=20,
            pady=6,
            width=10,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

    def save(self):
        """
        Saves the selected rental status.

        Stores the selected status and closes the dialog.
        """
        self.new_status = self.status_var.get()
        self.dialog.destroy()