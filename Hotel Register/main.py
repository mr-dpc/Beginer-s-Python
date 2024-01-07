class HotelRegister:
    def __init__(self):
        self.guests = {}

    def check_in(self):
        guest_name = input("Enter guest name: ")
        room_number = input("Enter room number: ")

        if room_number in self.guests:
            print(f"Room {room_number} is already occupied.")
        else:
            self.guests[room_number] = guest_name
            print(f"Check-in successful. {guest_name} is now in room {room_number}.")

    def check_out(self):
        room_number = input("Enter room number to check out: ")

        if room_number in self.guests:
            guest_name = self.guests.pop(room_number)
            print(f"Check-out successful. {guest_name} has left room {room_number}.")
        else:
            print(f"No guest found in room {room_number}.")

    def display_guests(self):
        if not self.guests:
            print("No guests currently checked in.")
        else:
            print("\nCurrent Guests:")
            for room, guest in self.guests.items():
                print(f"Room {room}: {guest}")

def main():
    hotel_register = HotelRegister()

    while True:
        print("\n1. Check-in\n2. Check-out\n3. Display Guests\n4. Quit")
        choice = input("Select an option (1/2/3/4): ")

        if choice == "1":
            hotel_register.check_in()
        elif choice == "2":
            hotel_register.check_out()
        elif choice == "3":
            hotel_register.display_guests()
        elif choice == "4":
            print("Exiting hotel register.")
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()

