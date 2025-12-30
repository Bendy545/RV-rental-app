import tkinter as tk
from tkinter import messagebox, ttk
from src.ui.views.accessory.accessory_dialog import AccessoryDialog

class AccessoryView:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services
        self.accessory_service = services["accessory"]

        self._create_ui()
        self._load_accessories()

    def _create_ui(self):
        title = tk.Label(
            self.parent,
            text="Accessory Management",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="black"
        )
        title.pack(pady=20)

        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Accessory",
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
            command=self._load_accessories,
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

        columns = ("ID", "Name", "Description", "Price/Day")

        style = ttk.Style()
        style.theme_use('default')

        style.configure("Treeview",background="white",foreground="black",fieldbackground="white",rowheight=25)

        style.configure("Treeview.Heading",background="#2b2b2b",foreground="white",font=("Arial", 10, "bold"))

        style.map('Treeview',background=[('selected', '#0078d7')],foreground=[('selected', 'white')])

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Accessory Name")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Price/Day", text="Price per Day")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Name", width=200)
        self.tree.column("Description", width=350)
        self.tree.column("Price/Day", width=100, anchor="center")

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
            command=self.delete_accessory,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="solid",
            borderwidth=1
        ).pack(side="left", padx=5)

    def _load_accessories(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            accessories = self.accessory_service.get_all_accessories_with_ids()

            for idx, acc in enumerate(accessories):
                formatted = list(acc)
                formatted[3] = f"${float(acc[3]):.2f}"
                tag = "evenrow" if idx % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=formatted, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading accessories: {str(e)}")

    def show_add_dialog(self):
        dialog = AccessoryDialog(self.parent, self.accessory_service, mode="add")
        self.parent.wait_window(dialog.dialog)
        self._load_accessories()

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an accessory to edit")
            return

        item = self.tree.item(selected[0])
        accessory_data = item["values"]

        dialog = AccessoryDialog(self.parent, self.accessory_service, mode="edit", accessory_data=accessory_data)
        self.parent.wait_window(dialog.dialog)
        self._load_accessories()

    def delete_accessory(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an accessory to delete")
            return

        item = self.tree.item(selected[0])
        acc_id = item["values"][0]
        acc_name = item["values"][1]

        if not messagebox.askyesno("Confirm Delete", f"Delete accessory {acc_name}?"):
            return

        try:
            self.accessory_service.delete_accessory(acc_id)
            messagebox.showinfo("Success", "Accessory deleted successfully")
            self._load_accessories()

        except Exception as e:
            messagebox.showerror("Error", f"Error deleting accessory: {str(e)}")

