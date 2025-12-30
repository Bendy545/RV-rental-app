import tkinter as tk
from tkinter import messagebox, ttk
from src.ui.views.rv_type.rv_type_dialog import RvTypeDialog

class RvTypeView:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services
        self.rv_type_service = services['rv_type']

        self._create_ui()
        self._load_rv_types()

    def _create_ui(self):
        title = tk.Label(self.parent, text="Rv Type Management", font=('Arial', 24, "bold"), bg="white")
        title.pack(pady=20)

        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Rv Type",
            command=self.show_add_dialog,
            bg="white",
            fg="black",
            font=('Arial', 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self._load_rv_types,
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

        columns = ("ID", "Name", "Description")

        style = ttk.Style()
        style.theme_use('default')

        style.configure("Treeview",background="white",foreground="black",fieldbackground="white",rowheight=25)

        style.configure("Treeview.Heading",background="#2b2b2b",foreground="white",font=("Arial", 10, "bold"))

        style.map('Treeview',background=[('selected', '#0078d7')],foreground=[('selected', 'white')])

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Type Name")
        self.tree.heading("Description", text="Description")

        self.tree.column("ID", width=80, anchor="center")
        self.tree.column("Name", width=200)
        self.tree.column("Description", width=400)

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
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="Delete Selected",
            command=self.delete_rv_type,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

    def _load_rv_types(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            rv_types = self.rv_type_service.get_all_types_with_ids()

            for idx, rv_type in enumerate(rv_types):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=rv_type, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading RV types: {str(e)}")

    def show_add_dialog(self):
        dialog = RvTypeDialog(self.parent, self.rv_type_service, mode="add")
        self.parent.wait_window(dialog.dialog)
        self._load_rv_types()

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an RV type to edit")
            return

        item = self.tree.item(selected[0])
        rv_type_data = item['values']

        dialog = RvTypeDialog(self.parent, self.rv_type_service, mode="edit", rv_type_data=rv_type_data)
        self.parent.wait_window(dialog.dialog)
        self._load_rv_types()

    def delete_rv_type(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an RV type to delete")
            return

        item = self.tree.item(selected[0])
        type_id = item['values'][0]
        type_name = item['values'][1]

        if not messagebox.askyesno("Confirm Delete", f"Delete RV type {type_name}?"):
            return

        try:
            self.rv_type_service.delete_rv_type(type_id)
            messagebox.showinfo("Success", "RV type successfully deleted")
            self._load_rv_types()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting RV type: {str(e)}")