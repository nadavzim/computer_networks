def check_input(s):  # a func that check if the input is valid - return true
    if type(s) is not str:
        return False
    if not s.isdigit():
        return False
    elif len(s) != NUMBER_LENGTH:
        return False
    else:
        return True


def spread_to_digits(s):  # a func that get the number string and cut it to the digits
    if check_input(s) is False:
        return False, ''
    else:
        res = ""
        for letter in s:
            res += letter + ', '
        res = res[:-2]
        return True, res


def number_sum(s):  # a func that get a number - by string, and return the sum of all the number digits
    if check_input(s) is False:
        return False, ''
    else:
        digits_sum = 0
        for letter in s:
            digits_sum += int(letter)
        return True, digits_sum


NUMBER_LENGTH = 5
INVALID_MSG = "the function only get a string of five digit's, invalid arguments given  "


def main():
    assert (check_input('')) is False
    assert (check_input('123456')) is False
    assert (check_input("1234")) is False
    assert (check_input("12-34")) is False
    assert (check_input("12345")) is True

    assert spread_to_digits("") == (False, '')
    assert spread_to_digits("@#$%&") == (False, '')
    assert spread_to_digits("apple") == (False, '')
    assert spread_to_digits("1234") == (False, '')
    assert spread_to_digits("123456") == (False, '')
    assert spread_to_digits("12345") == (True, '1, 2, 3, 4, 5')

    assert number_sum("") == (False, '')
    assert number_sum("apple") == (False, '')
    assert number_sum("@@@@@") == (False, '')
    assert number_sum("1234") == (False, '')
    assert number_sum("123456") == (False, '')
    assert number_sum("12345") == (True, 15)

    number = input("Please enter a five digit number:\n")
    while not check_input(number):
        print("you have entered invalid input.")
        number = input("Please enter a five digit number:\n")
    print("You entered the number: ", number)

    valid, number_in_digits = spread_to_digits(number)
    # send the number to the func that will slice the number into digits and check if it valid number in string
    if valid:
        print("The digits of this number are: " + number_in_digits)
    else:
        print(INVALID_MSG)

    valid, sum_of_digits = number_sum(number)
    if valid:
        print("The sum of the digits is:", sum_of_digits)
        # send the number to the sum func and print the sum and check if the number is five digits in string
    else:
        print(INVALID_MSG)


if __name__ == '__main__':
    main()
