import tkinter as tk
from tkinter import ttk, messagebox

class RentalDetailsDialog:
    def __init__(self, parent, rental_service, rental_id):
        self.rental_service = rental_service
        self.rental_id = rental_id

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Rental Details")
        self.dialog.geometry("500x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)

        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (450 // 2)
        self.dialog.geometry(f"500x450+{x}+{y}")

        self._load_and_display()

    def _load_and_display(self):
        try:
            details = self.rental_service.get_rental_details(self.rental_id)

            if not details:
                messagebox.showerror("Error", "Rental not found")
                self.dialog.destroy()
                return

            title_frame = tk.Frame(self.dialog, bg="#9C27B0", height=50)
            title_frame.pack(fill="x")
            title_frame.pack_propagate(False)

            tk.Label(
                title_frame,
                text=f"Rental Details (ID: {self.rental_id})",
                font=("Arial", 14, "bold"),
                bg="#9C27B0",
                fg="white"
            ).pack(pady=12)

            content_frame = tk.Frame(self.dialog, bg="white")
            content_frame.pack(fill="both", expand=True, padx=20, pady=20)

            rental = details['rental']

            info_text = f"""
                Date From:        {rental[0]}
                Date To:          {rental[1]}
                Created:          {rental[2]}
                Price:            ${float(rental[3]):.2f}
                Status:           {rental[4]}
                Paid:             {'Yes' if rental[5] == 1 else 'No'}
                Customer Email:   {rental[6]}
                RV (SPZ):         {rental[7]}
            """

            tk.Label(
                content_frame,
                text=info_text,
                font=("Courier", 10),
                bg="white",
                justify="left"
            ).pack(anchor="w", pady=(0, 15))

            tk.Label(
                content_frame,
                text="Included Accessories:",
                font=("Arial", 11, "bold"),
                bg="white",
                fg="#9C27B0"
            ).pack(anchor="w", pady=(10, 5))

            accessories = details['accessories']

            if accessories:
                acc_frame = tk.Frame(content_frame, relief="groove", borderwidth=2)
                acc_frame.pack(fill="both", expand=True)

                columns = ("Accessory", "Quantity", "Price")
                tree = ttk.Treeview(acc_frame, columns=columns, show="headings", height=6)

                tree.heading("Accessory", text="Accessory Name")
                tree.heading("Quantity", text="Quantity")
                tree.heading("Price", text="Price")

                tree.column("Accessory", width=250)
                tree.column("Quantity", width=80, anchor="center")
                tree.column("Price", width=100, anchor="center")

                for acc in accessories:
                    tree.insert("", "end", values=(
                        acc[0],
                        acc[1],
                        f"${float(acc[2]):.2f}"
                    ))

                tree.pack(fill="both", expand=True)

                total_acc_price = sum(float(acc[2]) for acc in accessories)
                tk.Label(
                    content_frame,
                    text=f"Total Accessories: ${total_acc_price:.2f}",
                    font=("Arial", 9, "bold"),
                    bg="white",
                    fg="#9C27B0"
                ).pack(anchor="e", pady=(5, 0))
            else:
                tk.Label(
                    content_frame,
                    text="No accessories included in this rental",
                    font=("Arial", 9, "italic"),
                    bg="white",
                    fg="gray"
                ).pack(anchor="w")

            button_frame = tk.Frame(self.dialog, bg="white")
            button_frame.pack(pady=15)

            tk.Button(
                button_frame,
                text="Close",
                command=self.dialog.destroy,
                bg="#757575",
                fg="white",
                font=("Arial", 10, "bold"),
                padx=30,
                pady=8,
                cursor="hand2",
                relief="flat"
            ).pack()

        except Exception as e:
            messagebox.showerror("Error", f"Error loading rental details: {str(e)}")
            self.dialog.destroy()