
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Can't divide by zero")

def power(a, b):
    return a**b