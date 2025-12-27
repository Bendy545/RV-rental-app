import tkinter as tk
from tkinter import messagebox, ttk
from src.ui.views.brand.brand_dialog import BrandDialog

class BrandView:
    def __init__(self, parent, services):
        self.parent = parent
        self.services = services
        self.brand_service = services['brand']

        self._create_ui()
        self._load_brands()

    def _create_ui(self):

        title = tk.Label(
            self.parent,
            text="Brand Management",
            font=('Arial', 24, 'bold'),
            bg="white",
            fg="black"
        )

        title.pack(pady=20)

        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Brand",
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
            command=self._load_brands,
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

        columns = ("ID", "Name")

        style = ttk.Style()
        style.theme_use('default')

        style.configure("Treeview",background="white",foreground="black",fieldbackground="white",rowheight=25)

        style.configure("Treeview.Heading",background="#2b2b2b",foreground="white",font=("Arial", 10, "bold"))

        style.map('Treeview',background=[('selected', '#0078d7')],foreground=[('selected', 'white')])

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Brand Name")

        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Name", width=400)

        self.tree.tag_configure('oddrow', background='#dbdbdb')
        self.tree.tag_configure('evenrow', background='white')

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

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
            command=self.delete_brand,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

    def _load_brands(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            brands = self.brand_service.get_all_brands_with_ids()

            for idx, brand in enumerate(brands):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=brand, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading brands: {str(e)}")


    def show_add_dialog(self):
        dialog = BrandDialog(self.parent, self.brand_service, mode="add")
        self.parent.wait_window(dialog.dialog)
        self._load_brands()

    def show_edit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a brand to edit")
            return

        item = self.tree.item(selected[0])
        brand_data = item['values']

        dialog = BrandDialog(self.parent, self.brand_service, mode="edit", brand_data=brand_data)
        self.parent.wait_window(dialog.dialog)
        self._load_brands()

    def delete_brand(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a brand to delete")
            return

        item = self.tree.item(selected[0])
        brand_id = item['values'][0]
        brand_name = item['values'][1]

        if not messagebox.askyesno("Confirm delete", f"Delete brand {brand_name}?"):
            return

        try:
            self.brand_service.delete_brand(brand_id)
            messagebox.showinfo("Success", "Brand deleted successfully")
            self._load_brands()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting brand: {str(e)}")
