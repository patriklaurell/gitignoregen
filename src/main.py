import requests
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.auto_suggest import Suggestion
from prompt_toolkit.validation import Validator, ValidationError

api_url = "https://www.toptal.com/developers/gitignore/api"


def main():

    # Define custom key bindings
    bindings = KeyBindings()

    keywords = requests.get(f"{api_url}/list").text.replace("\n", ",").split(",")

    session = PromptSession(
        complete_while_typing=True,
        completer=FuzzyCompleter(WordCompleter(keywords, ignore_case=True)),
        validator=Validator.from_callable(
            lambda text: text in keywords or text == "",
            error_message="Invalid keyword. Please select from the completer.",
            move_cursor_to_end=True,
        ),
    )

    chosen_keywords = []

    print(
        "Please enter the languages and operating systems you will use. Enter to generate."
    )

    while True:
        try:
            # Prompt the user for input with the completer and custom key bindings
            user_input = session.prompt(
                "> ",
                key_bindings=bindings,
            )

            if user_input == "":
                confirm = input("Confirm generation? (Y/n): ")

                if confirm == "y" or confirm == "" or confirm == "Y":
                    break
                else:
                    print("Exiting...")
                    return
            else:
                chosen_keywords.append(user_input)  # No need to append ", " here
        except KeyboardInterrupt:
            return  # Exit on Ctrl+C
        except EOFError:
            return  # Exit on Ctrl+D

    print("Generating...")
    response = requests.get(f"{api_url}/{','.join(chosen_keywords)}")

    with open(".gitignore", "w") as f:
        f.write(response.text)


if __name__ == "__main__":
    main()
