import tkinter as tk
from tkinter import messagebox

class MainWindow:
    def __init__(self, services):
        self.services = services

        self.root = tk.Tk()
        self.root.title("RV Rental Management System")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        self._create_menu()
        self._create_main_layout()

        self.show_dashboard()

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Data", command=self.show_import_window)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Manage", menu=manage_menu)
        manage_menu.add_command(label="Rentals", command=self.show_rentals)
        manage_menu.add_command(label="RVs", command=self.show_rvs)
        manage_menu.add_command(label="Customers", command=self.show_customers)
        manage_menu.add_command(label="Brands", command=self.show_brands)
        manage_menu.add_command(label="RV Types", command=self.show_rv_types)
        manage_menu.add_command(label="Accessories", command=self.show_accessories)

        reports_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Reports", menu=reports_menu)
        reports_menu.add_command(label="Revenue by Brand", command=self.show_revenue_report)
        reports_menu.add_command(label="Customer Statistics", command=self.show_customer_stats)
        reports_menu.add_command(label="Popular Accessories", command=self.show_accessories_report)
        reports_menu.add_command(label="RV Utilization", command=self.show_rv_utilization)

    def _create_main_layout(self):
        self.sidebar = tk.Frame(self.root, width=200, bg="#2b2b2b")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        title = tk.Label(
            self.sidebar,
            text="RV Rental\nSystem",
            font=("Arial", 20, "bold"),
            bg="#2b2b2b",
            fg="white",
            pady=20
        )
        title.pack()

        nav_buttons = [
            ("Dashboard", self.show_dashboard),
            ("Rentals", self.show_rentals),
            ("RVs", self.show_rvs),
            ("Customers", self.show_customers),
            ("Brands", self.show_brands),
            ("RV Types", self.show_rv_types),
            ("Accessories", self.show_accessories),
            ("Reports", self.show_revenue_report),
        ]

        for text, command in nav_buttons:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                width=18,
                height=2,
                font=("Arial", 10),
                bg="white",
                fg="black",
                relief="flat",
                cursor="hand2",
                activebackground="#505050",
                activeforeground="white"
            )
            btn.pack(pady=3, padx=10)

        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_content()

        title = tk.Label(
            self.content_frame,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            bg="white",
            fg="black"
        )
        title.pack(pady=20)

        stats_frame = tk.Frame(self.content_frame, bg="white")
        stats_frame.pack(fill="both", expand=True, padx=20, pady=20)

        try:
            rentals = self.services['rental'].get_all_rentals_formatted()
            rvs = self.services['rv'].get_all_rvs_formatted()
            customers = self.services['customer'].get_all_customers()

            active_rentals = len([r for r in rentals if r['status'] == 'active'])

            stats = [
                ("Total RVs", len(rvs), "#4CAF50"),
                ("Total Customers", len(customers), "#2196F3"),
                ("Active Rentals", active_rentals, "#FF9800"),
                ("Total Rentals", len(rentals), "#9C27B0"),
            ]

            for i, (label, value, color) in enumerate(stats):
                self._create_stat_card(stats_frame, label, value, color, i)

        except Exception as e:
            messagebox.showerror("Error", f"Error loading dashboard: {str(e)}")

    def _create_stat_card(self, parent, label, value, color, position):
        row = position // 2
        col = position % 2

        card = tk.Frame(parent, relief="raised", borderwidth=2, bg=color, width=250, height=150)
        card.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")
        card.pack_propagate(False)

        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)

        value_label = tk.Label(card, text=str(value), font=("Arial", 48, "bold"), bg=color, fg="white")
        value_label.pack(pady=(30, 5))

        text_label = tk.Label(card, text=label, font=("Arial", 14), bg=color, fg="white")
        text_label.pack()

    def show_rentals(self):
        from src.ui.views.rental.rental_view import RentalView
        self.clear_content()
        RentalView(self.content_frame, self.services)

    def show_rvs(self):
        from src.ui.views.rv.rv_view import RvView
        self.clear_content()
        RvView(self.content_frame, self.services)

    def show_customers(self):
        from src.ui.views.customer.customer_view import CustomerView
        self.clear_content()
        CustomerView(self.content_frame, self.services)

    def show_brands(self):
        from src.ui.views.brand.brand_view import BrandView
        self.clear_content()
        BrandView(self.content_frame, self.services)

    def show_rv_types(self):
        from src.ui.views.rv_type.rv_type_view import RvTypeView
        self.clear_content()
        RvTypeView(self.content_frame, self.services)

    def show_accessories(self):
        from src.ui.views.accessory.accessory_view import AccessoryView
        self.clear_content()
        AccessoryView(self.content_frame, self.services)

    def show_revenue_report(self):
        from src.ui.views.report.report_view import ReportView
        self.clear_content()
        ReportView(self.content_frame, self.services, 'revenue')

    def show_customer_stats(self):
        from src.ui.views.report.report_view import ReportView
        self.clear_content()
        ReportView(self.content_frame, self.services, 'customer_stats')

    def show_accessories_report(self):
        from src.ui.views.report.report_view import ReportView
        self.clear_content()
        ReportView(self.content_frame, self.services, 'accessories')

    def show_rv_utilization(self):
        from src.ui.views.report.report_view import ReportView
        self.clear_content()
        ReportView(self.content_frame, self.services, 'rv_utilization')

    def show_import_window(self):
        from src.ui.views.import_view import ImportView
        ImportView(self.root, self.services)

    def run(self):
        self.root.mainloop()


def create_application(services):
    return MainWindow(services)