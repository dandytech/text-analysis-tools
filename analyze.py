from random_username.generate import generate_username
import re
import nltk
from nltk.corpus import wordnet, stopwords
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('averaged_perceptron_tagger_eng')
from nltk.stem import WordNetLemmatizer
wordLemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words('english'))



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

# Get Average Word per Sentence, excluding punctuation
def getWordsPerSentence(sentences):
    totalWords =0
    for sentence in sentences:
        totalWords =+ len(sentence.split(" "))
    return totalWords/len(sentences)



# Convert part of speech from pos_tag function
# into wordnet compactible pos tag
posToWordnetTag = {
    "J": wordnet.ADJ,
    "V": wordnet.VERB,
    "N": wordnet.NOUN,
    "R": wordnet.ADV
}
def treebankPosToWordnetPos(partOfSpeech):
    return posToWordnetTag.get(partOfSpeech[0], wordnet.NOUN)

# Convert raw list of (word, POS) tuple to a list of strings
# that only inlcude valid English word
def cleansedWordList(posTaggedWordTuples):
    cleansedWords = []
    invalidWordPattern = r"[^a-zA-Z]"

    for word, pos in posTaggedWordTuples:
        cleansedWord = word.lower()

        if (
            len(cleansedWord) > 1
            and cleansedWord.isalpha()
            and cleansedWord not in stopWords
            and not re.search(invalidWordPattern, cleansedWord)
        ):
            lemma = wordLemmatizer.lemmatize(
                cleansedWord,
                treebankPosToWordnetPos(pos)
            )
            cleansedWords.append(lemma)

    return cleansedWords


#Get User Details
# welcomeUser()
# username = getUsername()
# greetUser(username)


articleTextRaw = getArticleText()
articleSentences = tokenizeSentences(articleTextRaw)
artticleWords = tokenizeWords(articleSentences)

# Get Sentence Analytics
stockSearchPartern = "[0-9]|[%$£€]|thousand|million|billion|trillion"
keySentences = extractKeySentences(articleSentences, stockSearchPartern)
wordsPerSentence = getWordsPerSentence(articleSentences)

# Get Word Analytics
wordsPosTagged = nltk.pos_tag(artticleWords)
articleWordCleansed = cleansedWordList(wordsPosTagged)
#Print for Testing
print("GOT:")
print("Normalized words:")
print(articleWordCleansed)
