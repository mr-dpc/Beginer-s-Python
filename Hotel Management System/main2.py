import tkinter as tk
from tkinter import messagebox
import pyttsx3

class HotelManagementSystem:
    def __init__(self):
        self.rooms = {}  # Dictionary to store room number and guest details
        self.filename = "db.txt"  # Text file to save and load data
        self.load_data()  # Load data from the file
        self.create_gui()
        self.init_text_to_speech()

    def init_text_to_speech(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.setProperty('voice',2)
        self.engine.say(text)
        self.engine.runAndWait()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Hotel Management System")
        self.root.geometry("451x457")
        self.root.resizable(False, False)
        self.root.iconbitmap("hotel.ico")
        self.root.configure(bg="#bf046b")
        self.root.attributes("-alpha", 0.85)

        self.label = tk.Label(self.root, text="Hotel Management System", font=("Helvetica", 16), bg="#bf046b")
        self.label.pack(pady=10)

        self.create_input_fields()
        self.create_button_frame()

    def create_input_fields(self):
        # Room Number Entry
        self.room_number_label = tk.Label(self.root, text="Room Number:", bg="#bf046b")
        self.room_number_label.pack()
        self.room_number_entry = tk.Entry(self.root, bg="#ffffff")
        self.room_number_entry.pack(pady=5)

        # Guest Name Entry
        self.guest_name_label = tk.Label(self.root, text="Guest Name:", bg="#bf046b")
        self.guest_name_label.pack()
        self.guest_name_entry = tk.Entry(self.root, bg="#ffffff")
        self.guest_name_entry.pack(pady=5)

    def create_button_frame(self):
        button_frame = tk.Frame(self.root, bg="#bf046b")
        button_frame.pack(pady=10)

        self.check_in_button = tk.Button(button_frame, text="Check In", command=self.check_in, bg="#bf046b")
        self.check_in_button.pack(side=tk.LEFT, padx=5)

        self.check_out_button = tk.Button(button_frame, text="Check Out", command=self.check_out, bg="#bf046b")
        self.check_out_button.pack(side=tk.LEFT, padx=5)

        self.show_guests_button = tk.Button(self.root, text="Show Guests", command=self.show_guests, bg="#bf046b")
        self.show_guests_button.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Search Room", command=self.search_room, bg="#bf046b")
        self.search_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Quit App", command=self.save_and_quit, bg="#bf046b")
        self.quit_button.pack(pady=5)

        self.about_button = tk.Button(self.root, text="About", command=self.show_about_dialog, bg="#bf046b")
        self.about_button.pack(pady=5)

        self.visualization_button = tk.Button(self.root, text="Room Visualization", command=self.show_room_visualization, bg="#bf046b")
        self.visualization_button.pack(pady=5)

    def show_about_dialog(self):
        about_dialog = AboutDialog(self.root)

    def show_room_visualization(self):
        visualization_window = RoomVisualization(self.root, self.rooms)

    def check_in(self):
        room_number = self.get_room_number(self.room_number_entry.get(), "Enter Room Number to Check In:")
        if room_number:
            guest_name = self.guest_name_entry.get()
            if room_number in self.rooms:
                messagebox.showwarning("Check In Error", f"Room {room_number} is already occupied by {self.rooms[room_number]}")
            else:
                self.rooms[room_number] = guest_name
                messagebox.showinfo("Check In", f"Guest {guest_name} checked into Room {room_number}")
                self.save_data()
                self.speak(f"{guest_name} has checked in room number {room_number}")

    def check_out(self):
        room_number = self.get_room_number(self.room_number_entry.get(), "Enter Room Number to Check Out:")
        if room_number in self.rooms:
            guest_name = self.rooms.pop(room_number)
            messagebox.showinfo("Check Out", f"Guest {guest_name} checked out from Room {room_number}")
            self.save_data()
            self.speak(f"{guest_name} has checked out from room number {room_number}")
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
            pass

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
            "Developed by: Your Name\n"
            "Copyright © 2024\n\n"
            "This software helps manage hotel room bookings and guest information."
        )

        about_label = tk.Label(about_window, text=about_text, padx=10, pady=10)
        about_label.pack()

        ok_button = tk.Button(about_window, text="OK", command=about_window.destroy)
        ok_button.pack(pady=10)

class RoomVisualization:
    def __init__(self, parent, rooms):
        self.parent = parent
        self.rooms = rooms
        self.create_visualization()

    def create_visualization(self):
        visualization_window = tk.Toplevel(self.parent)
        visualization_window.title("Room Visualization")

        rows = 5
        cols = 2
        room_labels = []

        for room, guest in self.rooms.items():
            room_labels.append(f"Room {room}\nGuest: {guest}")

        for i in range(rows):
            for j in range(cols):
                index = i * cols + j
                if index < len(room_labels):
                    label = tk.Label(visualization_window, text=room_labels[index], padx=10, pady=10, borderwidth=2, relief="solid")
                    label.grid(row=i, column=j, padx=5, pady=5)
                else:
                    break

        ok_button = tk.Button(visualization_window, text="OK", command=visualization_window.destroy)
        ok_button.grid(row=rows, column=0, columnspan=cols, pady=10)

def main():
    hotel_system = HotelManagementSystem()
    hotel_system.run()

if __name__ == "__main__":
    main()
