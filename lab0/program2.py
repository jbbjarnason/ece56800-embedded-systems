
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
print(f"a = {a}")

number = int(input("Enter number: "))

b = [i for i in a if i < number]

print(f"The new list is {b}")
