import getpass
import re
import random
import csv
import sys

# Initialise variables
points = 0
password = "ele"

# Function to check if numbers present
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def endGame(points):
    scoreboard = []
    # Write score to scoreboard
    with open("scoreboard.csv", "ab") as scoreboardFile:
        scoreboardWriter = csv.writer(scoreboardFile)
        scoreboardWriter.writerow([name, points])
    # Open scoreboard in read mode and store in memory
    scoreboardFile = open("scoreboard.csv", "rt")
    scoreboardReader = csv.reader(scoreboardFile)
    for i in scoreboardReader:
        scoreboard.append([i[0], int(i[1])])
    print("Game over!")
    print("Well done " + str(name) + ", you got " + str(points) + " points.")
    print("")
    print("Top 5:")
    # Sort list
    scoreboardSorted = sorted(scoreboard, key = lambda x: x[1])
    scoreboardSorted.reverse()
    # Print first 5
    i = 1
    for score in scoreboardSorted:
        print(str(score[0]) + ": " + str(score[1]) + " points")
        i = i + 1
        if i == 5:
            break
    sys.exit()

# Function to turn song name into usable string
def clean(song):
    cleaned = song.lower()
    cleaned = cleaned.strip()
    cleaned = re.sub(" +", " ", cleaned)
    return str(cleaned)

# Function to return first character of each word in song name
def songNameFormat(song):
    finalString = ""
    words = song.split()
    for word in words:
        ind = 1
        for letter in word:
            if(ind == 1):
                finalString = finalString + letter
            else:
                finalString = finalString + "_"
            ind = ind + 1
        finalString = finalString + " "
    return finalString

# Ask for password until correct
while(True):
    password_attempt = getpass.getpass()
    if(password_attempt == password):
        break # Break out of loop
    else:
        print("Incorrect password. Try again.")

# Open CSV file and load into list 'songDB'
SongFile = open("database.csv", "rt")
fileReader = csv.reader(SongFile)
songDB = []

# Put records from database into list
for row in fileReader:
    songDB.append(row)

# Ask for name with validation
name = raw_input("What is your name? ")
while(True):
    if str(name) == "" or hasNumbers(name):
        print("Incorrect name entered. Try again.")
        name = raw_input("What is your name? ")
    else:
        break

while(True):
    # Select random song and put into current song list
    song = []
    if len(songDB) > 0:
        randInd = random.randint(0, len(songDB)-1)
        song.append(songDB[randInd][0])
        song.append(songDB[randInd][1])
        songDB.pop(randInd)
        tries = 1
        print(songNameFormat(song[1]))
        print("By: " + str(song[0]))
        # Keep on asking for song name
        while(True):
            songAttempt = raw_input("Enter the full song name: ")
            songAttempt = clean(songAttempt)
            # Check if nothing is entered
            while(songAttempt == ""):
                print("You entered nothing. Try again: ")
                songAttempt = raw_input("Enter the full song name: ")
                songAttempt = clean(songAttempt)
            # If song is correctly guessed, check number of tries
            if(songAttempt == clean(song[1])):
                if(tries == 1):
                    points = points + 3
                    print("Points: " + str(points))
                    break
                elif(tries == 2):
                    points = points + 1
                    print("Points: " + str(points))
                    break
            else:
                print("Incorrect answer.")
                tries = tries + 1
                if(tries > 2):
					print("The correct answer was " + str(song[1]))
                    endGame(points)
                else:
                    pass
    else:
        print("You've gone through every song in the database, that's it! Well done! You made it!")
        endGame(points)
