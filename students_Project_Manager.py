import json
import csv

class Student:
    def __init__(self, student_id, name, age, course):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.scores = []

    def average(self):
        if len(self.scores) == 0:
            return 0
        return sum(self.scores) / len(self.scores)

    def grade(self):
        score = self.average()

        if score >= 70:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 45:
            return "D"
        else:
            return "F"

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "scores": self.scores
        }
        
def save_students():
    with open("students.json", "w") as file:
        json.dump([s.to_dict() for s in students], file, indent=4)


def load_students():
    try:
        with open("students.json", "r") as file:
            records = json.load(file)

        for record in records:
            student = Student(
                record["student_id"],
                record["name"],
                record["age"],
                record["course"]
            )
            student.scores = record.get("scores", [])
            students.append(student)

    except FileNotFoundError:
        pass
    except json.JSONDecodeError:
        print("The student file is invalid. Starting with an empty list.")


def find_student(student_id):
    for student in students:
        if student.student_id == student_id:
            return student
    return None


def register_student():
    student_id = input("Enter student ID: ").strip()

    if not student_id:
        print("Student ID cannot be empty.")
        return

    if find_student(student_id):
        print("This student ID already exists.")
        return

    name = input("Enter student name: ").strip()

    try:
        age = int(input("Enter student age: "))
    except ValueError:
        print("Age must be a number.")
        return

    if age <= 0 or not name:
        print("Enter a valid age and name.")
        return

    course = input("Enter course: ").strip()

    if not course:
        print("Course cannot be empty.")
        return

    students.append(Student(student_id, name, age, course))
    save_students()
    print("Student registered successfully.")


def view_students():
    if not students:
        print("No students registered.")
        return

    for student in students:
        print(
            f"ID: {student.student_id} | "
            f"Name: {student.name} | "
            f"Age: {student.age} | "
            f"Course: {student.course} | "
            f"Average: {student.average():.2f} | "
            f"Grade: {student.grade()}"
        )


def search_student():
    student_id = input("Enter student ID to search: ").strip()
    student = find_student(student_id)

    if student:
        print(f"Name: {student.name}")
        print(f"Age: {student.age}")
        print(f"Course: {student.course}")
        print(f"Scores: {student.scores}")
        print(f"Average: {student.average():.2f}")
        print(f"Grade: {student.grade()}")
    else:
        print("Student not found.")


def update_student():
    student_id = input("Enter student ID to update: ").strip()
    student = find_student(student_id)

    if not student:
        print("Student not found.")
        return

    name = input("Enter new name (press Enter to keep current): ").strip()
    age_text = input("Enter new age (press Enter to keep current): ").strip()
    course = input("Enter new course (press Enter to keep current): ").strip()

    if name:
        student.name = name

    if age_text:
        try:
            age = int(age_text)
            if age <= 0:
                print("Age must be positive. Age unchanged.")
            else:
                student.age = age
        except ValueError:
            print("Invalid age. Age unchanged.")

    if course:
        student.course = course

    save_students()
    print("Student record updated.")


def delete_student():
    student_id = input("Enter student ID to delete: ").strip()
    student = find_student(student_id)

    if not student:
        print("Student not found.")
        return

    confirm = input("Are you sure you want to delete this student? (yes/no): ")

    if confirm.lower() == "yes":
        students.remove(student)
        save_students()
        print("Student deleted.")
    else:
        print("Deletion cancelled.")


def record_score():
    student_id = input("Enter student ID: ").strip()
    student = find_student(student_id)

    if not student:
        print("Student not found.")
        return

    try:
        score = float(input("Enter assessment score (0-100): "))
    except ValueError:
        print("Score must be a number.")
        return

    if score < 0 or score > 100:
        print("Score must be between 0 and 100.")
        return

    student.scores.append(score)
    save_students()
    print(f"Score recorded. Average: {student.average():.2f}")
    print(f"Grade: {student.grade()}")


def export_csv():
    with open("students.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Student ID", "Name", "Age", "Course",
            "Scores", "Average", "Grade"
        ])

        for student in students:
            writer.writerow([
                student.student_id,
                student.name,
                student.age,
                student.course,
                student.scores,
                round(student.average(), 2),
                student.grade()
            ])

    print("Student records exported to students.csv.")

students = []
load_students()

while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Register Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Record Score")
    print("7. Export to CSV")
    print("8. Save and Exit")

    choice = input("Choose an option: ")
    
    if choice == "1":
        register_student()
    elif choice == "2":
        view_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        update_student()
    elif choice == "5":
        delete_student()
    elif choice == "6":
        record_score()
    elif choice == "7":
        export_csv()
    elif choice == "8":
        save_students()
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please choose from 1 to 8.")
