
number = int(input("How many Fibonacci numbers would you like to generate? "))

fibonacci = []
while number > 0:
    number = number - 1
    if len(fibonacci) < 2:
        fibonacci.append(1)
    else:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])

print(f"The Fibonacci Sequence is {str(fibonacci)[1:-1]}")
