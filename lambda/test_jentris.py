from jentris import Jentris
import json
import prompts


def do_test():
    """Provided for simple testing of the Jentri's class functionality, and localisation"""
    locale = "en"

    # Localized strings stored in language_strings.json
    with open("language_strings.json") as language_prompts:
        language_data = json.load(language_prompts)

    # Set default translation data to broader translation
    data = language_data[locale[:2]]
    # If a more specialized translation exists, then select it instead
    # example: "fr-CA" will pick "fr" translations first, but if "fr-CA" translation exists,
    #          then pick that instead
    if locale in language_data:
        data.update(language_data[locale])

    jentris = Jentris()
    print(f"{data[prompts.JENTRIS_IS_ON]} {jentris.jentris_date_text}")
    print(f"{data[prompts.THERE_ARE]} {jentris.jentris_sleeps} {data[prompts.SLEEPS_UNTIL]}")


# Run the main function
if __name__ == '__main__':
    do_test()
