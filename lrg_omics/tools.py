from datetime import date


def today():
    return date.today().strftime("%y%m%d")
