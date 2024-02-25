
import random

number = random.randint(0, 10)

for i in range(3):
    guess = int(input("Enter your guess:"))
    if guess == number:
        print("You win!")
        exit()

print(f"You lose!")
