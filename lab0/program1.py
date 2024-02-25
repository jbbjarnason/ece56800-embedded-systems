
from datetime import datetime

name = input("What is your name: ")
age = int(input("How old are you: "))

# get current year
current_year = datetime.now().year

print(f"{name} will turn 100 years old in either {current_year + 100 - age - 1} or {current_year + 100 - age}")
