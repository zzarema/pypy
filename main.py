import json
import csv
import random
import string


class User:
    
    def __init__(self, username, password):
       

        self.username = username
        self.password = password
        self.reservations = [] 


class AuthManager:
    

    def __init__(self):
        

        self.users = []  

    def register(self, username, password):
       


        if any(user.username == username for user in self.users):
            print("User with this username already exists.")
        else:
            self.users.append(User(username, password))
            print("Registration successful.")

    def login(self, username, password):
        

        for user in self.users:
            if user.username == username and user.password == password:
                print("Login successful.")
                return user
        print("Invalid username or password.")
        return None

    def user_login_or_register(self):
       

        while True:
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ")

            if choice == "1":
                return self.login_user()
            elif choice == "2":
                self.register_user()
            elif choice == "3":
                return None
            else:
                print("Invalid choice. Please select 1, 2, or 3.")

    def register_user(self):
        

        username = input("Enter username: ")
        password = input("Enter password: ")
        self.register(username, password)

    def login_user(self):
       

        username = input("Enter username: ")
        password = input("Enter password: ")
        return self.login(username, password)




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
        

        confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.reservations.append((start_date, end_date, confirmation_code))
        print("Reservation successful.")
        print("Confirmation code:", confirmation_code)

    def confirm_reservation(self, index):
        

        if 0 <= index < len(self.reservations):
            reservation = self.reservations[index]
            del self.reservations[index]
            print("Reservation confirmed successfully.")
            return reservation  
        else:
            print("Invalid reservation index.")
            return None

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



def confirm_reservation(user):
    

    print("Your Reservations:")
    for i, reservation in enumerate(user.reservations):
        print(f"{i + 1}. {reservation[0]} to {reservation[1]}")
    choice = int(input("Enter the reservation number to confirm: ")) - 1
    if 0 <= choice < len(user.reservations):
        reservation = user.reservations[choice]
        confirmed_reservation = all_goods[reservation[0]].confirm_reservation(choice)
        if confirmed_reservation:
            
            user.reservations.remove(reservation)
          
            save_confirmed_reservation(confirmed_reservation)
    else:
        print("Invalid choice.")


def save_confirmed_reservation(confirmed_reservation):
    

    with open('orders.json', 'a') as file:
        json.dump(confirmed_reservation, file)
        file.write('\n')

    with open('orders.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(confirmed_reservation)


def view_user_reservations(user):
    

    print(f"Reservations for user {user.username}:")
    if user.reservations:
        for i, reservation in enumerate(user.reservations):
            print(f"{i + 1}. {reservation[0]} to {reservation[1]}")
    else:
        print("You have no reservations.")


def user_dashboard(user):
   

    print(f"Welcome, {user.username}!")
    if user.reservations:
        print("Your Reservations:")
        for i, reservation in enumerate(user.reservations):
            print(f"{i + 1}. {reservation[0]} to {reservation[1]}")
    else:
        print("You have no reservations.")


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

def create_listing():
    goods = create_goods_from_input()
    print("Listing created successfully.")

def save_to_json(filename, data):
    

    with open(filename, 'w') as file:
        json.dump(data, file)
    json.dump([goods.__dict__ for goods in all_goods], file)

def load_from_json(filename):
    with open(filename) as file:
        data = json.load(file)
        all_goods.clear()
        for goods_data in data:
            goods = Goods(goods_data['name'], goods_data['price'], goods_data['rooms'], goods_data['address'], goods_data['email'], goods_data['phone'], goods_data['number'], goods_data['area'])
            goods.reservations = goods_data['reservations']
            all_goods.append(goods)

def save_to_csv(filename, data):
    


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


def reserve_listing(user):
   


    print("Current Listings:")
    for i, goods in enumerate(all_goods):
        print(f"{i + 1}. {goods.name}")
    choice = int(input("Enter the listing number to reserve: ")) 
    if 1 <= choice < len(all_goods):
        goods = all_goods[choice-1]
        start_date = input("Enter start date of reservation: ")
        end_date = input("Enter end date of reservation: ")
        goods.reserve(start_date, end_date)
        
        user.reservations.append((choice, start_date, end_date))
        print("Reservation successful.")
    else:
        print("Invalid choice.")


def confirm_reservation(user):
   

    print("Your Reservations:")
    for i, reservation in enumerate(user.reservations):
        print(f"{i + 1}. {reservation[0]} to {reservation[1]}")
    choice = int(input("Enter the reservation number to confirm: ")) - 1
    if 0 <= choice < len(user.reservations):
        reservation = user.reservations[choice]
        confirmed_reservation = all_goods[reservation[0]].confirm_reservation(choice)
        if confirmed_reservation:
            
            user.reservations.remove(reservation)
            
            save_confirmed_reservation(confirmed_reservation)
    else:
        print("Invalid choice.")


def save_confirmed_reservation(confirmed_reservation):
    


    with open('orders.json', 'a') as file:
        json.dump(confirmed_reservation, file)
        file.write('\n')

    with open('orders.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(confirmed_reservation)

def view_user_reservations(user):
    

    print(f"Reservations for user {user.username}:")

    if user.reservations:
        for i, reservation in enumerate(user.reservations):
            goods_name = all_goods[reservation[0]].name
            print(f"{i + 1}. {goods_name}: {reservation[1]} to {reservation[2]}")
    else:
        print("You have no reservations.")


def delete_user_reservation(user):
   

    print("Your Reservations:")

    for i, reservation in enumerate(user.reservations):
        goods_name = all_goods[reservation[0]].name
        print(f"{i + 1}. {goods_name}: {reservation[1]} to {reservation[2]}")
    choice = int(input("Enter the reservation number to delete: ")) - 1
    if 0 <= choice < len(user.reservations):
        del user.reservations[choice]
        print("Reservation deleted successfully.")

    else:
        print("Invalid choice.")



auth_manager = AuthManager()

while True:
    print("Welcome!")
    print("Please select your mode:")
    print("1. Rent-giver")
    print("2. Rent-seeker")
    print("3. Exit")
    mode = input("Enter your choice (1-3): ")

    if mode == "1":
        print("You have selected Rent-giver mode.")

        while True:
            print("\nRent-giver Menu:")
            print("1. Create Listing")
            print("2. Delete Listing")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                goods = create_goods_from_input()
              
                all_goods.append(goods)

            elif choice == "2":
               
                print("Functionality not implemented yet.")
        
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")


    elif mode == "2":
        user = auth_manager.user_login_or_register()
        if user:
            while True:
                print("\nRent-seeker Menu:")
                print("1. Reserve Listing")
                print("2. View Reservations")
                print("3. Cancel Reservation")
                print("4. Delete Reservation")
                print("5. Exit")
                choice = input("Enter your choice: ")
                if choice == "1":
                    
                    reserve_listing(user)
                elif choice == "2":
                    view_user_reservations(user)
                elif choice == "3":
                    print("Functionality not implemented yet.")
                elif choice == "4":
                    delete_user_reservation(user)
                elif choice == "5":
                    break
                else:
                    print("Invalid choice. Please try again.")

    elif mode == "3":
        
        save_to_json("goods.json", [goods.__dict__ for goods in all_goods])
        save_to_csv("goods.csv", all_goods)
        break

    else:
        print("Invalid choice. Please select 1, 2, or 3.")
