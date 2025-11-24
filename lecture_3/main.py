import statistics
from typing import Callable, Final, TypedDict


class Student(TypedDict):
    """Student entity with a list of grades."""

    name: str
    grades: list[int]


MENU_TEXT: Final[str] = """
--- Student Grade Analyzer ---
1. Add a new student
2. Add grades for a student
3. Generate a full report
4. Find the top student
5. Exit program
"""


def show_error(message: str) -> None:
    """Prints a formatted error message."""
    print(f"Error: {message}")


def parse_choice(raw: str) -> int | None:
    """Converts raw input to menu choice integer."""
    try:
        return int(raw.strip())
    except ValueError:
        return None


def clean_name(raw: str) -> str | None:
    """Normalizes and validates a student name."""
    name = " ".join(raw.split())
    if not name:
        return None
    return name


def get_student_by_name(name: str, students: list[Student]) -> Student | None:
    """Returns student by name (case-insensitive) if present."""
    target = name.casefold()
    for student in students:
        if student["name"].casefold() == target:
            return student
    return None


def get_average_grade(grades: list[int]) -> float | None:
    """Computes average grade or returns None if empty."""
    if not grades:
        return None
    return statistics.mean(grades)


def student_report_line(student: Student) -> str:
    """Formats a single student's average line."""
    avg = get_average_grade(student["grades"])
    if avg is None:
        return f"{student['name']}'s average grade is N/A."
    return f"{student['name']}'s average grade is {avg:.1f}."


def get_top_performer(students: list[Student]) -> tuple[Student, float] | None:
    """Returns the student with the highest average, if any."""
    candidates: list[tuple[Student, float]] = []

    for student in students:
        avg = get_average_grade(student["grades"])
        if avg is not None:
            candidates.append((student, avg))

    if not candidates:
        return None

    best_student, best_avg = max(candidates, key=lambda item: item[1])

    return best_student, best_avg


def parse_grade(raw: str) -> int | None:
    """Parses a grade string; handles 'done' and validation."""

    raw = raw.strip()
    if raw.lower() == "done":
        return None
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError("Invalid input. Please enter a number.") from exc
    if value < 0 or value > 100:
        raise ValueError("Grade must be between 0 and 100.")
    return value


def add_grades_for_student(student: Student) -> None:
    """Prompts for grades and appends them to the given student."""
    while True:
        raw = input("Enter a grade (or 'done' to finish): ")
        try:
            grade = parse_grade(raw)
        except ValueError as err:
            show_error(str(err))
            continue
        if grade is None:
            break
        student["grades"].append(grade)


def aggregate_stats(students: list[Student]) -> tuple[float, float, float] | None:
    """Aggregates max/min/overall averages across students with grades."""
    averages = [avg for s in students if (avg := get_average_grade(s["grades"])) is not None]
    if not averages:
        return None

    max_avg = max(averages)
    min_avg = min(averages)
    overall = sum(averages) / len(averages)

    return max_avg, min_avg, overall


def format_report(students: list[Student]) -> list[str]:
    """Builds the full report lines, including summary if available."""
    if not students:
        return ["No students available."]

    lines = ["--- Student Report ---"]
    for student in students:
        lines.append(student_report_line(student))

    stats = aggregate_stats(students)
    if stats:
        max_avg, min_avg, overall = stats
        summary = (
            f"--------------------------\n"
            f"Max Average: {max_avg:.1f}\n"
            f"Min Average: {min_avg:.1f}\n"
            f"Overall Average: {overall:.1f}"
        )
        lines.extend(summary.splitlines())
    else:
        lines.append("No grades available.")
    return lines


def add_student(students: list[Student]) -> bool:
    """Adds a new student."""
    raw = input("Enter student name: ")

    name = clean_name(raw)
    if not name:
        raise ValueError("Name cannot be empty.")

    if get_student_by_name(name, students):
        raise ValueError("Student already exists.")

    students.append(Student(name=name, grades=[]))
    print(f"Student {name} added.")
    return True


def add_grades(students: list[Student]) -> bool:
    """Adds grades for a student."""
    raw = input("Enter student name: ")

    name = clean_name(raw)
    if not name:
        raise ValueError("Name cannot be empty.")

    student = get_student_by_name(name, students)
    if not student:
        raise LookupError("Student not found.")

    add_grades_for_student(student)
    return True


def show_report(students: list[Student]) -> bool:
    """Shows the full report."""
    for line in format_report(students):
        print(line)
    return True


def show_top_performer(students: list[Student]) -> bool:
    """Shows the top performer."""
    result = get_top_performer(students)
    if not result:
        print("No top performer available.")
        return True

    student, avg = result
    print(f"The student with the highest average is {student['name']} with a grade of {avg:.1f}.")

    return True


def exit_program() -> bool:
    """Exits the program."""
    print("Exiting program.")
    return False


def report_invalid_choice() -> None:
    """Reports an invalid menu selection."""
    show_error("Invalid choice. Please select a valid option.")


def action_registry(students: list[Student]) -> dict[int, Callable[[], bool]]:
    """Registry that maps menu choices to handlers."""
    # Each handler returns True to continue the loop or False to exit.
    def bind(action: Callable[[list[Student]], bool]) -> Callable[[], bool]:
        def handler() -> bool:
            return action(students)

        return handler

    return {
        1: bind(add_student),
        2: bind(add_grades),
        3: bind(show_report),
        4: bind(show_top_performer),
        5: exit_program,
    }


def main() -> None:
    students = []
    actions = action_registry(students)

    while True:
        print(f"\n{MENU_TEXT}")
        choice = parse_choice(input("Enter your choice: "))
        handler = actions.get(choice)
        if handler is None:
            report_invalid_choice()
            continue
        try:
            if not handler():
                break
        except (ValueError, LookupError) as err:
            show_error(str(err))


if __name__ == "__main__":
    main()
