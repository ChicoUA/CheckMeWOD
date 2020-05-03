def check_close(pos1, pos2):
    if pos2 - 20 <= pos1 <= pos2 + 20:
        return True
    else:
        return False


def check_close2(pos1, pos2):
    if pos2 - 200 <= pos1 <= pos2 + 200:
        return True
    else:
        return False


def check_close3(pos1, pos2):
    if pos2 - 30 <= pos1 <= pos2 + 30:
        return True
    else:
        return False