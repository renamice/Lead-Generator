import json
import os
import re
import sys
from datetime import datetime

from langchain_ollama import OllamaLLM

from config import AI_MODEL, EMAIL_FOLDER, INSTAGRAM_PROMPT

LLM = OllamaLLM(model=AI_MODEL)


def main():
    if len(sys.argv) != 2:
        print("put a filename at the end too.")
        exit(1)
    init(sys.argv[1])


def init(filepath):
    data = load_file(filepath)
    if data == None:
        print("Error: couldn't load file")
        exit(1)

    metadata = data[0]
    data = remove_metadata(data)
    if metadata["platform"] == "instagram":
        generate_email_instagram(data)


# list ->
# takes in list of dictionary each containing a profile and generates and logs the personalized emails
def generate_email_instagram(data):
    for profile in data:
        session = {}
        session["email"] = profile["email"]
        prompt = INSTAGRAM_PROMPT.format(
            name=profile["name"], handle=profile["handle"], bio=profile["bio"]
        )
        answer = LLM.invoke(prompt)
        email = extract_subject(answer)
        session["prompt"] = prompt
        session["subject"] = email["subject"]
        session["body"] = email["body"]

        log_session(session, profile["name"])


# dictionary ->
# takes in a dictionary containig session informationa and saves it into a json file for logging purposes and later use while sending.
def log_session(session, email_to):
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    file_name = f"{timestamp} {email_to}.json"

    os.makedirs(EMAIL_FOLDER, exist_ok=True)
    file_path = os.path.join(EMAIL_FOLDER, file_name)

    with open(file_path, "w") as json_file:
        json.dump(session, json_file, indent=4)

    print(f"Saved email log at {file_path}")


# String -> Dictionary
# returns the Subject and body of email as two different items
def extract_subject(email):
    subject_pattern = r"Subject:\s*(.+?)\n"

    content = {}
    subject = re.search(subject_pattern, email).group(1).strip()
    body = body = re.sub(subject_pattern, "", email, count=1).strip()

    content["subject"] = subject
    content["body"] = body

    return content


# list -> list
# removes the first item of the list which is for info about the file
def remove_metadata(data):
    return data[1:]


# String -> list
# takes a filename as input and returns the content int a list
def load_file(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {filename}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON. {e}")
        return None


if __name__ == "__main__":
    main()
