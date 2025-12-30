import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.views.rental.rental_dialog import RentalDialog, StatusDialog
from src.ui.views.rental.rental_details_dialog import RentalDetailsDialog

class RentalView:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services
        self.rental_service = services['rental']

        self._create_ui()
        self._load_rentals()

    def _create_ui(self):
        title = tk.Label(
            self.parent,
            text="Rental Management",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="black"
        )
        title.pack(pady=20)

        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Create Rental",
            command=self.show_add_dialog,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self._load_rentals,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self.parent, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "From", "To", "Created", "Price", "Status", "Paid", "Customer", "RV")

        style = ttk.Style()
        style.theme_use('default')

        style.configure("Treeview",background="white",foreground="black",fieldbackground="white",rowheight=25)

        style.configure("Treeview.Heading",background="#2b2b2b",foreground="white",font=("Arial", 10, "bold"))

        style.map('Treeview',background=[('selected', '#0078d7')],foreground=[('selected', 'white')])

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("From", text="Date From")
        self.tree.heading("To", text="Date To")
        self.tree.heading("Created", text="Created")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Paid", text="Paid")
        self.tree.heading("Customer", text="Customer Email")
        self.tree.heading("RV", text="RV (SPZ)")

        self.tree.column("ID", width=0, stretch=False)
        self.tree.column("From", width=100, anchor="center")
        self.tree.column("To", width=100, anchor="center")
        self.tree.column("Created", width=100, anchor="center")
        self.tree.column("Price", width=80, anchor="center")
        self.tree.column("Status", width=80, anchor="center")
        self.tree.column("Paid", width=60, anchor="center")
        self.tree.column("Customer", width=180)
        self.tree.column("RV", width=100)

        self.tree.tag_configure('oddrow', background='#dbdbdb')
        self.tree.tag_configure('evenrow', background='white')

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        action_frame = tk.Frame(self.parent, bg="white")
        action_frame.pack(pady=10)

        tk.Button(
            action_frame,
            text="View Details",
            command=self.view_details,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="Update Status",
            command=self.update_status,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="Mark as Paid",
            command=self.mark_as_paid,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="Delete Selected",
            command=self.delete_rental,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

    def _load_rentals(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            rentals = self.rental_service.get_all_rentals_with_ids()

            for idx, rental in enumerate(rentals):
                formatted = (
                    rental['id'],
                    str(rental['date_from']),
                    str(rental['date_to']),
                    str(rental['creation_date']),
                    f"${rental['price']:.2f}",
                    rental['status'],
                    rental['is_paid'],
                    rental['customer_email'],
                    rental['rv_spz']
                )
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=formatted, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading rentals: {str(e)}")

    def show_add_dialog(self):
        dialog = RentalDialog(self.parent, self.services)
        self.parent.wait_window(dialog.dialog)
        self._load_rentals()

    def view_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a rental to view details")
            return

        item = self.tree.item(selected[0])
        rental_id = item['values'][0]

        RentalDetailsDialog(self.parent, self.rental_service, rental_id)

    def update_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a rental")
            return

        item = self.tree.item(selected[0])
        rental_id = item['values'][0]
        current_status = item['values'][5]

        status_dialog = StatusDialog(self.parent, current_status)
        self.parent.wait_window(status_dialog.dialog)

        if status_dialog.new_status:
            try:
                self.rental_service.update_rental_status(rental_id, status_dialog.new_status)
                messagebox.showinfo("Success", "Status updated successfully")
                self._load_rentals()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", f"Error updating status: {str(e)}")

    def mark_as_paid(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a rental")
            return

        item = self.tree.item(selected[0])
        rental_id = item['values'][0]
        is_paid = item['values'][6]

        if is_paid == "Yes":
            messagebox.showinfo("Info", "This rental is already marked as paid")
            return

        if messagebox.askyesno("Confirm", "Mark this rental as paid?"):
            try:
                self.rental_service.mark_rental_as_paid(rental_id)
                messagebox.showinfo("Success", "Rental marked as paid")
                self._load_rentals()
            except Exception as e:
                messagebox.showerror("Error", f"Error updating payment status: {str(e)}")

    def delete_rental(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a rental")
            return

        item = self.tree.item(selected[0])
        rental_id = item['values'][0]
        customer = item['values'][7]
        rv_spz = item['values'][8]

        if messagebox.askyesno("Confirm Delete", f"Delete rental for {customer} (RV: {rv_spz})?"):
            try:
                self.rental_service.delete_rental(rental_id)
                messagebox.showinfo("Success", "Rental deleted successfully")
                self._load_rentals()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting rental: {str(e)}")