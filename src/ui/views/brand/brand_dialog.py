import tkinter as tk
from tkinter import messagebox

class BrandDialog:
    def __init__(self, parent, brand_service, mode="add", brand_data=None):
        self.brand_service = brand_service
        self.mode = mode
        self.brand_data = brand_data

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Brand" if mode == "add" else "Edit brand")
        self.dialog.geometry("400x200")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (200 // 2)
        self.dialog.geometry(f"400x200+{x}+{y}")
        self._create_form()

    def _create_form(self):
        title_text = "Add new brand" if self.mode == "add" else "Edit brand"
        title_frame = tk.Frame(self.dialog, bg="#4CAF50", height=50)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text=title_text,
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white"
        ).pack(pady=12)

        form_frame = tk.Frame(self.dialog, bg="white")
        form_frame.pack(padx=30, pady=20, fill="both", expand=True)

        tk.Label(
            form_frame,
            text="Brand name *:",
            font=("Arial", 10, "bold"),
            bg="white"
        ).pack(anchor="w")

        self.name_entry = tk.Entry(form_frame, width=40, font=("Arial", 10))
        self.name_entry.pack(pady=5, fill="x")

        if self.mode == "edit" and self.brand_data:
            self.brand_id = self.brand_data[0]
            self.name_entry.insert(0, self.brand_data[1])

        button_frame = tk.Frame(self.dialog, bg="white")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Save",
            command=self.save,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=25,
            pady=8,
            width=10,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Cancel",
            command=self.dialog.destroy,
            bg="#757575",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=25,
            pady=8,
            width=10,
            cursor="hand2",
            relief="flat"
        ).pack(side="left", padx=5)

        self.name_entry.focus()

    def save(self):
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showerror("Validation Error", "Brand name is required")
            return

        try:
            if self.mode == "add":
                self.brand_service.create_brand(name)
                messagebox.showinfo("Success", "Brand added successfully")

            else:
                self.brand_service.update_brand(self.brand_id, name)
                messagebox.showinfo("Success", "Brand updated successfully")

            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")