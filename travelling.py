import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Entry, Button, StringVar, OptionMenu
import mysql.connector
from datetime import datetime
from PIL import Image, ImageTk

class CustomerManagementApp:
    def __init__(self, root):
        self.root = root

    def open_first_window(self):
        # Create first window
        self.first_window = tk.Frame(self.root)
        self.first_window.pack(fill="both", expand=True)

        # Load background image
        image_path = "C:\\Users\\daksh\\Downloads\\mountain travelling.png"
        image = Image.open(image_path)
        image = image.resize((800, 600))  # Resize the image
        photo = ImageTk.PhotoImage(image)

        # Create background label with image
        background_label = Label(self.first_window, image=photo)
        background_label.image = photo  # Keep reference to the image
        background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create "Continue" button
        continue_button = Button(self.first_window, text="Continue", command=self.open_main_window, bg="blue", fg="white")
        continue_button.place(relx=0.5, rely=0.9, relwidth=0.2, relheight=0.1)

    def open_main_window(self):
        # Hide the first window
        self.first_window.pack_forget()

        # Create main window
        self.main_window = tk.Frame(self.root)
        self.main_window.pack(fill="both", expand=True)

        # MySQL Database Connection
        try:
            self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="iamvengeance",
            database="MOUNTAIN",
            auth_plugin="mysql_native_password"
)

            self.cursor = self.db.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            self.main_window.destroy()
            return

        # GUI Components
        self.create_widgets()

    def create_widgets(self):
        # Customer details form
        self.id_label = Label(self.main_window, text="Customer ID")
        self.id_label.pack()
        self.id_entry = Entry(self.main_window)
        self.id_entry.pack()

        self.name_label = Label(self.main_window, text="Customer Name")
        self.name_label.pack()
        self.name_entry = Entry(self.main_window)
        self.name_entry.pack()

        self.contact_label = Label(self.main_window, text="Contact No")
        self.contact_label.pack()
        self.contact_entry = Entry(self.main_window)
        self.contact_entry.pack()

        self.address_label = Label(self.main_window, text="Address")
        self.address_label.pack()
        self.address_entry = Entry(self.main_window)
        self.address_entry.pack()

        self.gender_label = Label(self.main_window, text="Gender")
        self.gender_label.pack()
        self.gender_var = StringVar(self.main_window)
        self.gender_var.set("Select Gender")
        self.gender_menu = OptionMenu(self.main_window, self.gender_var, "Male", "Female")
        self.gender_menu.pack()

        self.activity_label = Label(self.main_window, text="Activity")
        self.activity_label.pack()
        self.activity_entry = Entry(self.main_window)
        self.activity_entry.pack()

        self.amount_label = Label(self.main_window, text="Amount")
        self.amount_label.pack()
        self.amount_entry = Entry(self.main_window)
        self.amount_entry.pack()

        # Automatically fill pickup date and time
        self.date_label = Label(self.main_window, text="Pickup Date & Time")
        self.date_label.pack()
        self.date_entry = Entry(self.main_window)
        self.date_entry.pack()
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Buttons for operations
        self.add_button = Button(self.main_window, text="Add Customer", command=self.add_customer)
        self.add_button.pack()

        self.modify_button = Button(self.main_window, text="Modify Customer", command=self.modify_customer)
        self.modify_button.pack()

        self.delete_button = Button(self.main_window, text="Delete Customer", command=self.delete_customer)
        self.delete_button.pack()

        self.search_button = Button(self.main_window, text="Search Customer", command=self.search_customer)
        self.search_button.pack()

        self.show_button = Button(self.main_window, text="Show Data", command=self.show_data)
        self.show_button.pack()

        self.history_button = Button(self.main_window, text="History of Customers", command=self.show_history)
        self.history_button.pack()

        self.bill_button = Button(self.main_window, text="Get Bill", command=self.get_bill)
        self.bill_button.pack()

        self.clear_button = Button(self.main_window, text="Clear", command=self.clear_fields)
        self.clear_button.pack()

    def add_customer(self):
        if not self.id_entry.get() or not self.name_entry.get() or not self.contact_entry.get() or not self.address_entry.get() or not self.activity_entry.get() or not self.amount_entry.get():
            messagebox.showerror("Error", "Please fill all fields")
            return
        query = """INSERT INTO customers 
                   (customer_id, name, contact_no, address, gender, product, price, pickup_date_time)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            self.id_entry.get(), self.name_entry.get(), self.contact_entry.get(),
            self.address_entry.get(), self.gender_var.get(), self.activity_entry.get(),
            self.amount_entry.get(), self.date_entry.get()
        )
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Success", "Customer added successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        self.clear_fields()

    def modify_customer(self):
        if not self.id_entry.get():
            messagebox.showerror("Error", "Please enter Customer ID")
            return
        query = """UPDATE customers SET name=%s, contact_no=%s, address=%s, gender=%s, 
                   activity=%s, amount=%s, pickup_date_time=%s WHERE customer_id=%s"""
        values = (
            self.name_entry.get(), self.contact_entry.get(), self.address_entry.get(),
            self.gender_var.get(), self.activity_entry.get(), self.amount_entry.get(),
            self.date_entry.get(), self.id_entry.get()
        )
        try:
            self.cursor.execute(query, values)
            self.db.commit()
            messagebox.showinfo("Success", "Customer details updated!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        self.clear_fields()

    def delete_customer(self):
        if not self.id_entry.get():
            messagebox.showerror("Error", "Please enter Customer ID")
            return
        query = "DELETE FROM customers WHERE customer_id=%s"
        try:
            self.cursor.execute(query, (self.id_entry.get(),))
            self.db.commit()
            messagebox.showinfo("Success", "Customer deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
        self.clear_fields()

    def search_customer(self):
        if not self.id_entry.get():
            messagebox.showerror("Error", "Please enter Customer ID")
            return
        query = "SELECT * FROM customers WHERE customer_id=%s"
        try:
            self.cursor.execute(query, (self.id_entry.get(),))
            result = self.cursor.fetchone()
            if result:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, result[1])
                self.contact_entry.delete(0, tk.END)
                self.contact_entry.insert(0, result[2])
                self.address_entry.delete(0, tk.END)
                self.address_entry.insert(0, result[3])
                self.gender_var.set(result[4])
                self.activity_entry.delete(0, tk.END)
                self.activity_entry.insert(0, result[5])
                self.amount_entry.delete(0, tk.END)
                self.amount_entry.insert(0, result[6])
                self.date_entry.delete(0, tk.END)
                self.date_entry.insert(0, result[7])
            else:
                messagebox.showinfo("Info", "Customer not found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def show_data(self):
        data_window = Toplevel(self.root)
        data_window.title("Customer Data")
        query = "SELECT * FROM customers"
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            for i, row in enumerate(results):
                Label(data_window, text=f"Customer ID: {row[0]}, Name: {row[1]}, Contact: {row[2]}, activity: {row[5]}").pack()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    def show_history(self):
        pass  # Add implementation as needed

    def get_bill(self):
        pass  # Add implementation as needed

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.gender_var.set("Select Gender")
        self.activity_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def new_func(CustomerManagementApp, root):
    app = CustomerManagementApp(root)
    return app

if __name__ == "__main__":
    root = tk.Tk()
    app = new_func(CustomerManagementApp, root)
    app.open_first_window()
    root.mainloop()
