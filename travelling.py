import streamlit as st
import mysql.connector
from datetime import datetime

# MySQL database connection
def connect_db():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="iamvengeance",
            database="MOUNTAIN",
            auth_plugin="mysql_native_password"
        )
        return db
    except mysql.connector.Error as err:
        st.error(f"Database Connection Error: {err}")
        return None

# Add customer to database
def add_customer(db, data):
    query = """
        INSERT INTO customers 
        (customer_id, name, contact_no, address, gender, product, price, pickup_date_time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = db.cursor()
    try:
        cursor.execute(query, data)
        db.commit()
        st.success("Customer added successfully!")
    except mysql.connector.Error as err:
        st.error(f"Error adding customer: {err}")

# Show all customers
def show_customers(db):
    query = "SELECT * FROM customers"
    cursor = db.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            st.write({
                "Customer ID": row[0],
                "Name": row[1],
                "Contact": row[2],
                "Address": row[3],
                "Gender": row[4],
                "Activity": row[5],
                "Amount": row[6],
                "Pickup Date": row[7]
            })
    except mysql.connector.Error as err:
        st.error(f"Error fetching data: {err}")

# App UI
def main():
    st.title("Mountain Travel Customer Management")

    menu = ["Add Customer", "View All Customers"]
    choice = st.sidebar.selectbox("Select Option", menu)

    db = connect_db()
    if not db:
        return

    if choice == "Add Customer":
        st.subheader("Enter Customer Details")

        customer_id = st.text_input("Customer ID")
        name = st.text_input("Name")
        contact = st.text_input("Contact Number")
        address = st.text_area("Address")
        gender = st.selectbox("Gender", ["Male", "Female"])
        product = st.text_input("Activity")
        price = st.text_input("Amount")
        pickup_time = st.text_input("Pickup Date & Time", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        if st.button("Add"):
            if all([customer_id, name, contact, address, product, price]):
                data = (customer_id, name, contact, address, gender, product, price, pickup_time)
                add_customer(db, data)
            else:
                st.warning("Please fill in all required fields.")

    elif choice == "View All Customers":
        st.subheader("Customer Records")
        show_customers(db)

if __name__ == "__main__":
    main()
