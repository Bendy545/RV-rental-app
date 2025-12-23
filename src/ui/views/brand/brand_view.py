import tkinter as tk
from tkinter import messagebox, ttk

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
            bg="white"
        )

        title.pack(pady=20)

        # Buttons frame
        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="➕ Add Brand",
            command=self.show_add_dialog,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self._load_brands,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        # Table frame
        table_frame = tk.Frame(self.parent, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Create treeview
        columns = ("ID", "Name")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=20)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Brand Name")

        self.tree.column("ID", width=100, anchor="center")
        self.tree.column("Name", width=400)

        self.tree.tag_configure('oddrow', background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='white')

        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action buttons
        action_frame = tk.Frame(self.parent, bg="white")
        action_frame.pack(pady=10)

        tk.Button(
            action_frame,
            text="✏️ Edit Selected",
            command=self.show_edit_dialog,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            action_frame,
            text="🗑️ Delete Selected",
            command=self.delete_brand,
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

    def _load_brands(self):
        raise NotImplemented

    def show_add_dialog(self):
        raise NotImplemented

    def show_edit_dialog(self):
        raise NotImplemented

    def delete_brand(self):
        raise NotImplemented