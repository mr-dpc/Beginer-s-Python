import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import csv
from datetime import datetime
from reportlab.pdfgen import canvas


class StudentGradeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Calculator")

        # Variables to store input values
        self.name_var = tk.StringVar()
        self.id_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.section_var = tk.StringVar()
        self.english_var = tk.StringVar()
        self.math_var = tk.StringVar()
        self.science_var = tk.StringVar()
        self.social_science_var = tk.StringVar()
        self.gk_var = tk.StringVar()
        self.pe_var = tk.StringVar()
        self.art_var = tk.StringVar()

        # Create labels, entry widgets, and search widgets
        self.create_widgets()

    def validate_input(self):
        # Check if all fields are filled
        if not all([self.name_var.get(), self.id_var.get(), self.class_var.get(), self.section_var.get(),
                    self.english_var.get(), self.math_var.get(), self.science_var.get(),
                    self.social_science_var.get(), self.gk_var.get(), self.pe_var.get(), self.art_var.get()]):
            messagebox.showwarning("Incomplete Form", "Please fill in all fields.")
            return False

        # Check if class is in the range 1 to 10
        try:
            class_value = int(self.class_var.get())
            if not (1 <= class_value <= 10):
                messagebox.showwarning("Invalid Class", "Class must be between 1 and 10.")
                return False
        except ValueError:
            messagebox.showwarning("Invalid Class", "Please enter a valid numeric class value.")
            return False

        # Check if section is a single character between A and L
        if not (len(self.section_var.get()) == 1 and 'A' <= self.section_var.get() <= 'L'):
            messagebox.showwarning("Invalid Section", "Section must be a single character between A and L.")
            return False

        # Check if ID is a digit and has a length of 8
        try:
            id_value = int(self.id_var.get())
            if not (len(self.id_var.get()) == 8):
                messagebox.showwarning("Invalid ID", "ID must be a digit with a length of 8.")
                return False
        except ValueError:
            messagebox.showwarning("Invalid ID", "ID must be a numeric value.")
            return False

        # Check if marks are in the range 0 to 100 and contain only digits or decimals
        for subject, value in [("English", self.english_var.get()), ("Math", self.math_var.get()),
                               ("Science", self.science_var.get()), ("Social Science", self.social_science_var.get()),
                               ("General Knowledge", self.gk_var.get()), ("Physical Education", self.pe_var.get()),
                               ("Art", self.art_var.get())]:
            try:
                marks_value = float(value)
                if not (0 <= marks_value <= 100):
                    messagebox.showwarning(f"Invalid {subject} Marks", f"{subject} marks must be between 0 and 100.")
                    return False
            except ValueError:
                messagebox.showwarning(f"Invalid {subject} Marks", f"{subject} marks must be numeric.")
                return False

        return True

    def calculate_grades(self):
        if not self.validate_input():
            return

        try:
            # Calculate total subject marks out of 700
            total_marks = (float(self.english_var.get()) +
                           float(self.math_var.get()) +
                           float(self.science_var.get()) +
                           float(self.social_science_var.get()) +
                           float(self.gk_var.get()) +
                           float(self.pe_var.get()) +
                           float(self.art_var.get()))

            # Calculate CGPA out of 5
            cgpa = total_marks / 140

            # Determine comments based on CGPA range
            if 4.80 <= cgpa <= 4.99:
                comments = "Outstanding Performance"
            elif 4.00 <= cgpa < 4.80:
                comments = "Excellent Performance"
            elif 3.00 <= cgpa < 4.00:
                comments = "Good Performance"
            elif 2.00 <= cgpa < 3.00:
                comments = "Satisfactory Performance"
            else:
                comments = "Need Improvement"

            # Save data to CSV
            self.save_to_csv(cgpa, total_marks, comments)

            # Display the results in a messagebox
            result_message = f"Total CGPA: {cgpa:.2f}\nTotal Subject Marks: {total_marks}\nComments: {comments}"
            messagebox.showinfo("Result", result_message)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_fields(self):
        # Clear all entry fields
        self.name_var.set("")
        self.id_var.set("")
        self.class_var.set("")
        self.section_var.set("")
        self.english_var.set("")
        self.math_var.set("")
        self.science_var.set("")
        self.social_science_var.set("")
        self.gk_var.set("")
        self.pe_var.set("")
        self.art_var.set("")

    def save_to_csv(self, cgpa, total_marks, comments):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        data = [current_datetime, self.name_var.get(), self.id_var.get(), self.class_var.get(),
                self.section_var.get(), self.english_var.get(), self.math_var.get(), self.science_var.get(),
                self.social_science_var.get(), self.gk_var.get(), self.pe_var.get(), self.art_var.get(),
                f"{cgpa:.2f}", total_marks, comments]

        # Check if the file exists, create headers if not
        file_exists = False
        try:
            with open("grade.csv", 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                headers = next(csv_reader)
                if headers:
                    file_exists = True
        except FileNotFoundError:
            pass

        # Write data to CSV
        with open("grade.csv", 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write headers if the file is newly created
            if not file_exists:
                headers = ["Timestamp", "Name", "ID", "Class", "Section",
                           "English", "Math", "Science", "Social Science",
                           "General Knowledge", "Physical Education", "Art",
                           "CGPA", "Total Marks", "Comments"]
                csv_writer.writerow(headers)

            csv_writer.writerow(data)

    def search_student(self):
        search_id = self.id_var.get()

        try:
            with open("grade.csv", 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                headers = next(csv_reader)

                for row in csv_reader:
                    if row[2] == search_id:
                        # If ID is found, populate the fields
                        self.name_var.set(row[1])
                        self.id_var.set(row[2])
                        self.class_var.set(row[3])
                        self.section_var.set(row[4])
                        self.english_var.set(row[5])
                        self.math_var.set(row[6])
                        self.science_var.set(row[7])
                        self.social_science_var.set(row[8])
                        self.gk_var.set(row[9])
                        self.pe_var.set(row[10])
                        self.art_var.set(row[11])
                        return

            # If ID is not found, show a message
            messagebox.showwarning("Student Not Found", f"No information found for ID: {search_id}")

        except FileNotFoundError:
            messagebox.showwarning("Database Error", "Database file not found.")

    def delete_student(self):
        search_id = self.id_var.get()

        try:
            with open("grade.csv", 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                headers = next(csv_reader)
                rows = list(csv_reader)

            # Check if ID is found in the data
            found = False
            for i, row in enumerate(rows):
                if row[2] == search_id:
                    found = True
                    del rows[i]
                    break

            if found:
                # Rewrite the CSV file without the deleted row
                with open("grade.csv", 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(headers)
                    csv_writer.writerows(rows)

                messagebox.showinfo("Delete Successful", f"Data for ID {search_id} has been deleted.")
                self.clear_fields()
            else:
                messagebox.showwarning("Student Not Found", f"No information found for ID: {search_id}")

        except FileNotFoundError:
            messagebox.showwarning("Database Error", "Database file not found.")
    
    def print_data(self):
        if not self.validate_input():
            return

        try:
            # Retrieve data from fields
            name = self.name_var.get()
            student_id = self.id_var.get()
            student_class = self.class_var.get()
            section = self.section_var.get()
            english_marks = float(self.english_var.get())
            math_marks = float(self.math_var.get())
            science_marks = float(self.science_var.get())
            social_science_marks = float(self.social_science_var.get())
            gk_marks = float(self.gk_var.get())
            pe_marks = float(self.pe_var.get())
            art_marks = float(self.art_var.get())

            # Calculate total subject marks out of 700
            total_marks = (english_marks + math_marks + science_marks +
                           social_science_marks + gk_marks + pe_marks + art_marks)

            # Calculate CGPA out of 5
            cgpa = total_marks / 140

            # Determine comments based on CGPA range
            if 4.80 <= cgpa <= 4.99:
                comments = "Outstanding Performance"
            elif 4.00 <= cgpa < 4.80:
                comments = "Excellent Performance"
            elif 3.00 <= cgpa < 4.00:
                comments = "Good Performance"
            elif 2.00 <= cgpa < 3.00:
                comments = "Satisfactory Performance"
            else:
                comments = "Need Improvement"

            # Create a PDF and write the information
            pdf_filename = f"Student_Report_{student_id}.pdf"
            c = canvas.Canvas(pdf_filename)
            c.setFont("Helvetica", 12)
            c.drawString(72, 800, f"Student Report - {name}")
            c.drawString(72, 780, f"ID: {student_id}")
            c.drawString(72, 760, f"Class: {student_class}")
            c.drawString(72, 740, f"Section: {section}")

            # Add marks for all subjects
            c.drawString(72, 720, f"English Marks: {english_marks}")
            c.drawString(72, 700, f"Math Marks: {math_marks}")
            c.drawString(72, 680, f"Science Marks: {science_marks}")
            c.drawString(72, 660, f"Social Science Marks: {social_science_marks}")
            c.drawString(72, 640, f"General Knowledge Marks: {gk_marks}")
            c.drawString(72, 620, f"Physical Education Marks: {pe_marks}")
            c.drawString(72, 600, f"Art Marks: {art_marks}")

            c.drawString(72, 580, f"Total Marks: {total_marks}")
            c.drawString(72, 560, f"CGPA: {cgpa:.2f}")
            c.drawString(72, 540, f"Comments: {comments}")

            c.save()

            messagebox.showinfo("PDF Created", f"Student information saved to {pdf_filename}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    def create_widgets(self):
        # Create a frame for better organization
        frame = ttk.Frame(self.root, padding=(20, 10))
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Labels and entry widgets
        ttk.Label(frame, text="Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="ID:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.id_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Class:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.class_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Section:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.section_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="English Marks:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.english_var).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Math Marks:").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.math_var).grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Science Marks:").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.science_var).grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Social Science Marks:").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.social_science_var).grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(frame, text="General Knowledge Marks:").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.gk_var).grid(row=8, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Physical Education Marks:").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.pe_var).grid(row=9, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Art Marks:").grid(row=10, column=0, sticky="w", padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.art_var).grid(row=10, column=1, padx=5, pady=5)

        # Search, Calculate, Clear, and Save Data Buttons
        ttk.Button(frame, text="Search", command=self.search_student).grid(row=11, column=0, pady=10, padx=5)
        ttk.Button(frame, text="Calculate", command=self.calculate_grades).grid(row=11, column=1, pady=10, padx=5)
        ttk.Button(frame, text="Clear", command=self.clear_fields).grid(row=11, column=2, pady=10, padx=5)
        ttk.Button(frame, text="Save Data", command=self.save_to_csv).grid(row=11, column=3, pady=10, padx=5)
        ttk.Button(frame, text="Delete Data", command=self.delete_student).grid(row=11, column=4, pady=10, padx=5)
        ttk.Button(frame, text="Print PDF", command=self.print_data).grid(row=11, column=5, pady=10, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentGradeCalculator(root)
    root.mainloop()
