import unicodedata
import re
import string, random


def slugify(value, allow_unicode=False, to_lower=True):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def clean_string(value, allow_unicode=False):
    """ Clean string for write in DB """
    # TODO: implement
    return value

def clean_filename(value, allow_unicode=False):
    # TODO: clean the value to produce a valid filename (with extension)
    return value


def random_alphanumeric(length: str = 32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))