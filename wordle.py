# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 12:31:45 2022

@author: Amanda
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Get the list of words
wordList = np.loadtxt("WordleList", dtype=str, delimiter="\t", skiprows=1, usecols=2)
for i in range(len(wordList)):
    wordList[i] = wordList[i].lower()

#split the word list into possible answers and accepted guesses    
answerList = wordList[0:2315]
guessList = wordList[2316:12971]

#create an array with the alphabet
alphabet = np.array(('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'))


#count how many times a letter appears in a word, and also how many times a letter appears in a given position
def countLetters(alphabet, answerList): 
    counts = np.zeros((len(alphabet), 6), dtype=int)
    for word in answerList:
        for letter in alphabet:
            for i in range(0, 5):
                if (word[i] == letter):
                    index = np.where(alphabet==letter)
                    counts[index, 0] += 1
                    counts[index, i+1] += 1
    return counts

#show a heatmap of the counts of letters at different positions
def plotCounts(letterCounts, alphabet):
    plt.figure(figsize=(15, 15))
    ax = sns.heatmap(letterCounts[0:len(alphabet), 1:6], square=True, linewidths=0.5, annot=True, fmt='g', yticklabels=alphabet, xticklabels=[1, 2, 3, 4, 5])
    plt.xlabel("Position in Word")
    plt.ylabel("Letter")
    plt.title("Counts of Letter Positions in Wordle Answers")
    plt.show()
    return

#calculate a score for each letter
def calculateScores(alphabet, answerList, letterCounts):
    scores = np.zeros_like(answerList, dtype=int)
    for w in range(len(answerList)):
        word = str(answerList[w])
        for i in range(0, 5):
            index = np.where(alphabet==word[i])
            scores[w] = scores[w] + letterCounts[index, i+1]
    return scores


letterCounts = countLetters(alphabet, answerList)
wordScores = calculateScores(alphabet, answerList, letterCounts)

#the word with the highest score is the best guess
maximumScoreLoc = np.argmax(wordScores)
bestWord = answerList[maximumScoreLoc]
print("The best first guess to maximize green letters is", bestWord.upper(), "with a score of", wordScores[maximumScoreLoc])


def getResults(answerList, bestWord):
    #ask user "what was the result for letter 1? Green, Grey, or Yellow?
    for i in range(1, 6):
        print("Was letter", i, "green, yellow, or grey?")
        letterResult = input("Type the result here: ")
        if (letterResult == "Green" or letterResult == "green"):
            print("Ok, letter", i, "was green.") 
            #remove all words from the answer list that don't have that letter in that position
            for w in range(0, len(answerList)):
                check = 0
                if (w >= len(answerList)):
                    break
                while (check == 0):
                    if (w >= len(answerList)):
                        break
                    if (answerList[w][i-1] != bestWord[i-1]):
                        answerList = np.delete(answerList, w)
                    else:
                        check = 1        
            print("Answer list updated. There are now", len(answerList), "possible words remaining.")
        elif (letterResult == "Yellow" or letterResult == "yellow"):
            print("Ok, letter", i, "was yellow.")
            #remove all words from the answer list that include that letter in this position
            for w in range(0, len(answerList)):
                check = 0
                if (w >= len(answerList)):
                    break
                while (check == 0):
                    if (w >= len(answerList)):
                        break
                    if (answerList[w][i-1] == bestWord[i-1]):
                        answerList = np.delete(answerList, w)
                    else:
                        check = 1
            #remove all words from the answer list that don't have that letter anywhere
            for w in range(0, len(answerList)):
                checkWhile = 0
                if (w >= len(answerList)):
                    break
                while (checkWhile == 0):
                    if (w >= len(answerList)):
                        break
                    checkLetter = 0   #variable to track if the searched-for letter is in the current word or not
                    for j in range(0,5):
                        if (answerList[w][j] == bestWord[i-1]):
                            checkLetter = 1   #the letter was found in this word
                    if (checkLetter == 0): #the letter was not found in this word
                        answerList = np.delete(answerList, w)
                    else:
                        checkWhile = 1
            print("Answer list updated. There are now", len(answerList), "possible words remaining.")        
        elif (letterResult == "Grey" or letterResult == "grey" or letterResult == "Gray" or letterResult == "gray"):
            print("Ok, letter", i, "was grey.")
        #remove all words from the answer list that include that letter anywhere
            for w in range(0, len(answerList)):
                check = 0
                if (w >= len(answerList)):
                    break
                while (check == 0):
                    if (w >= len(answerList)):
                        break
                    for j in range(0,5):
                        if (answerList[w][j] == bestWord[i-1]):
                            answerList = np.delete(answerList, w)        
                            break
                    check = 1
            print("Answer list updated. There are now", len(answerList), "possible words remaining.")
    return answerList

#results from first guess, calculation of second guess
for guess in range(1, 7):
    print("-------------------------------------------------------")
    print("Wordle Guess #", guess, ":", bestWord.upper())
    answerList = getResults(answerList, bestWord)
    letterCounts = countLetters(alphabet, answerList)
    wordScores = calculateScores(alphabet, answerList, letterCounts)
    maximumScoreLoc = np.argmax(wordScores)
    bestWord = answerList[maximumScoreLoc]
    print("The best next guess to maximize green letters is", bestWord.upper(), "with a score of", wordScores[maximumScoreLoc])    
    guess += 1



