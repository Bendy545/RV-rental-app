import tkinter as tk
from tkinter import messagebox, ttk

class ReportView:
    def __init__(self, parent, services, report_type):
        self.parent = parent
        self.services = services
        self.report_service = services['report']
        self.report_type = report_type

        self._create_ui()
        self._load_report()

    def _create_ui(self):
        titles = {
            'revenue': "Revenue by Brand Report",
            'customer_stats': "Customer Statistics Report",
            'accessories': "Popular Accessories Report",
            'rv_utilization': "RV Utilization Report"
        }

        title = tk.Label(
            self.parent,
            text=titles.get(self.report_type, "Report"),
            font=("Arial", 24, "bold"),
            bg="white"
        )
        title.pack(pady=20)

        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Refresh",
            command=self._load_report,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        table_frame = tk.Frame(self.parent, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = self._get_columns()
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

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

    def _get_columns(self):
        columns_map = {
            'revenue': ("Brand", "Total Rentals", "Total Revenue", "Avg Price", "Min Price", "Max Price"),
            'customer_stats': ("Customer", "Email", "Phone", "Rentals", "Total Spent", "Avg Days", "Last Rental"),
            'accessories': ("Accessory", "Description", "Times Rented", "Total Qty", "Revenue", "Avg Revenue"),
            'rv_utilization': ("SPZ", "Brand", "Type", "Price/Day", "Rentals", "Days Rented", "Avg Duration", "Revenue")
        }
        return columns_map.get(self.report_type, ("Data",))

    def _load_report(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            if self.report_type == 'revenue':
                data = self.report_service.get_revenue_by_brand_report()
            elif self.report_type == 'customer_stats':
                data = self.report_service.get_customer_statistics_report()
            elif self.report_type == 'accessories':
                data = self.report_service.get_popular_accessories_report()
            elif self.report_type == 'rv_utilization':
                data = self.report_service.get_rv_utilization_report()
            else:
                data = []

            for idx, row in enumerate(data):
                formatted_row = self._format_row(row)
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=formatted_row, tags=(tag,))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading report: {str(e)}")

    def _format_row(self, row):
        formatted = []
        for value in row:
            if value is None:
                formatted.append("N/A")
            elif isinstance(value, float):
                formatted.append(f"{value:.2f}")
            else:
                formatted.append(str(value))
        return formatted