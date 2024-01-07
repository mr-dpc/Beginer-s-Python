import tkinter as tk
from tkinter import messagebox

class HotelManagementSystem:
    def __init__(self):
        self.rooms = {}  # Dictionary to store room number and guest details
        self.filename = "db.txt"  # Text file to save and load data
        self.load_data()  # Load data from the file
        self.create_gui()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Hotel Management System")
        self.root.geometry("451x457")
        self.root.resizable(False, False)

        # Set the custom icon
        self.root.iconbitmap("hotel.ico")

        # Set background color of the main window
        self.root.configure(bg="#34caf7")
        self.root.attributes("-alpha", 0.85)

        self.label = tk.Label(self.root, text="Hotel Management System", font=("Helvetica", 16), bg="#34caf7")
        self.label.pack(pady=10)

        self.room_number_label = tk.Label(self.root, text="Room Number:", bg="#34caf7")
        self.room_number_label.pack()
        self.room_number_entry = tk.Entry(self.root, bg="#34caf7")
        self.room_number_entry.pack(pady=5)

        self.guest_name_label = tk.Label(self.root, text="Guest Name:", bg="#34caf7")
        self.guest_name_label.pack()
        self.guest_name_entry = tk.Entry(self.root, bg="#34caf7")
        self.guest_name_entry.pack(pady=5)

        # Frame to hold Check In and Check Out buttons
        button_frame = tk.Frame(self.root, bg="#34caf7")
        button_frame.pack(pady=10)

        self.check_in_button = tk.Button(button_frame, text="Check In", command=self.check_in, bg="#34caf7")
        self.check_in_button.pack(side=tk.LEFT, padx=5)

        self.check_out_button = tk.Button(button_frame, text="Check Out", command=self.check_out, bg="#34caf7")
        self.check_out_button.pack(side=tk.LEFT, padx=5)

        self.show_guests_button = tk.Button(self.root, text="Show Guests", command=self.show_guests, bg="#34caf7")
        self.show_guests_button.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Search Room", command=self.search_room, bg="#34caf7")
        self.search_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit App", command=self.save_and_quit, bg="#34caf7")
        self.quit_button.pack(pady=5)

        # About button to show the About Dialog
        self.about_button = tk.Button(self.root, text="About", command=self.show_about_dialog, bg="#34caf7")
        self.about_button.pack(pady=5)

    def show_about_dialog(self):
        about_dialog = AboutDialog(self.root)

    def check_in(self):
        room_number = self.get_room_number(self.room_number_entry.get(), "Enter Room Number to Check In:")
        if room_number:
            guest_name = self.guest_name_entry.get()
            self.rooms[room_number] = guest_name
            messagebox.showinfo("Check In", f"Guest {guest_name} checked into Room {room_number}")
            self.save_data()

    def check_out(self):
        room_number = self.get_room_number(self.room_number_entry.get(), "Enter Room Number to Check Out:")
        if room_number in self.rooms:
            guest_name = self.rooms.pop(room_number)
            messagebox.showinfo("Check Out", f"Guest {guest_name} checked out from Room {room_number}")
            self.save_data()
        else:
            messagebox.showwarning("Error", f"No guest found in Room {room_number}")

    def show_guests(self):
        if not self.rooms:
            messagebox.showinfo("Guest List", "No guests currently checked in.")
        else:
            guest_list = "\n".join([f"Room {room}: {guest}" for room, guest in self.rooms.items()])
            messagebox.showinfo("Guest List", guest_list)

    def search_room(self):
        room_number = self.get_room_number(self.room_number_entry.get(), "Enter Room Number to Search:")
        if room_number in self.rooms:
            guest_name = self.rooms[room_number]
            messagebox.showinfo("Search Result", f"Room {room_number} is occupied by {guest_name}")
        else:
            messagebox.showinfo("Search Result", f"Room {room_number} is currently unoccupied")

    def get_room_number(self, input_value, prompt):
        try:
            room_number = int(input_value)
            if room_number <= 0:
                raise ValueError("Room number must be a positive integer.")
            return room_number
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return None

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    room, guest = map(str.strip, line.split(':'))
                    self.rooms[int(room)] = guest
        except FileNotFoundError:
            pass  # No file found, ignore

    def save_data(self):
        with open(self.filename, 'w') as file:
            for room, guest in self.rooms.items():
                file.write(f"{room}: {guest}\n")

    def save_and_quit(self):
        self.save_data()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

class AboutDialog:
    def __init__(self, parent):
        self.parent = parent
        self.create_about_dialog()

    def create_about_dialog(self):
        about_window = tk.Toplevel(self.parent)
        about_window.title("About Hotel Management System")

        about_text = (
            "Hotel Management System\n\n"
            "Version: 1.0\n"
            "Developed by: Sayem Billah\n"
            "Copyright © 2024\n\n"
            "This software helps manage hotel room bookings and guest information."
        )

        about_label = tk.Label(about_window, text=about_text, padx=10, pady=10)
        about_label.pack()

        ok_button = tk.Button(about_window, text="OK", command=about_window.destroy)
        ok_button.pack(pady=10)

def main():
    hotel_system = HotelManagementSystem()
    hotel_system.run()

if __name__ == "__main__":
    main()
