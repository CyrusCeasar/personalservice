import re


def isEmail(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)


