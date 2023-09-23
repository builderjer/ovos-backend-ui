def seralize(string):
    """Takes a string returned from backend crud and converts it to a list"""
    string = string.strip()
    for ch in "[]\'":
        string = string.replace(ch, '')
    string = list(string.split(","))
    return string
