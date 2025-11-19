from typing import Final

CURRENT_YEAR: Final[int] = 2025
EXIT_COMMAND: Final[str] = "stop"


def generate_profile(age: int) -> str:
    """Determines the life stage based on the given age."""
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    else:
        return "Adult"


if __name__ == "__main__":
    # gather basic user information
    user_name = input("Enter your full name: ")
    birth_year_str = input("Enter your birth year: ")

    birth_year = int(birth_year_str)

    current_age = CURRENT_YEAR - birth_year

    hobbies: list[str] = []

    # collect hobbies until user types 'stop'
    while True:
        hobby_input = input("Enter a favorite hobby or type 'stop' to finish: ")

        if hobby_input.casefold() == EXIT_COMMAND:
            break

        hobbies.append(hobby_input)

    life_stage = generate_profile(current_age)

    user_profile = {
        "name": user_name,
        "age": current_age,
        "stage": life_stage,
        "hobbies": hobbies
    }

    # display final summary
    print("---")
    print("Profile Summary:")
    print(f"Name: {user_profile['name']}")
    print(f"Age: {user_profile['age']}")
    print(f"Life Stage: {user_profile['stage']}")

    if not user_profile["hobbies"]:
        print("You didn't mention any hobbies.")
    else:
        print(f"Favorite Hobbies ({len(user_profile['hobbies'])}):")
        for hobby in user_profile["hobbies"]:
            print(f"- {hobby}")

    print("---")