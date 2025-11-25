import re
import statistics
from enum import Enum
from typing import Callable, Final, TypedDict


MENU_TEXT: Final[str] = """
--- Student Grade Analyzer ---
1. Add a new student
2. Add grades for a student
3. Generate a full report
4. Find the top student
5. Exit program
"""


# e.g. "John", "Mary Jane", "Jean-Luc", "O'Connor".
STUDENT_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[A-ZА-ЯЁ][A-Za-zА-Яа-яЁё]*(?:[\s'-][A-Za-zА-Яа-яЁё]+)*$"
)


class Student(TypedDict):
    """Student entity with a list of grades.

    Keys:
        name: Student name.
        grades: List of integer grades.
    """
    name: str
    grades: list[int]


class MenuOptionEnum(Enum):
    """Enumerates available menu options."""

    ADD_STUDENT = 1
    ADD_GRADES = 2
    SHOW_REPORT = 3
    SHOW_TOP_PERFORMER = 4
    EXIT = 5


def parse_choice(raw: str) -> int | None:
    """Converts raw input to a menu choice integer.

    Args:
        raw: User input string.

    Returns:
        Parsed integer choice or None if invalid.
    """
    try:
        return int(raw.strip())
    except ValueError:
        raise ValueError("Invalid input. Please enter a number.")


def parse_grade(raw: str) -> int | None:
    """Parses a grade string; handles 'done' and validation.

    Args:
        raw: User input string.

    Returns:
        Integer grade or None when the user enters 'done'.

    Raises:
        ValueError: If the value is not a number or is out of [0, 100].
    """
    raw = raw.strip()
    if raw.lower() == "done":
        return None
    value = validate_grade(raw)
    return value


def normalize_name(raw: str) -> str | None:
    """Normalizes a student name.

    Args:
        raw: Raw user input.

    Returns:
        Cleaned name string or None if empty after trimming.
    """
    name = " ".join(raw.split())
    if not name:
        return None
    return name


def validate_name(raw: str) -> str:
    """Validates and returns a normalized student name.

    Args:
        raw: Raw user input.

    Returns:
        Cleaned name string.

    Raises:
        ValueError: If the name is empty after trimming or contains invalid characters.
    """
    name = normalize_name(raw)
    if not name:
        raise ValueError("Name cannot be empty.")
    if not STUDENT_NAME_PATTERN.fullmatch(name):
        raise ValueError(
            "Name must start with a capital letter and contain only letters, spaces, apostrophes, or hyphens."
        )
    return name


def validate_grade(raw: str) -> int:
    """Validates and converts a grade string to int within [0, 100].

    Args:
        raw: Grade input string.

    Returns:
        Parsed grade integer.

    Raises:
        ValueError: If not a number or out of allowed range.
    """
    try:
        value = int(raw)
    except ValueError as e:
        raise ValueError("Invalid input. Please enter a number.") from e
    if value < 0 or value > 100:
        raise ValueError("Grade must be between 0 and 100.")
    return value


def get_student_by_name(name: str, students: list[Student]) -> Student:
    """Returns student by name (case-insensitive) if present.

    Args:
        name: Name to search.
        students: Collection of student records.

    Returns:
        Matching student or None if not found.
    """
    target = name.casefold()
    for student in students:
        if student["name"].casefold() == target:
            return student

    raise LookupError("Student not found.")


def get_average_grade(grades: list[int]) -> float | None:
    """Computes average grade or returns None if empty.

    Args:
        grades: List of integer grades.

    Returns:
        Mean grade as float or None when the list is empty.
    """
    if not grades:
        return None
    return statistics.mean(grades)


def get_student_report_line(student: Student) -> str:
    """Formats a single student's average line.

    Args:
        student: Student record.

    Returns:
        Human-readable line with average or N/A.
    """
    avg = get_average_grade(student["grades"])
    if avg is None:
        return f"{student['name']}'s average grade is N/A."
    return f"{student['name']}'s average grade is {avg:.1f}."


def get_top_performer(students: list[Student]) -> tuple[Student, float] | None:
    """Returns the student with the highest average, if any.

    Args:
        students: Collection of student records.

    Returns:
        Tuple of the best student and their average, or None if unavailable.
    """
    candidates: list[tuple[Student, float]] = []

    for student in students:
        avg = get_average_grade(student["grades"])
        if avg is not None:
            candidates.append((student, avg))

    if not candidates:
        return None

    best_student, best_avg = max(candidates, key=lambda item: item[1])

    return best_student, best_avg


def add_grades_for_student(student: Student) -> None:
    """Prompts for grades and appends them to the given student.

    Args:
        student: Student record to update.
    """
    while True:
        raw = input("Enter a grade (or 'done' to finish): ")
        try:
            grade = parse_grade(raw)
        except ValueError as e:
            print(f"Error: {e}")
            continue
        if grade is None:
            break
        student["grades"].append(grade)


def add_student(students: list[Student]) -> None:
    """Adds a new student.

    Args:
        students: Collection of student records to modify.

    Raises:
        ValueError: If the name is empty or already exists.
    """
    raw = input("Enter student name: ")

    name = validate_name(raw)

    if get_student_by_name(name, students):
        raise ValueError("Student already exists.")

    students.append(Student(name=name, grades=[]))
    print(f"Student {name} added.")


def add_grades(students: list[Student]) -> None:
    """Adds grades for a student.

    Args:
        students: Collection of student records.

    Raises:
        ValueError: If name is empty.
        LookupError: If student does not exist.
    """
    raw = input("Enter student name: ")

    name = validate_name(raw)

    student = get_student_by_name(name, students)
    if student:
        add_grades_for_student(student)


def aggregate_stats(students: list[Student]) -> tuple[float, float, float] | None:
    """Aggregates max/min/overall averages across students with grades.

    Args:
        students: Collection of student records.

    Returns:
        Tuple of (max, min, overall) averages or None if no grades exist.
    """
    averages = [avg for s in students if (avg := get_average_grade(s["grades"])) is not None]

    if not averages:
        return None

    max_avg, min_avg, overall = max(averages), min(averages), sum(averages) / len(averages)

    return max_avg, min_avg, overall


def do_report(students: list[Student]) -> list[str]:
    """Builds the full report lines, including summary if available.

    Args:
        students: Collection of student records.

    Returns:
        List of formatted report lines.
    """
    if not students:
        return ["No students available."]

    lines = ["--- Student Report ---"]
    for student in students:
        lines.append(get_student_report_line(student))

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

    return lines


def print_report(students: list[Student]) -> None:
    """Shows the full report.

    Args:
        students: Collection of student records.
    """
    for line in do_report(students):
        print(line)


def print_top_performer(students: list[Student]) -> None:
    """Shows the top performer.

    Args:
        students: Collection of student records.
    """
    result = get_top_performer(students)
    if not result:
        print("No top performer available.")
        return

    student, avg = result
    print(f"The student with the highest average is {student['name']} with a grade of {avg:.1f}.")


def do_exit()-> None:
    """Exits the program."""
    print("Exiting program.")
    exit(1)


def action_registry(students: list[Student]) -> dict[int, Callable[[], None]]:
    """Registry that maps menu choices to handlers.

    Args:
        students: Collection of student records shared across handlers.

    Returns:
        Mapping of menu choice integers to handler callables.
    """
    return {
        MenuOptionEnum.ADD_STUDENT.value: lambda: add_student(students),
        MenuOptionEnum.ADD_GRADES.value: lambda: add_grades(students),
        MenuOptionEnum.SHOW_REPORT.value: lambda: print_report(students),
        MenuOptionEnum.SHOW_TOP_PERFORMER.value: lambda: print_top_performer(students),
        MenuOptionEnum.EXIT.value: lambda: do_exit()
    }


def main() -> None:
    students = []
    actions = action_registry(students)

    while True:
        print(f"\n{MENU_TEXT}")
        try:
            choice = parse_choice(input("Enter your choice: "))
            handler = actions.get(choice, lambda: print(NotImplementedError("Warning: Invalid choice.")))
            handler()
        except (ValueError, LookupError) as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
