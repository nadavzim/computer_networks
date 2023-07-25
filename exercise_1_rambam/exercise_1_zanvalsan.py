import exer
def spread_to_digits(s): # a func that get the number string and cut it to the digits
    res = ""
    for letter in s:
        res += letter + ' ,'
    res = res[:-1]
    return res


def number_sum(s): # a func that get a number - by string, and return the sum of all the number digits
    digits_sum = 0
    for letter in s:
        digits_sum += int(letter)
    return digits_sum


NUmberLENGTH = 5
def main():

    number = input("Please enter a five digit number:\n")
    print("You entered the number: ", number)
    print("The digits of this number are:", spread_to_digits(number)) # send the number to the func that will slice the number into digits
    print("The sum of the digits is:", number_sum(number)) # send the number to the sum func and print the sum


if __name__ == '__main__':
   main()
