import re

def remove_invalid_filename(filename):
    return re.sub('[^\w\-_\. ]', '_', filename)