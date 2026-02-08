from random_username.generate import generate_username
from nltk.tokenize import word_tokenize, sent_tokenize
import re

def welcomeUser():
    print("\nWelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

def getUsername():
    maxAttempts = 3
    attempts = 0

    while attempts < maxAttempts:
        if attempts == 0:
            inputPrompt = "\nTo begin, please enter your username:\n"
        else:
            inputPrompt = "\nPlease try again:\n"

        usernameFromInput = input(inputPrompt)

        # Validate username
        if len(usernameFromInput) >= 5 and usernameFromInput.isidentifier():
            return usernameFromInput
        else:
            print("Username must be at least 5 characters, alphanumeric/underscore only, no spaces, and cannot start with a number.")
            attempts += 1

    print(f"\nExhausted all {maxAttempts} attempts, assigning a username instead...")
    return generate_username()[0]

def greetUser(name):
    print("Hello,", name)



   


#Get Texts from file
def getArticleText():
   f=open("files/article.txt", "r")
   rawText = f.read()
   f.close()
   return rawText.replace("\n", " ").replace("\r", "")

#Extract Sentences from raw text body
def tokenizeSentences(rawText):
    return sent_tokenize(rawText)

#Extract words from list of Sentences
def tokenizeWords(sentences):
    words =[]
    for sentence in sentences:
        word_tokenize(sentence)
        words.extend(word_tokenize(sentence))
    return words

#Get the key sentences based on search partern of key words
def extractKeySentences(sentences, stockPartern):
    matchedSentences = []
    for sentence in sentences:
        #if sentence matched desired partern, add to matchedSentences
        if re.search(stockPartern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences

#Get User Details
# welcomeUser()
# username = getUsername()
# greetUser(username)


articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
artticleWords = tokenizeWords(articleSentences)

# Get Analytics
stockSearchPartern = "[0-9]| [%$£€] | thousand | million | billion | trillion"
keySentences = extractKeySentences(articleSentences, stockSearchPartern)
wordsPerSentence = len(artticleWords)/len(articleSentences)
#Print for Testing
print("GOT:")
print(wordsPerSentence)
print(artticleWords)
