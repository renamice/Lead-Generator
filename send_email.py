import json
import os
import shutil

from config import EMAIL_FOLDER, SENT_EMAIL


def main():
    init()


def init():
    email_files = []
    for file in os.listdir(EMAIL_FOLDER):
        if file.endswith("json"):
            email_files.append(file)

    for log in email_files:
        file_path = os.path.join(EMAIL_FOLDER, log)

        with open(file_path, "r") as f:
            email_data = json.load(f)

        send_to = email_data["email"][0]
        subject = email_data["subject"]
        body = email_data["body"]

        if send_email(send_to, subject, body):
            new_path = os.path.join(SENT_EMAIL, log)
            shutil.move(file_path, new_path)
            print(f"Moved '{log}' to {SENT_EMAIL}")


# String String String -> Boolean
def send_email(address, subject, body):
    os.makedirs(SENT_EMAIL, exist_ok=True)

    # TODO: send to the address specified

    # TODO: print a log of whether the email was sent or not

    # TODO: return true if success
    return False


if __name__ == "__main__":
    main()
