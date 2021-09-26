import random
player1 = 0
player2 = 0
player3 = 0
currentTurn = 1
currentWord = ""
round = 1
bank = [0, 0, 0]
roundPrize = [1000, 2000, 3000]
roundHint = ["Adjective", "A thing", "A TV show"]
randWord = ["labyrinthine", "paddleboard", "bachelorette"]
currentBoard = ["_"] * len(randWord[0])
roundFinished = False
vowelList = []
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# This function randomly generates a wheel entry as per the Wheel of Fortune actual rules
def spinWheel():
    wheelOptions = [300, 500, 450, 500, 800, "Lose a Turn", 700, 1000, 650, "Bankrupt", 900,
                    500, 350, 600, 500, 400, 550, 800, 300,
                    700, 900, 500, 5000, 950]
    return random.choice(wheelOptions)


# This function finds a given character and sets the board so that the character has been guessed
def checkChar(guess):
    global currentWord
    global currentBoard
    correctGuess = False
    for i in range(len(currentWord)):
        if currentWord[i:i + 1] == guess:
            currentBoard[i] = guess
            correctGuess = True
    return correctGuess

# This function initializes the board at the start of each round
def initializeBoard():
    global currentBoard
    currentWord = randWord[round - 1]
    currentBoard = ["_"] * len(currentWord)

def incrementTurn():
    global currentTurn
    if currentTurn == 1 or currentTurn == 2:
        currentTurn += 1
    elif currentTurn == 3:
        currentTurn = 1

def takeTurn():
    global roundFinished
    global vowelList
    done = False
    while not done:
        print("Player %i, you have $%i" % (currentTurn, bank[currentTurn - 1]))
        print("The category for this round is: %s" % roundHint[round - 1])
        print("The word is: %s" % currentWord)
        print("The board looks like:")
        printList(currentBoard)
        initialChoice = int(input("""Player %i, what would you like to do?
        1. Guess the word
        2. Guess a consonant
        3. Buy a vowel
        Your selection here: """ % currentTurn))
        if initialChoice == 1:
            wordChoice = str(input("Please input the word: ")).lower()
            if wordChoice == currentWord:
                bank[currentTurn - 1] += roundPrize[round - 1]
                print("You won this round! Your bank is now $%i" % bank[currentTurn - 1])
                done = True
                return True
            else:
                print("Sorry, that's not the puzzle. Your turn is over.")
                done = True
        elif initialChoice == 2:
            rolledPrize = spinWheel()
            print("You rolled %s" % str(rolledPrize))
            if rolledPrize == "Bankrupt":
                print("Sorry, your turn is over.")
                bank[currentTurn - 1] = 0
                break
            elif rolledPrize == "Lose a Turn":
                print("Sorry, your turn is over.")
                break
            guess = str(input("Please guess a consonant: ")).lower()
            if not checkChar(guess):
                print("Sorry, that's not the consonant. Your turn is over.")
                done = True
            else:
                print("Nice job, time to go again.")
                bank[currentTurn - 1] += rolledPrize
        elif initialChoice == 3:
            if bank[currentTurn - 1] >= 250:
                print("Please input a vowel from the following list:")
                printVowels(vowelList)
                vowelInput = str(input("Your vowel choice here: ")).lower()
                vowelList.remove(vowelInput.upper())
                bank[currentTurn - 1] = bank[currentTurn - 1] - 250
                inWord = checkChar(vowelInput)
                if inWord:
                    print("Nice job, time to go again.")
                else:
                    print("Sorry, that vowel isn't in the word. Your turn is over.")
                    done = True
            else:
                print("Sorry, you only have $%i, you can't buy a vowel, pick another option." % bank[currentTurn - 1])

# We use this function to display the current board in a readable fashion
def printList(wordList):
    for i in range(len(wordList)):
        print(wordList[i], end = '')
    print("\n")

# This function displays the list of vowels
def printVowels(wordList):
    for i in range(len(wordList) - 1):
        print(wordList[i] + ",", end = '')
    print(wordList[len(wordList)- 1])
    print("\n")

# This function is run to reinitialize the list of vowels after each round
def beginRound():
    global vowelList
    global currentWord
    print("It is round %i!" % round)
    currentWord = randWord[round - 1]
    vowelList = ["A", "E", "I", "O", "U"]
    initializeBoard()

# This function loops through each player's turn until someone wins
def playRound():
    roundFinished = False
    while not roundFinished:
        roundFinished = takeTurn()
        incrementTurn()

#We use this function to find the player with the highest winnings so they can go to the final round
def getMax():
    global bank
    maximum = 0
    maxPlayer = 1
    for i in range(3):
        if bank[i] > maximum:
            maximum = bank[i]
            maxPlayer = i
    return maxPlayer

# This function handles the entirety of the final round. Since the final round setup is so different from the
#other rounds, this seemed like the best approach
def finalRound():
    global currentWord
    global currentBoard
    finalPlayer = getMax() + 1
    print("""Congratulations, player %i! 
    You have advanced to the final round! You will be given a word where R, S, T, L, N, E are filled in. You
    will input three consonants and a vowel (all at no cost, which does not reveal anything else). 
    You then must guess the word in one guess. Here is the final word with those letters filled in: \n""" % finalPlayer)
    currentWord = randWord[2]
    print(currentWord)
    currentBoard = ["_"] * len(currentWord)
    #We substitute in the characters that are automatically given
    checkChar("e")
    checkChar("s")
    checkChar("t")
    checkChar("l")
    checkChar("n")
    checkChar("r")
    printList(currentBoard)
    #We ask the user to input their desired expressions
    cons1 = str(input("Select your first consonant."))
    cons2 = str(input("Select your second consonant."))
    cons3 = str(input("Select your third consonant."))
    vowel1 = str(input("Select your vowel."))

    checkChar(cons1)
    checkChar(cons2)
    checkChar(cons3)
    checkChar(vowel1)
    print("Here is the board with your selections:")
    printList(currentBoard)
    finalGuess = str(input("What is your final guess? Input it here: "))
    print(currentWord)
    if finalGuess == currentWord:
        bank[finalPlayer - 1] += 3000
        print("You won Wheel of Fortune! You won $%i net winnings!" % bank[finalPlayer - 1])
    else:
        print("You lost Wheel of Fortune! You still get $%i in net winnings, though." % bank[finalPlayer - 1])
    print("You can check the CSV to see everyone's final winnings!")

# This function uses file i/o to write each participant's final score to the file
def writeFile():
    f = open("gameResults.csv", "w")
    f.write("Participant, Winnings ($)\n")
    for i in range(3):
        f.write(str(i+1) + "," + str(bank[i]) + "\n")
    f.close()

if __name__ == '__main__':
    while round < 3:
        beginRound()
        playRound()
        round += 1
    finalRound()
    writeFile()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
