import tkinter as tk
from tkinter import messagebox, filedialog, ttk

class ImportView:
    def __init__(self, parent, services):
        self.services = services
        self.import_service = services['import']

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Import Data")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")

        self._create_ui()

    def _create_ui(self):
        """
        Creates UI elements for ImportView
        :return: ImportView UI elements
        """
        title_frame = tk.Frame(self.dialog, bg="#3F51B5", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="Import Data from Files",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="black"
        ).pack(pady=15)

        container = tk.Frame(self.dialog, bg="white")
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        content_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))



        content_frame.bind("<Configure>", on_configure)

        instructions = tk.Label(
            content_frame,
            text="Select the type of data to import and choose a file:",
            font=("Arial", 11),
            bg="white",
            fg="black"
        )
        instructions.pack(pady=(0, 15))

        options_frame = tk.Frame(content_frame, bg="white")
        options_frame.pack(fill="x", pady=10)

        self._create_import_section(
            options_frame,
            "Customers",
            "Import customers from CSV file",
            "CSV Format: name,surname,email,tel",
            self.import_customers,
            "#4CAF50",
            0
        )

        self._create_import_section(
            options_frame,
            "Brands",
            "Import brands from CSV file",
            "CSV Format: name",
            self.import_brands,
            "#2196F3",
            1
        )

        self._create_import_section(
            options_frame,
            "Accessories",
            "Import accessories from JSON file",
            'JSON Format: [{"name":"...", "description":"...", "price_for_day":...}]',
            self.import_accessories,
            "#FF9800",
            2
        )

        self._create_import_section(
            options_frame,
            "RV Types",
            "Import RV types from JSON file",
            'JSON Format: [{"name":"...", "description":"..."}]',
            self.import_rv_types,
            "#9C27B0",
            3
        )

        result_label = tk.Label(
            content_frame,
            text="Import Results:",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="black"
        )
        result_label.pack(anchor="w", pady=(20, 5))

        result_frame = tk.Frame(content_frame)
        result_frame.pack(fill="both", expand=True)

        self.result_text = tk.Text(
            result_frame,
            height=8,
            font=("Courier", 9),
            wrap="word"
        )
        self.result_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(result_frame, command=self.result_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Close",
            command=self.dialog.destroy,
            bg="white",
            fg="black",
            font=("Arial", 10, "bold"),
            padx=30,
            pady=8,
            cursor="hand2",
            relief="flat"
        ).pack()

    def _create_import_section(self, parent, title, description, format_info, command, color, row):
        """
        Creates a single import section with description and action button.

        :param parent: Parent container.
        :param title: Section title.
        :param description: Short description of the import.
        :param format_info: Information about required file format.
        :param command: Function executed when import button is clicked.
        :param color: Button and title accent color.
        :param row: Row index for grid placement.
        """
        section_frame = tk.Frame(parent, bg="white", relief="ridge", borderwidth=1)
        section_frame.grid(row=row, column=0, sticky="ew", pady=5)
        parent.grid_columnconfigure(0, weight=1)

        content = tk.Frame(section_frame, bg="white")
        content.pack(fill="x", padx=15, pady=10)

        tk.Label(
            content,
            text=title,
            font=("Arial", 12, "bold"),
            bg="white",
            fg=color
        ).pack(anchor="w")

        tk.Label(
            content,
            text=description,
            font=("Arial", 9),
            bg="white",
            fg="#666"
        ).pack(anchor="w", pady=(2, 0))

        tk.Label(
            content,
            text=format_info,
            font=("Arial", 8, "italic"),
            bg="white",
            fg="#999"
        ).pack(anchor="w", pady=(2, 5))

        tk.Button(
            content,
            text=f"Select {title} File",
            command=command,
            bg=color,
            fg="white",
            font=("Arial", 9, "bold"),
            padx=10,
            pady=5,
            cursor="hand2",
            relief="flat"
        ).pack(anchor="w")

    def import_customers(self):
        """
        Imports customers from a CSV file.
        """
        filename = filedialog.askopenfilename(
            title="Select Customers CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filename:
            return

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Importing customers...\n")
        self.dialog.update()

        try:
            result = self.import_service.import_customers_from_csv(filename)

            self.result_text.insert(tk.END, f"\n✓ Successfully imported: {result['imported']} customers\n")

            if result['errors']:
                self.result_text.insert(tk.END, f"\n⚠ Errors encountered:\n")
                for error in result['errors']:
                    self.result_text.insert(tk.END, f"  • {error}\n")

            if result['imported'] > 0:
                messagebox.showinfo("Success", f"Imported {result['imported']} customers!")

        except Exception as e:
            self.result_text.insert(tk.END, f"\n✗ Error: {str(e)}\n")
            messagebox.showerror("Import Error", str(e))

    def import_brands(self):
        """
        Imports brands from a CSV file.
        """
        filename = filedialog.askopenfilename(title="Select Brands CSV File",filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

        if not filename:
            return

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Importing brands...\n")
        self.dialog.update()

        try:
            result = self.import_service.import_brands_from_csv(filename)

            self.result_text.insert(tk.END, f"\n✓ Successfully imported: {result['imported']} brands\n")

            if result['errors']:
                self.result_text.insert(tk.END, f"\n⚠ Errors encountered:\n")
                for error in result['errors']:
                    self.result_text.insert(tk.END, f"  • {error}\n")

            if result['imported'] > 0:
                messagebox.showinfo("Success", f"Imported {result['imported']} brands!")

        except Exception as e:
            self.result_text.insert(tk.END, f"\n✗ Error: {str(e)}\n")
            messagebox.showerror("Import Error", str(e))

    def import_accessories(self):
        """
        Imports accessories from a JSON file.
        """
        filename = filedialog.askopenfilename(
            title="Select Accessories JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not filename:
            return

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Importing accessories...\n")
        self.dialog.update()

        try:
            result = self.import_service.import_accessories_from_json(filename)

            self.result_text.insert(tk.END, f"\n✓ Successfully imported: {result['imported']} accessories\n")

            if result['errors']:
                self.result_text.insert(tk.END, f"\n⚠ Errors encountered:\n")
                for error in result['errors']:
                    self.result_text.insert(tk.END, f"  • {error}\n")

            if result['imported'] > 0:
                messagebox.showinfo("Success", f"Imported {result['imported']} accessories!")

        except Exception as e:
            self.result_text.insert(tk.END, f"\n✗ Error: {str(e)}\n")
            messagebox.showerror("Import Error", str(e))

    def import_rv_types(self):
        """
        Imports rv_types from a JSON file.
        """
        filename = filedialog.askopenfilename(
            title="Select RV Types JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not filename:
            return

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Importing RV types...\n")
        self.dialog.update()

        try:
            result = self.import_service.import_rv_types_from_json(filename)

            self.result_text.insert(tk.END, f"\n✓ Successfully imported: {result['imported']} RV types\n")

            if result['errors']:
                self.result_text.insert(tk.END, f"\n⚠ Errors encountered:\n")
                for error in result['errors']:
                    self.result_text.insert(tk.END, f"  • {error}\n")

            if result['imported'] > 0:
                messagebox.showinfo("Success", f"Imported {result['imported']} RV types!")

        except Exception as e:
            self.result_text.insert(tk.END, f"\n✗ Error: {str(e)}\n")
            messagebox.showerror("Import Error", str(e))