from db_connection import get_connection
import time

# ------------------ LOADING PAGE ------------------
def loading():
    print("\nLoading Restaurant Management System", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="")
    print("\n")


# ------------------ VIEW MENU ------------------
def view_menu():
    db = get_connection()
    cur = db.cursor()

    cur.execute("SELECT * FROM menu")
    items = cur.fetchall()

    print("\n--------- AVAILABLE MENU ---------")
    print("ID   Dish Name                 Type        Price")
    print("-----------------------------------------------")
    for item in items:
        print(f"{item[0]:<4} {item[1]:<25} {item[2]:<10} ₹{item[3]}")
    print("-----------------------------------------------")

    db.close()


# ------------------ BOOK ORDER ------------------
def book_order():
    db = get_connection()
    cur = db.cursor()

    name = input("Enter your name: ")
    mob = int(input("Enter mobile number: "))
    address = input("Enter address: ")

    while True:
        dish_id = int(input("Enter Dish ID: "))
        qty = int(input("Enter quantity: "))

        cur.execute("SELECT PRICE FROM menu WHERE ID=%s", (dish_id,))
        price = cur.fetchone()

        if price is None:
            print("Invalid Dish ID!")
            continue

        total = price[0] * qty

        cur.execute(
            "INSERT INTO cusdet (ID, QUANTITY, NAME, MOBNO, ADDRESS, TOTALPRICE) VALUES (%s,%s,%s,%s,%s,%s)",
            (dish_id, qty, name, mob, address, total)
        )

        db.commit()
        print("Order placed successfully!")
        print(f"Total Price: ₹{total}")

        more = input("Do you want to order something else? (yes/no): ").lower()
        if more != "yes":
            break

    db.close()


# ------------------ VIEW YOUR ORDERS ------------------
def view_orders():
    db = get_connection()
    cur = db.cursor()

    mob = int(input("Enter your mobile number: "))

    query = """
    SELECT c.ORDER_ID, m.NAME, c.QUANTITY, c.TOTALPRICE, c.ADDRESS
    FROM cusdet c
    JOIN menu m ON c.ID = m.ID
    WHERE c.MOBNO = %s
    """

    cur.execute(query, (mob,))
    orders = cur.fetchall()

    if not orders:
        print("No orders found!")
    else:
        print("\n------- YOUR ORDERS -------")
        for o in orders:
            print(f"Order ID: {o[0]} | Item: {o[1]} | Qty: {o[2]} | Total: ₹{o[3]}")
            print(f"Address: {o[4]}")
            print("----------------------------")

    db.close()


# ------------------ EDIT ORDER ------------------
def edit_order():
    db = get_connection()
    cur = db.cursor()

    order_id = int(input("Enter Order ID to edit: "))
    new_qty = int(input("Enter new quantity: "))

    cur.execute("SELECT ID FROM cusdet WHERE ORDER_ID=%s", (order_id,))
    dish = cur.fetchone()

    if dish is None:
        print("Invalid Order ID!")
        db.close()
        return

    cur.execute("SELECT PRICE FROM menu WHERE ID=%s", (dish[0],))
    price = cur.fetchone()[0]

    new_total = price * new_qty

    cur.execute(
        "UPDATE cusdet SET QUANTITY=%s, TOTALPRICE=%s WHERE ORDER_ID=%s",
        (new_qty, new_total, order_id)
    )

    db.commit()
    print("Order updated successfully!")
    print(f"New Total Price: ₹{new_total}")

    db.close()


# ------------------ CANCEL ORDER ------------------
def cancel_order():
    db = get_connection()
    cur = db.cursor()

    order_id = int(input("Enter Order ID to cancel: "))

    cur.execute("DELETE FROM cusdet WHERE ORDER_ID=%s", (order_id,))
    db.commit()

    print("Order cancelled successfully!")
    db.close()


# ------------------ FEEDBACK ------------------
def feedback():
    db = get_connection()
    cur = db.cursor()

    name = input("Enter your name: ")
    comment = input("Write your feedback: ")

    cur.execute(
        "INSERT INTO feedback (NAME, COMMENTS) VALUES (%s,%s)",
        (name, comment)
    )

    db.commit()
    print("Thank you for your feedback!")

    db.close()


# ------------------ MAIN MENU ------------------
def main_menu():
    while True:
        print("\n===== GROVE STREET RESTAURANT =====")
        print("1. View Menu")
        print("2. Book Order")
        print("3. View Your Orders")
        print("4. Edit Order")
        print("5. Cancel Order")
        print("6. Feedback")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            view_menu()
        elif choice == "2":
            book_order()
        elif choice == "3":
            view_orders()
        elif choice == "4":
            edit_order()
        elif choice == "5":
            cancel_order()
        elif choice == "6":
            feedback()
        elif choice == "7":
            print("Thank you for visiting Grove Street Restaurant!")
            break
        else:
            print("Invalid choice! Try again.")


# ------------------ START PROGRAM ------------------
loading()
main_menu()
