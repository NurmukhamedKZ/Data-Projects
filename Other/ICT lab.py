def calculate_factorial(n):
    if n < 0:
        print("Factorial is not defined for negative numbers.")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
    
num1 = input("Enter a number: ")
try:
    num = int(num1)
    factorial = calculate_factorial(num)
    if factorial is not None:
        print(f"Factorial of {num} is {factorial}.")
except ValueError:
    print("Please enter a valid integer.")
