import sys

import generate_email
import insta_leads
import send_email


def main():
    if len(sys.argv) != 5:
        print_help()
        exit()

    media = sys.argv[1]
    field = sys.argv[2]
    area = sys.argv[3]
    try:
        amount = int(sys.argv[4])
    except:
        print_help()
        exit(1)

    data = []
    filepath = ""
    # Generating leads
    if media == "instagram":
        filepath = insta_leads.init(field, area, amount)
    # You can add other medias here

    # Generating emails
    generate_email.init(filepath)

    # Sending emails
    send_email.init()


# ->
# prints out help
def print_help():
    print(
        f"""
    Usage: python {sys.argv[0]} [site] [field] [location] [amount]
    
    [site]:     instagram
    [field]:    occupation you want to target
    [location]: area you want to target
    [amout]:    number of leads you want to search for
    """
    )


if __name__ == "__main__":
    main()
