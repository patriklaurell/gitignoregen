import requests
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import FuzzyCompleter, WordCompleter


def main():
    session = PromptSession()

    keywords = (
        requests.get("https://www.toptal.com/developers/gitignore/api/list")
        .text.replace("\n", ",")
        .split(",")
    )

    chosen_keywords = []

    # Create a completer with the keywords
    keyword_completer = FuzzyCompleter(WordCompleter(keywords, ignore_case=True))

    print("Please enter the languages and operating systems you will use.")

    while True:
        try:
            # Prompt the user for input with the completer
            user_input = session.prompt("> ", completer=keyword_completer)

            if user_input == "":
                print("Confirm generation? (Y/n)")
                confirm = session.prompt("> ")

                if confirm == "y" or confirm == "" or confirm == "Y":
                    break
                else:
                    print("Exiting...")
                    return
            else:
                chosen_keywords.append(user_input)
        except KeyboardInterrupt:
            return  # Exit on Ctrl+C
        except EOFError:
            return  # Exit on Ctrl+D

    print("Generating...")
    response = requests.get(
        f"https://www.toptal.com/developers/gitignore/api/{','.join(chosen_keywords)}"
    )

    with open(".gitignore", "w") as f:
        f.write(response.text)


if __name__ == "__main__":
    main()
