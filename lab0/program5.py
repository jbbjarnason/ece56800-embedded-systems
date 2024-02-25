
birthdays = {
    "Albert Einstein": "14/03/1879",
    "Benjamin Franklin": "17/01/1706",
    "Ada Lovelace": "10/12/1815"
}

print("Welcome to the birthday dictionary. We know the birthdays of:")
for name in birthdays:
    print(name)

name = input("Who's birthday do you want to look up?\n")
if name in birthdays:
    print(f"{name}'s birthday is {birthdays[name]}")
