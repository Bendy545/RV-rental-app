import tkinter as tk
from tkinter import messagebox, ttk
from src.ui.views.rv.rv_dialog import RvDialog

class RvView:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services
        self.rv_service = services["rv"]

        self._create_ui()
        self._load_rvs()

    def _create_ui(self):
        title = tk.Label(
            self.parent,
            text="RV Management",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="black"
        )

        title.pack(pady=20)

        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add RV",
            command=self.show_add_dialog,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self._load_rvs,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self.parent, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "SPZ", "Manufacture Date", "Price/Day", "Brand", "Type")

        style = ttk.Style()
        style.theme_use('default')

        style.configure("Treeview",background="white",foreground="black",fieldbackground="white",rowheight=25)

        style.configure("Treeview.Heading",background="#2b2b2b",foreground="white",font=("Arial", 10, "bold"))

        style.map('Treeview',background=[('selected', '#0078d7')],foreground=[('selected', 'white')])

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

        self.tree.heading("ID", text="ID")
        self.tree.heading("SPZ", text="License Plate")
        self.tree.heading("Manufacture Date", text="Manufacture Date")
        self.tree.heading("Price/Day", text="Price per Day")
        self.tree.heading("Brand", text="Brand")
        self.tree.heading("Type", text="Type")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("SPZ", width=120)
        self.tree.column("Manufacture Date", width=130, anchor="center")
        self.tree.column("Price/Day", width=100, anchor="center")
        self.tree.column("Brand", width=120)
        self.tree.column("Type", width=180)

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
            text="Edit Selected",
            command=self.show_edit_dialog,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="Delete Selected",
            command=self.delete_rv,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

    def _load_rvs(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            rvs = self.rv_service.get_all_rvs_formatted()

            for idx, rv in enumerate(rvs):
                formatted = (
                    rv['id'],
                    rv['spz'],
                    rv['manufacture_date'].strftime('%Y-%m-%d') if hasattr(rv['manufacture_date'], 'strftime') else str(rv['manufacture_date']),
                    f"${rv['price_per_day']:.2f}",
                    rv['brand'],
                    rv['type']
                )
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=formatted, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading RVs: {str(e)}")

    def show_add_dialog(self):
        dialog = RvDialog(self.parent, self.services, mode="add")
        self.parent.wait_window(dialog.dialog)
        self._load_rvs()

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an RV to edit")
            return

        item = self.tree.item(selected[0])
        rv_data = item['values']

        dialog = RvDialog(self.parent, self.services, mode="edit", rv_data=rv_data)
        self.parent.wait_window(dialog.dialog)
        self._load_rvs()

    def delete_rv(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an RV to delete")
            return

        item = self.tree.item(selected[0])
        rv_id = item['values'][0]
        rv_spz = item['values'][1]

        if not messagebox.askyesno("Confirm Delete", f"Delete RV {rv_spz}?"):
            return

        try:
            self.rv_service.delete_rv(rv_id)
            messagebox.showinfo("Success", "RV deleted successfully")
            self._load_rvs()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting RV: {str(e)}")