import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import os

class MedicalStoreManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Store Management System")
        self.root.geometry("500x500")

        # Create database connection
        self.conn = sqlite3.connect("medical_store_db.db")
        self.cursor = self.conn.cursor()

        # Create tables if they don't exist
        self.create_tables()

        # Create home window
        self.home_window = tk.Frame(self.root, bg="lightgray")
        self.home_window.pack(fill="both", expand=True)

        # Create store name label and entry
        tk.Label(self.home_window, text="Enter Store Name:", bg="lightgray").pack(side="top")
        self.store_name_entry = tk.Entry(self.home_window, width=40)
        self.store_name_entry.pack(side="top")

        # Create add store button
        tk.Button(self.home_window, text="Add Store", command=self.add_store).pack(side="top")

        # Create store list label and listbox
        tk.Label(self.home_window, text="Store List:", bg="lightgray").pack(side="top")
        self.store_list = tk.Listbox(self.home_window, width=40)
        self.store_list.pack(side="top", fill="both", expand=True)

        # Create button frame
        self.button_frame = tk.Frame(self.root, bg="lightgray")
        self.button_frame.pack(side="bottom", fill="x")

        # Create buttons
        self.add_medicine_button = tk.Button(self.button_frame, text="Add Medicine", command=self.add_medicine_window, state="disabled")
        self.add_medicine_button.pack(side="left")

        self.search_medicine_button = tk.Button(self.button_frame, text="Search Medicine", command=self.search_medicine_window, state="disabled")
        self.search_medicine_button.pack(side="left")

        self.make_bill_button = tk.Button(self.button_frame, text="Make Bill", command=self.make_bill_window, state="disabled")
        self.make_bill_button.pack(side="left")

        self.store_details_button = tk.Button(self.button_frame, text="Store Details", command=self.store_details_window, state="disabled")
        self.store_details_button.pack(side="left")

        self.modify_medicine_button = tk.Button(self.button_frame, text="Modify Medicine", command=self.modify_medicine_window, state="disabled")
        self.modify_medicine_button.pack(side="left")

        self.bill_history_button = tk.Button(self.button_frame, text="Bill History", command=self.bill_history_window, state="disabled")
        self.bill_history_button.pack(side="left")

        # Update store listbox
        self.update_store_listbox()

    def create_tables(self):
        # Create table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stores (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY,
                name TEXT,
                quantity INTEGER,
                price REAL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INTEGER PRIMARY KEY,
                customer_name TEXT,
                age INTEGER,
                gender TEXT,
                mobile TEXT,
                address TEXT,
                doctor_name TEXT,
                hospital_name TEXT,
                total_cost REAL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bill_items (
                id INTEGER PRIMARY KEY,
                bill_id INTEGER,
                medicine_name TEXT,
                quantity INTEGER,
                dose TEXT,
                cost REAL,
                FOREIGN KEY (bill_id) REFERENCES bills (id)
            )
        """)
        self.conn.commit()
        # self.cursor.execute("SELECT * FROM stores")
        # store = self.cursor.fetchone()
        #
        # if store:
        #     # Store already exists, disable store name entry and add store button
        #     self.store_name_entry.config(state="disabled")
        #     self.add_store_button.config(state="disabled")
        #
        #     # Enable buttons
        #     self.add_medicine_button.config(state="normal")
        #     self.search_medicine_button.config(state="normal")
        #     self.make_bill_button.config(state="normal")
        #     self.store_details_button.config(state="normal")
        #     self.modify_medicine_button.config(state="normal")
        #     self.bill_history_button.config(state="normal")
        # else:
        #     # Store doesn't exist, enable store name entry and add store button
        #     self.store_name_entry.config(state="normal")
        #     self.add_store_button.config(state="normal")
        #
        #     # Disable buttons
        #     self.add_medicine_button.config(state="disabled")
        #     self.search_medicine_button.config(state="disabled")
        #     self.make_bill_button.config(state="disabled")
        #     self.store_details_button.config(state="disabled")
        #     self.modify_medicine_button.config(state="disabled")
        #     self.bill_history_button.config(state="disabled")

    def add_store(self):
        store_name = self.store_name_entry.get()

        if store_name:
            self.cursor.execute("SELECT * FROM stores WHERE name = ?", (store_name,))
            store = self.cursor.fetchone()

            if store:
                messagebox.showinfo("Error", "Store already exists!")
            else:
                self.cursor.execute("INSERT INTO stores (name) VALUES (?)", (store_name,))
                self.conn.commit()
                messagebox.showinfo("Success", "Store added successfully!")
                self.store_list.insert("end", store_name)
                self.store_name_entry.delete(0, "end")

                # Enable buttons
                self.add_medicine_button.config(state="normal")
                self.search_medicine_button.config(state="normal")
                self.make_bill_button.config(state="normal")
                self.store_details_button.config(state="normal")
                self.modify_medicine_button.config(state="normal")
        elif not store_name:
            messagebox.showinfo("Success", "Store added successfully!")
            self.store_name_entry.delete(0, "end")

            # Enable buttons
            self.add_medicine_button.config(state="normal")
            self.search_medicine_button.config(state="normal")
            self.make_bill_button.config(state="normal")
            self.store_details_button.config(state="normal")
            self.modify_medicine_button.config(state="normal")
            self.bill_history_button.config(state="normal")
        else:
            messagebox.showerror("Error", "Please enter a store name!")

    def bill_history_window(self):
        self.bill_history_window = tk.Toplevel(self.root)
        self.bill_history_window.title("Bill History")

        # Create bill history listbox
        self.bill_history_listbox = tk.Listbox(self.bill_history_window, width=40)
        self.bill_history_listbox.pack(side="top", fill="both", expand=True)

        # Fetch bill history from database
        self.cursor.execute("SELECT * FROM bills")
        bills = self.cursor.fetchall()

        for bill in bills:
            self.bill_history_listbox.insert("end",f"Bill ID: {bill[0]}, Customer Name: {bill[1]}, Total Cost: {bill[8]}")

    def store_details_window(self):
        # Create store details window
        self.store_details_window = tk.Toplevel(self.root)
        self.store_details_window.title("Store Details")

        # Create store details label
        tk.Label(self.store_details_window, text="Store Details:", font=("Helvetica", 14, "bold")).pack(side="top")

        # Create store details frame
        self.store_details_frame = tk.Frame(self.store_details_window)
        self.store_details_frame.pack(side="top")

        # Create store details labels
        tk.Label(self.store_details_frame, text="Store Name:", font=("Helvetica", 12)).pack(side="left")
        self.store_details_name_label = tk.Label(self.store_details_frame, text="Roshan Medical Store",
                                                 font=("Helvetica", 14, "bold"))
        self.store_details_name_label.pack(side="left")

        tk.Label(self.store_details_frame, text="Medicines:", font=("Helvetica", 12)).pack(side="left")
        self.store_details_medicines_label = tk.Label(self.store_details_frame, text="")
        self.store_details_medicines_label.pack(side="left")

        # Get store details
        store_name = self.store_list.get(tk.ANCHOR)

        if store_name:
            self.cursor.execute("SELECT * FROM stores WHERE name =?", (store_name,))
            store = self.cursor.fetchone()

            if store:
                self.store_details_name_label.config(text=store[1])
                self.cursor.execute("SELECT name FROM medicines")
                medicines = self.cursor.fetchall()
                medicine_names = ", ".join([m[0] for m in medicines])
                self.store_details_medicines_label.config(text=medicine_names)
            else:
                messagebox.showerror("Error", "Store not found!")
        else:
            messagebox.showerror("Error", "Please select a store from the list!")
    def update_store_listbox(self):
        self.store_list.delete(0, "end")
        self.cursor.execute("SELECT name FROM stores")
        stores = self.cursor.fetchall()
        for store in stores:
            self.store_list.insert("end", store[0])

    def add_medicine_window(self):
        # Create add medicine window
        self.add_medicine_window = tk.Toplevel(self.root)
        self.add_medicine_window.title("Add Medicine")

        # Create medicine details frame
        self.medicine_details_frame = tk.Frame(self.add_medicine_window)
        self.medicine_details_frame.pack(side="top")

        # Create medicine details labels and entries
        tk.Label(self.medicine_details_frame, text="Medicine Name:").pack(side="left")
        self.medicine_name_entry = tk.Entry(self.medicine_details_frame, width=20)
        self.medicine_name_entry.pack(side="left")

        tk.Label(self.medicine_details_frame, text="Quantity:").pack(side="left")
        self.quantity_entry = tk.Entry(self.medicine_details_frame, width=20)
        self.quantity_entry.pack(side="left")

        tk.Label(self.medicine_details_frame, text="Price:").pack(side="left")
        self.price_entry = tk.Entry(self.medicine_details_frame, width=20)
        self.price_entry.pack(side="left")

        # Create add medicine button
        tk.Button(self.medicine_details_frame, text="Add Medicine", command=self.add_medicine).pack(side="left")

    def add_medicine(self):
        medicine_name = self.medicine_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if medicine_name and quantity and price:
            try:
                quantity = int(quantity)
                price = float(price)
                self.cursor.execute("INSERT INTO medicines (name, quantity, price) VALUES (?,?,?)", (medicine_name, quantity, price))
                self.conn.commit()
                messagebox.showinfo("Success", "Medicine added successfully!")
                self.medicine_name_entry.delete(0, "end")
                self.quantity_entry.delete(0, "end")
                self.price_entry.delete(0, "end")
            except ValueError:
                messagebox.showerror("Error", "Quantity and Price must be numbers!")
        else:
            messagebox.showerror("Error", "Please fill in all medicine information fields!")

    def search_medicine_window(self):
        # Create search medicine window
        self.search_medicine_window = tk.Toplevel(self.root)
        self.search_medicine_window.title("Search Medicine")

        # Create medicine name label and entry
        tk.Label(self.search_medicine_window, text="Enter Medicine Name:").pack(side="top")
        self.search_medicine_entry = tk.Entry(self.search_medicine_window, width=40)
        self.search_medicine_entry.pack(side="top")

        # Create search button
        tk.Button(self.search_medicine_window, text="Search", command=self.search_medicine).pack(side="top")

        # Create search results frame
        self.search_results_frame = tk.Frame(self.search_medicine_window)
        self.search_results_frame.pack(side="top")

        # Create search results labels
        tk.Label(self.search_results_frame, text="Medicine Name:").pack(side="left")
        self.search_results_name_label = tk.Label(self.search_results_frame, text="")
        self.search_results_name_label.pack(side="left")

        tk.Label(self.search_results_frame, text="Quantity:").pack(side="left")
        self.search_results_quantity_label = tk.Label(self.search_results_frame, text="")
        self.search_results_quantity_label.pack(side="left")

        tk.Label(self.search_results_frame, text="Price:").pack(side="left")
        self.search_results_price_label = tk.Label(self.search_results_frame, text="")
        self.search_results_price_label.pack(side="left")

    def search_medicine(self):
        medicine_name = self.search_medicine_entry.get()

        if medicine_name:
            self.cursor.execute("SELECT * FROM medicines WHERE name = ?", (medicine_name,))
            medicine = self.cursor.fetchone()

            if medicine:
                self.search_results_name_label.config(text=medicine[1])
                self.search_results_quantity_label.config(text=medicine[2])
                self.search_results_price_label.config(text=medicine[3])
            else:
                messagebox.showinfo("Not Found", "Medicine not found!")
        else:
            messagebox.showerror("Error", "Please enter a medicine name!")

    def make_bill_window(self):
        # Create make bill window
        self.make_bill_window = tk.Toplevel(self.root)
        self.make_bill_window.title("Make Bill")

        # Create customer details frame
        self.customer_details_frame = tk.Frame(self.make_bill_window)
        self.customer_details_frame.pack(side="top")

        # Create customer details labels and entries
        tk.Label(self.customer_details_frame, text="Customer Name:").pack(side="left")
        self.customer_name_entry = tk.Entry(self.customer_details_frame, width=20)
        self.customer_name_entry.pack(side="left")

        tk.Label(self.customer_details_frame, text="Age:").pack(side="left")
        self.age_entry = tk.Entry(self.customer_details_frame, width=20)
        self.age_entry.pack(side="left")

        tk.Label(self.customer_details_frame, text="Gender:").pack(side="left")
        self.gender_entry = tk.Entry(self.customer_details_frame, width=20)
        self.gender_entry.pack(side="left")

        tk.Label(self.customer_details_frame, text="Mobile:").pack(side="left")
        self.mobile_entry = tk.Entry(self.customer_details_frame, width=20)
        self.mobile_entry.pack(side="left")

        tk.Label(self.customer_details_frame, text="Address:").pack(side="left")
        self.address_entry = tk.Entry(self.customer_details_frame, width=20)
        self.address_entry.pack(side="left")

        tk.Label(self.customer_details_frame, text="Doctor Name:").pack(side="left")
        self.doctor_name_entry = tk.Entry(self.customer_details_frame, width=20)
        self.doctor_name_entry.pack(side="left")

        tk.Label(self.customer_details_frame, text="Hospital Name:").pack(side="left")
        self.hospital_name_entry = tk.Entry(self.customer_details_frame, width=20)
        self.hospital_name_entry.pack(side="left")

        # Create bill items frame
        self.bill_items_frame = tk.Frame(self.make_bill_window)
        self.bill_items_frame.pack(side="top")

        # Create bill items labels and entries
        tk.Label(self.bill_items_frame, text="Medicine Name:").pack(side="left")
        self.medicine_name_entry = tk.Entry(self.bill_items_frame, width=20)
        self.medicine_name_entry.pack(side="left")

        tk.Label(self.bill_items_frame, text="Quantity:").pack(side="left")
        self.quantity_entry = tk.Entry(self.bill_items_frame, width=20)
        self.quantity_entry.pack(side="left")

        tk.Label(self.bill_items_frame, text="Dose:").pack(side="left")
        self.dose_entry = tk.Entry(self.bill_items_frame, width=20)
        self.dose_entry.pack(side="left")

        tk.Label(self.bill_items_frame, text="Cost:").pack(side="left")
        self.cost_entry = tk.Entry(self.bill_items_frame, width=20)
        self.cost_entry.pack(side="left")

        # Create add bill item button
        tk.Button(self.bill_items_frame, text="Add Bill Item", command=self.add_bill_item).pack(side="left")

        # Create bill items listbox
        self.bill_items_listbox = tk.Listbox(self.make_bill_window, width=40)
        self.bill_items_listbox.pack(side="top", fill="both", expand=True)

        # Create total cost label and entry
        tk.Label(self.make_bill_window, text="Total Cost:").pack(side="top")
        self.total_cost_entry = tk.Entry(self.make_bill_window, width=20)
        self.total_cost_entry.pack(side="top")

        # Create make bill button
        tk.Button(self.make_bill_window, text="Make Bill", command=self.make_bill).pack(side="top")

        # Create print bill button
        tk.Button(self.make_bill_window, text="Print Bill", command=self.print_bill).pack(side="top")

        # Create download bill button
        tk.Button(self.make_bill_window, text="Download Bill", command=self.download_bill).pack(side="top")

    def add_bill_item(self):
        medicine_name = self.medicine_name_entry.get()
        quantity = self.quantity_entry.get()
        dose = self.dose_entry.get()
        cost = self.cost_entry.get()

        if medicine_name and quantity and dose and cost:
            try:
                quantity = int(quantity)
                cost = float(cost)
                self.bill_items_listbox.insert("end", f"{medicine_name} - {quantity} - {dose} - {cost}")
                self.medicine_name_entry.delete(0, "end")
                self.quantity_entry.delete(0, "end")
                self.dose_entry.delete(0, "end")
                self.cost_entry.delete(0, "end")
            except ValueError:
                messagebox.showerror("Error", "Quantity and Cost must be numbers!")
        else:
            messagebox.showerror("Error", "Please fill in all bill item information fields!")

    def make_bill(self):
        customer_name = self.customer_name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        mobile = self.mobile_entry.get()
        address = self.address_entry.get()
        doctor_name = self.doctor_name_entry.get()
        hospital_name = self.hospital_name_entry.get()

        total_cost = 0
        for item in self.bill_items_listbox.get(0, "end"):
            _, _, _, cost = item.split(" - ")
            total_cost += float(cost)

        if customer_name and age and gender and mobile and address and doctor_name and hospital_name:
            try:
                age = int(age)
                self.cursor.execute(
                    "INSERT INTO bills (customer_name, age, gender, mobile, address, doctor_name, hospital_name, total_cost) VALUES (?,?,?,?,?,?,?,?)",
                    (customer_name, age, gender, mobile, address, doctor_name, hospital_name, total_cost))
                self.conn.commit()
                messagebox.showinfo("Success", "Bill made successfully!")
                self.make_bill_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Age must be a number!")
        else:
            messagebox.showerror("Error", "Please fill in all customer details fields!")

        self.bill_id = self.cursor.lastrowid

        # Save bill items to database
        for item in self.bill_items_listbox.get(0, "end"):
            # Split the item string into its components
            medicine_name, quantity, dose, cost = item.split(" - ")
            self.cursor.execute(
                "INSERT INTO bill_items (bill_id, medicine_name, quantity, dose, cost) VALUES (?,?,?,?,?)",
                (self.bill_id, medicine_name, int(quantity), dose, float(cost))
            )
        self.conn.commit()

        messagebox.showinfo("Success", "Bill made successfully!")
        self.make_bill_window.destroy()

    def print_bill(self):
        bill_details = self.get_bill_details()
        bill_items = self.get_bill_items()

        # Generate bill string
        bill_string = self.generate_bill_string(bill_details, bill_items)

        # Open a new window for the bill
        bill_window = tk.Toplevel(self.root)
        bill_window.title("Bill")
        bill_window.geometry("500x500")

        # Create a text widget to display the bill
        bill_text = tk.Text(bill_window, wrap=tk.WORD)
        bill_text.pack(fill="both", expand=True)
        bill_text.insert(tk.END, bill_string)
        bill_text.config(state="disabled")

        # Allow printing using the OS's default printer
        try:
            bill_window.update()
            os.startfile(bill_text, "print")
        except:
            messagebox.showerror("Error", "Failed to print bill!")

    def download_bill(self):
        bill_details = self.get_bill_details()
        bill_items = self.get_bill_items()

        # Generate bill string
        bill_string = self.generate_bill_string(bill_details, bill_items)

        # Save bill to a text file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        bill_filename = f"bill_{timestamp}.txt"
        with open(bill_filename, "w") as f:
            f.write(bill_string)

        messagebox.showinfo("Success", f"Bill downloaded as '{bill_filename}'!")

    def get_bill_details(self):
        customer_name = self.customer_name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        mobile = self.mobile_entry.get()
        address = self.address_entry.get()
        doctor_name = self.doctor_name_entry.get()
        hospital_name = self.hospital_name_entry.get()
        return {
            "customer_name": customer_name,
            "age": age,
            "gender": gender,
            "mobile": mobile,
            "address": address,
            "doctor_name": doctor_name,
            "hospital_name": hospital_name,
        }

    def generate_bill_string(self, bill_details, bill_items):
        # ... (Generate the formatted bill string here) ...

        # Example:
        bill_string = f"""
           ========================================================
           Medical Store Management System
           --------------------------------------------------------
           Date: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
           --------------------------------------------------------
           Customer Name: {bill_details["customer_name"]}
           Age: {bill_details["age"]}
           Gender: {bill_details["gender"]}
           Mobile: {bill_details["mobile"]}
           Address: {bill_details["address"]}
           Doctor Name: {bill_details["doctor_name"]}
           Hospital Name: {bill_details["hospital_name"]}
           --------------------------------------------------------
           Medicine Name | Quantity | Dose | Cost
           --------------------------------------------------------
           """
        for item in bill_items:
            bill_string += f"""{item["medicine_name"]} | {item["quantity"]} | {item["dose"]} | {item["cost"]}
               """
        bill_string += f"""
           --------------------------------------------------------
           Total Cost: {self.total_cost_entry.get()}
           ========================================================
           """
        return bill_string

    def get_bill_items(self):
        bill_items = []
        for item in self.bill_items_listbox.get(0, "end"):
            medicine_name, quantity, dose, cost = item.split(" - ")
            bill_items.append({
                "medicine_name": medicine_name,
                "quantity": quantity,
                "dose": dose,
                "cost": cost,
            })
        return bill_items

    def store_details_window(self):
        # Create store details window
        self.store_details_window = tk.Toplevel(self.root)
        self.store_details_window.title("Store Details")

        # Create store details label
        tk.Label(self.store_details_window, text="Store Details:").pack(side="top")

        # Create store details frame
        self.store_details_frame = tk.Frame(self.store_details_window)
        self.store_details_frame.pack(side="top")

        # Create store details labels
        tk.Label(self.store_details_frame, text="Store Name:").pack(side="left")
        self.store_details_name_label = tk.Label(self.store_details_frame, text="")
        self.store_details_name_label.pack(side="left")

        tk.Label(self.store_details_frame, text="Medicines:").pack(side="left")
        self.store_details_medicines_label = tk.Label(self.store_details_frame, text="")
        self.store_details_medicines_label.pack(side="left")

        # Get store details
        store_name = self.store_list.get(tk.ANCHOR)

        if store_name:
            self.cursor.execute("SELECT * FROM stores WHERE name = ?", (store_name,))
            store = self.cursor.fetchone()

            if store:
                self.store_details_name_label.config(text=store[1])
                self.cursor.execute("SELECT name FROM medicines")
                medicines = self.cursor.fetchall()
                medicine_names = ", ".join([m[0] for m in medicines])
                self.store_details_medicines_label.config(text=medicine_names)
            else:
                messagebox.showerror("Error", "Store not found!")
        else:
            messagebox.showerror("Error", "Please select a store from the list!")

    def modify_medicine_window(self):
        # Create modify medicine window
        self.modify_medicine_window = tk.Toplevel(self.root)
        self.modify_medicine_window.title("Modify Medicine")

        # Create medicine name label and entry
        tk.Label(self.modify_medicine_window, text="Enter Medicine Name:").pack(side="top")
        self.modify_medicine_name_entry = tk.Entry(self.modify_medicine_window, width=40)
        self.modify_medicine_name_entry.pack(side="top")

        # Create search button
        tk.Button(self.modify_medicine_window, text="Search", command=self.search_medicine_to_modify).pack(side="top")

        # Create modify details frame
        self.modify_details_frame = tk.Frame(self.modify_medicine_window)
        self.modify_details_frame.pack(side="top")

        # Create modify details labels and entries
        tk.Label(self.modify_details_frame, text="Quantity:").pack(side="left")
        self.modify_quantity_entry = tk.Entry(self.modify_details_frame, width=20)
        self.modify_quantity_entry.pack(side="left")

        tk.Label(self.modify_details_frame, text="Price:").pack(side="left")
        self.modify_price_entry = tk.Entry(self.modify_details_frame, width=20)
        self.modify_price_entry.pack(side="left")

        # Create modify button
        tk.Button(self.modify_details_frame, text="Modify", command=self.modify_medicine).pack(side="left")

    def search_medicine_to_modify(self):
        medicine_name = self.modify_medicine_name_entry.get()

        if medicine_name:
            self.cursor.execute("SELECT * FROM medicines WHERE name = ?", (medicine_name,))
            medicine = self.cursor.fetchone()

            if medicine:
                self.modify_quantity_entry.delete(0, "end")
                self.modify_price_entry.delete(0, "end")
                self.modify_quantity_entry.insert(0, medicine[2])
                self.modify_price_entry.insert(0, medicine[3])
            else:
                messagebox.showinfo("Not Found", "Medicine not found!")
        else:
            messagebox.showerror("Error", "Please enter a medicine name!")

    def modify_medicine(self):
        medicine_name = self.modify_medicine_name_entry.get()
        quantity = self.modify_quantity_entry.get()
        price = self.modify_price_entry.get()

        if medicine_name and quantity and price:
            try:
                quantity = int(quantity)
                price = float(price)
                self.cursor.execute("UPDATE medicines SET quantity = ?, price = ? WHERE name = ?", (quantity, price, medicine_name))
                self.conn.commit()
                messagebox.showinfo("Success", "Medicine modified successfully!")
                self.modify_medicine_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Quantity and Price must be numbers!")
        else:
            messagebox.showerror("Error", "Please fill in all medicine information fields!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalStoreManagementSystem(root)
    root.mainloop()