import json
import csv

class User:
    def __init__(self, username, password, is_landlord):
        self.username = username
        self.password = password
        self.is_landlord = is_landlord

# Список для хранения всех пользователей
all_users = []

# Текущий пользователь
current_user = None

def create_user():
    username = input("Enter username: ")
    password = input("Enter password: ")
    return User(username, password, False)  # При создании пользователя предполагаем, что он арендатор

def register():
    print("Register:")
    user = create_user()
    all_users.append(user)
    print("User registered successfully.")

def login():
    global current_user
    username = input("Enter username: ")
    password = input("Enter password: ")
    for user in all_users:
        if user.username == username and user.password == password:
            current_user = user
            print("Login successful.")
            return
    print("Invalid username or password.")

class Goods:
    def __init__(self, name, price, rooms, address, email, phone, number, area):
        self.name = name
        self.price = price
        self.rooms = rooms
        self.address = address
        self.email = email
        self.phone = phone
        self.number = number
        self.area = area
        self.reservations = []

    def reserve(self, start_date, end_date):
        self.reservations.append((start_date, end_date))

    def cancel_reservation(self, index):
        if 0 <= index < len(self.reservations):
            del self.reservations[index]
            print("Reservation canceled successfully.")
        else:
            print("Invalid reservation index.")

all_goods = []

def create_goods_from_input():
    name = input("Enter name: ")
    price = float(input("Enter price: "))
    rooms = int(input("Enter number of rooms: "))
    address = input("Enter address: ")
    email = input("Enter email: ")
    phone = input("Enter phone number: ")
    number = input("Enter number: ")
    area = float(input("Enter area: "))
    goods = Goods(name, price, rooms, address, email, phone, number, area)
    all_goods.append(goods)
    return goods

def save_to_json(filename):
    with open(filename, 'w') as file:
        json.dump([goods.__dict__ for goods in all_goods], file)

def load_from_json(filename):
    with open(filename) as file:
        data = json.load(file)
        all_goods.clear()
        for goods_data in data:
            goods = Goods(goods_data['name'], goods_data['price'], goods_data['rooms'], goods_data['address'], goods_data['email'], goods_data['phone'], goods_data['number'], goods_data['area'])
            goods.reservations = goods_data['reservations']
            all_goods.append(goods)

def save_to_csv(filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'price', 'rooms', 'address', 'email', 'phone', 'number', 'area', 'reservations'])
        for goods in all_goods:
            writer.writerow([goods.name, goods.price, goods.rooms, goods.address, goods.email, goods.phone, goods.number, goods.area, goods.reservations])

def load_from_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        next(reader)  
        all_goods.clear()
        for row in reader:
            goods = Goods(row[0], float(row[1]), int(row[2]), row[3], row[4], row[5], row[6], float(row[7]))
            goods.reservations = json.loads(row[8])
            all_goods.append(goods)

def create_listing():
    goods = create_goods_from_input()
    print("Listing created successfully.")

def delete_listing():
    if not all_goods:
        print("The list is empty.")
        return
    print("Current Listings:")
    for i, goods in enumerate(all_goods):
        print(f"{i + 1}. {goods}")
    choice = int(input("Enter the listing number to delete: "))
    if 1 <= choice <= len(all_goods):
        del all_goods[choice - 1]
        print("Listing deleted successfully.")
    else:
        print("Invalid choice.")

def reserve_listing():
    if not all_goods:
        print("The list is empty.")
        return
    print("Current Listings:")
    for i, goods in enumerate(all_goods):
        print(f"{i + 1}. {goods}")
    choice = int(input("Enter the listing number to reserve: "))
    if 1 <= choice <= len(all_goods):
        goods = all_goods[choice - 1]
        start_date = input("Enter start date of reservation: ")
        end_date = input("Enter end date of reservation: ")
        goods.reserve(start_date, end_date)
        print("Reservation successful.")
    else:
        print("Invalid choice.")

def view_reservations():
    if not all_goods:
        print("The list is empty.")
        return
    print("Your Reservations:")
    for i, goods in enumerate(all_goods):
        print(f"{i + 1}. {goods.name}")
        for j, reservation in enumerate(goods.reservations):
            print(f"    {j + 1}. {reservation[0]} to {reservation[1]}")

def cancel_reservation():
    if not all_goods:
        print("The list is empty.")
        return
    print("Your Reservations:")
    for i, goods in enumerate(all_goods):
        print(f"{i + 1}. {goods.name}")
        for j, reservation in enumerate(goods.reservations):
            print(f"    {j + 1}. {reservation[0]} to {reservation[1]}")
    listing_choice = int(input("Enter the listing number to cancel reservation: "))
    reservation_choice = int(input("Enter the reservation number to cancel: "))
    if 1 <= listing_choice <= len(all_goods):
        goods = all_goods[listing_choice - 1]
        goods.cancel_reservation(reservation_choice - 1)
    else:
        print("Invalid listing choice.")

def view_all_reservations():
    if not all_goods:
        print("The list is empty.")
        return
    print("All Reservations:")
    for goods in all_goods:
        if goods.reservations:
            print(f"{goods.name}:")
            for i, reservation in enumerate(goods.reservations):
                print(f"    {i + 1}. {reservation[0]} to {reservation[1]}")

if __name__ == "__main__":
    while True:
        print("Welcome!")
        print("Please select your mode:")
        print("1. Register")
        print("2. Log In")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
            if current_user:
                print("You have successfully logged in.")
                if current_user.is_landlord:
                    print("You are a rent-giver.")
                else:
                    print("You are a rent-seeker.")
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")
