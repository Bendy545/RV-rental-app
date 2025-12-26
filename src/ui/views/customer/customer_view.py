import tkinter as tk
from tkinter import ttk, messagebox
from customer_dialog import CustomerDialog

class CustomerView:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services
        self.customer_service = services['customer']

        self._create_ui()
        self._load_customers()

    def _create_ui(self):
        title = tk.Label(
            self.parent,
            text="Customer Management",
            font=("Arial", 24, "bold"),
            bg="white"
        )
        title.pack(pady=20)

        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)

        add_btn = tk.Button(
            button_frame,
            text="➕ Add Customer",
            command=self.show_add_dialog,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        )
        add_btn.pack(side="left", padx=5)

        refresh_btn = tk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self._load_customers,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        )
        refresh_btn.pack(side="left", padx=5)

        table_frame = tk.Frame(self.parent, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Surname", "Email", "Phone")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Surname", text="Surname")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone", text="Phone")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=150)
        self.tree.column("Surname", width=150)
        self.tree.column("Email", width=250)
        self.tree.column("Phone", width=120)

        self.tree.tag_configure('oddrow', background='#f0f0f0')
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

        edit_btn = tk.Button(
            action_frame,
            text="Edit Selected",
            command=self.show_edit_dialog,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            action_frame,
            text="Delete Selected",
            command=self.delete_customer,
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        )
        delete_btn.pack(side="left", padx=5)

    def _load_customers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            customers = self.customer_service.get_all_customers_with_ids()

            for idx, customer in enumerate(customers):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=customer, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading customers: {str(e)}")

    def show_add_dialog(self):
        dialog = CustomerDialog(self.parent, self.customer_service, mode="add")
        self.parent.wait_window(dialog.dialog)
        self._load_customers()

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a customer to edit")
            return

        item = self.tree.item(selected[0])
        customer_data = item['values']

        dialog = CustomerDialog(
            self.parent,
            self.customer_service,
            mode="edit",
            customer_data=customer_data
        )
        self.parent.wait_window(dialog.dialog)
        self._load_customers()

    def delete_customer(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("No Selection", "Please select a customer to delete")
            return

        item = self.tree.item(selected[0])
        customer_id = item['values'][0]
        customer_name = f"{item['values'][1]} {item['values'][2]}"

        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete customer {customer_name}?"):
            return

        try:
            self.customer_service.delete_customer(customer_id)
            messagebox.showinfo("Success", "Customer deleted successfully")
            self._load_customers()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting customer: {str(e)}")

