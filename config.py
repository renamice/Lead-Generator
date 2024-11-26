# INSTAGRAM
RESULTS = 0  # used when file run indivdually
FIELD = ""  # used when file run indivdually
LOCATION = ""  # used when file run indivdually
INSTAGRAM_PROMPT = """
Generate an email for {name}.
Instagram handle: {handle}.
Bio: {bio}.
- Include warm feeling towards them.
Include a subject at the top as "Subject: "
And continue the email after that from the next line.
"""

# PROGRAM
AI_MODEL = "llama2"
LEADFOLDER = "leads"
EMAIL_FOLDER = "email-generated"
SENT_EMAIL = "email-sent"
