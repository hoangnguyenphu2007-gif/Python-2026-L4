def bai1():
    radius = float(input("Enter circle radius? "))
    area = 3.14 * radius * radius
    print("Circle area =", area)

def bai2():
    celsius = input("Enter the temperature in Celsius? ")
    fahrenheit = float(celsius) * 9 / 5 + 32
    print(celsius, "(C) =", fahrenheit, "(F)")

def bai3() :
    num = int(input("Enter a number? "))
    is_prime = True

    if num < 2:
        is_prime = False
    else:
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break

    if is_prime:
        print(num, "is a prime number")
    else:
        print(num, "is a NOT prime number")

def bai4() :
    num = int(input("Enter a number? "))
    total = 0

    for i in range(1, num):
        if num % i == 0:
            total += i

    if total == num:
        print(num, "is a perfect number")
    else:
        print(num, "is a NOT perfect number")

def bai5():
    colors = ["White", "Black", "Blue", "Red", "Yellow"]
    favorite = input("What is your favorite color? ")

    if favorite in colors:
        index = colors.index(favorite)
        print("Your color is at index", index, "in my list")
    else:
        print("Sorry, I could not find your color")

def bai6():
    range1 = list(range(0, 7))
    range2 = list(range(1, 11, 3))
    range3 = list(range(5, 0, -1))
    range4 = list(range(6, -3, -2))

    print("range1:", range1)
    print("range2:", range2)
    print("range3:", range3)
    print("range4:", range4)

def remove_dollar_sign(s):
    return s.replace("$", "")

print(remove_dollar_sign("$100"))       
print(remove_dollar_sign("$1$2$3"))    

def extract_even(l):
    result = []
    for num in l:
        if num % 2 == 0:
            result.append(num)
    return result

print(extract_even([1, 4, 5, -1, 10]))   

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(factorial(5))    
print(factorial(0))    

def get_divisors(n):
    divisors = []
    for i in range(1, n + 1):
        if n % i == 0:
            divisors.append(i)
    return divisors

print(get_divisors(28))  

import math

def bai11():
    x1 = float(input("Enter x1: "))
    y1 = float(input("Enter y1: "))
    x2 = float(input("Enter x2: "))
    y2 = float(input("Enter y2: "))

    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    print("The distance between the two points is", distance)

def print_pattern(m, n):
    for row in range(m):
        for col in range(n):
            if row == 0 or row == m - 1 or col == 0 or col == n - 1:
                print("*", end=" ")
            else:
                print(" ", end=" ")
        print()

print_pattern(4, 5)


bai1()
bai2()
bai3()
bai4()
bai5()
bai6()
print(remove_dollar_sign("$100"))        
print(extract_even([1, 4, 5, -1, 10]))   
print(factorial(5))                      
print(get_divisors(28))                                    
bai11()
print_pattern(4, 5)   
