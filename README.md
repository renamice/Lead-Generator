
# Lead Generator

Generates leads only from instagram for now.
It is easy to find email on insta bio, so that is why it got done first and quick.


Linkedin and Google maps don't give out emails.
Linkedin requires premium, not worth it. APIs are ridiculous too.

`TODO`: Make the app send emails. I've left that up to you. Everything else works fine.

Also, I am not sure about using googlesearch, that thing kept banning IP while I was tring to test this thing.
You might want to look into that.

### SETUP:
1. Install ollama and pull a `model`.
2. Place this `model` name in place as `AI_MODEL` in `config.py`.
3. Install the requirements.
4. Cross your fingers and hope it works.

### Modifications
I have written the codebase in a redable way, so might be helpful.

Other than that, you can easily add new scrapers:
1. Create a python file with that scraper/lead generator.
2. Add a handler for this on `generate_email.py`
3. Update the `print_help()` on `main.py`

### Integrating
The `main.py` file should serve as an example to how you can build an app around it.
