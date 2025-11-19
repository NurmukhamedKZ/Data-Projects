def add(a,b):
    return a + b
def subtract(a,b):
    return a - b
def multiply(a,b):
    return a * b
def divide(a,b):
    return a / b

num1 = input("enter first number: ")
num2 = input("enter second number: ")

if num1.isdigit() and num2.isdigit():
    num1 = float(num1)
    num2 = float(num2)
    print("Select operation.")
    print("1.Add\n2.Subtract\n3.Multiply\n4.Divide\n")
    choice = input("Enter choice(1/2/3/4): ")
    if choice == '1':
        print(num1,"+",num2,"=", add(num1,num2))
    elif choice == '2':
        print(num1,"-",num2,"=", subtract(num1,num2))
    elif choice == '3':
        print(num1,"*",num2,"=", multiply(num1,num2))
    elif choice == '4':
        if num2 != 0:
            print(num1,"/",num2,"=", divide(num1,num2))
        else:
            print("Error! Division by zero.")
    else:
        print("Invalid input")
else:
    print("type correct numbers")
