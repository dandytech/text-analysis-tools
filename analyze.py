# from random_username.generate import generate_username
# import re, nltk, json
# from nltk.corpus import wordnet, stopwords
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from wordcloud import WordCloud
# nltk.download('wordnet')
# nltk.download('stopwords')
# from nltk.tokenize import word_tokenize, sent_tokenize
# nltk.download('averaged_perceptron_tagger')
# nltk.download('vader_lexicon')
# from nltk.stem import WordNetLemmatizer
# wordLemmatizer = WordNetLemmatizer()
# stopWords = set(stopwords.words('english'))
# sentimentAnalyzer = SentimentIntensityAnalyzer()


# def welcomeUser():
#     print("\nWelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

# def getUsername():
#     maxAttempts = 3
#     attempts = 0

#     while attempts < maxAttempts:
#         if attempts == 0:
#             inputPrompt = "\nTo begin, please enter your username:\n"
#         else:
#             inputPrompt = "\nPlease try again:\n"

#         usernameFromInput = input(inputPrompt)

#         # Validate username
#         if len(usernameFromInput) >= 5 and usernameFromInput.isidentifier():
#             return usernameFromInput
#         else:
#             print("Username must be at least 5 characters, alphanumeric/underscore only, no spaces, and cannot start with a number.")
#             attempts += 1

#     print(f"\nExhausted all {maxAttempts} attempts, assigning a username instead...")
#     return generate_username()[0]

# def greetUser(name):
#     print("Hello,", name)


# #Get Texts from file
# def getArticleText():
#    f=open("files/article.txt", "r")
#    rawText = f.read()
#    f.close()
#    return rawText.replace("\n", " ").replace("\r", "")

# #Extract Sentences from raw text body
# def tokenizeSentences(rawText):
#     return sent_tokenize(rawText)

# #Extract words from list of Sentences
# def tokenizeWords(sentences):
#     words =[]
#     for sentence in sentences:
#         word_tokenize(sentence)
#         words.extend(word_tokenize(sentence))
#     return words

# #Get the key sentences based on search partern of key words
# def extractKeySentences(sentences, stockPartern):
#     matchedSentences = []
#     for sentence in sentences:
#         #if sentence matched desired partern, add to matchedSentences
#         if re.search(stockPartern, sentence.lower()):
#             matchedSentences.append(sentence)
#     return matchedSentences

# # Get Average Word per Sentence, excluding punctuation
# def getWordsPerSentence(sentences):
#     totalWords =0
#     for sentence in sentences:
#         totalWords =+ len(sentence.split(" "))
#     return totalWords/len(sentences)



# # Convert part of speech from pos_tag function
# # into wordnet compactible pos tag
# posToWordnetTag = {
#     "J": wordnet.ADJ,
#     "V": wordnet.VERB,
#     "N": wordnet.NOUN,
#     "R": wordnet.ADV
# }
# def treebankPosToWordnetPos(partOfSpeech):
#     return posToWordnetTag.get(partOfSpeech[0], wordnet.NOUN)

# # Convert raw list of (word, POS) tuple to a list of strings
# # that only inlcude valid English word
# def cleansedWordList(posTaggedWordTuples):
#     cleansedWords = []
#     invalidWordPattern = r"[^a-zA-Z]"

#     for word, pos in posTaggedWordTuples:
#         cleansedWord = word.lower()

#         if (
#             len(cleansedWord) > 1
#             and cleansedWord.isalpha()
#             and cleansedWord not in stopWords
#             and not re.search(invalidWordPattern, cleansedWord)
#         ):
#             lemma = wordLemmatizer.lemmatize(
#                 cleansedWord,
#                 treebankPosToWordnetPos(pos)
#             )
#             cleansedWords.append(lemma)

#     return cleansedWords

# def analyzedText(textToAnalyze):
#     articleSentences = tokenizeSentences(textToAnalyze)
#     artticleWords = tokenizeWords(articleSentences)

#     # Get Sentence Analytics
#     stockSearchPartern = "[0-9]|[%$£€]|thousand|million|billion|trillion"
#     keySentences = extractKeySentences(articleSentences, stockSearchPartern)
#     wordsPerSentence = getWordsPerSentence(articleSentences)

#     # Get Word Analytics
#     wordsPosTagged = nltk.pos_tag(artticleWords)
#     articleWordCleansed = cleansedWordList(wordsPosTagged)


#     #Generate wordcloud
#     separator = " "
#     wordCloudFilePath = "result/wordcloud.png"
#     wordcloud =WordCloud(
#         width=1000,
#         height=700,
#         random_state=1,
#         background_color="salmon",
#         colormap="Pastel1",
#         collocations=False
#     ).generate(separator.join(articleWordCleansed))
#     wordcloud.to_file(wordCloudFilePath)
#     #Print for Testing
#     sentimentResult = sentimentAnalyzer.polarity_scores(textToAnalyze)


#     # Collate Analysis into one Dictionary
#     finalResult = {
#     "data": {
#     "keySentences" : keySentences,
#     "wordsPerSentence": round(wordsPerSentence, 1),
#     "sentiment":sentimentResult,
#     "wordCloudFilePath": wordCloudFilePath
#     },
#     "metadata": {
#         "sentencesAnalyzed": len(articleSentences),
#         "wordsAnalyzed": len(articleWordCleansed),
#     }

#     }
#     return finalResult

# def runAsFile():
#     #Get User Details
#     welcomeUser()
#     username = getUsername()
#     greetUser(username)

#     #Extract and tokenize Text
#     articleTextRaw = getArticleText()
#     analyzedText(articleTextRaw)

from random_username.generate import generate_username
import re
import json
import nltk
from nltk.corpus import wordnet, stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from wordcloud import WordCloud

# -------------------- NLTK SETUP --------------------
nltk.download("wordnet")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
nltk.download("vader_lexicon")
nltk.download("punkt")

wordLemmatizer = WordNetLemmatizer()
stopWords = set(stopwords.words("english"))
sentimentAnalyzer = SentimentIntensityAnalyzer()

# -------------------- USER FLOW --------------------
def welcomeUser():
    print("\nWelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

def getUsername():
    maxAttempts = 3
    attempts = 0

    while attempts < maxAttempts:
        prompt = "\nTo begin, please enter your username:\n" if attempts == 0 else "\nPlease try again:\n"
        usernameFromInput = input(prompt)

        if len(usernameFromInput) >= 5 and usernameFromInput.isidentifier():
            return usernameFromInput
        else:
            print("Username must be at least 5 characters, alphanumeric/underscore only, no spaces, and cannot start with a number.")
            attempts += 1

    print(f"\nExhausted all {maxAttempts} attempts, assigning a username instead...")
    return generate_username()[0]

def greetUser(name):
    print("Hello,", name)

# -------------------- FILE INPUT --------------------
def getArticleText():
    with open("files/article.txt", "r", encoding="utf-8") as f:
        rawText = f.read()
    return rawText.replace("\n", " ").replace("\r", "").strip()

# -------------------- TOKENIZATION --------------------
def tokenizeSentences(rawText):
    if not rawText:
        return []
    return sent_tokenize(rawText)

def tokenizeWords(sentences):
    words = []
    for sentence in sentences:
        words.extend(word_tokenize(sentence))
    return words

# -------------------- SENTENCE ANALYSIS --------------------
def extractKeySentences(sentences, stockPattern):
    matchedSentences = []
    for sentence in sentences:
        if re.search(stockPattern, sentence.lower()):
            matchedSentences.append(sentence)
    return matchedSentences

def getWordsPerSentence(sentences):
    if not sentences:
        return 0

    totalWords = 0
    for sentence in sentences:
        totalWords += len(sentence.split())

    return totalWords / len(sentences)

# -------------------- WORD CLEANING --------------------
posToWordnetTag = {
    "J": wordnet.ADJ,
    "V": wordnet.VERB,
    "N": wordnet.NOUN,
    "R": wordnet.ADV
}

def treebankPosToWordnetPos(partOfSpeech):
    return posToWordnetTag.get(partOfSpeech[0], wordnet.NOUN)

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

# -------------------- MAIN ANALYSIS --------------------
def analyzedText(textToAnalyze):
    if not textToAnalyze or not textToAnalyze.strip():
        return {
            "data": {},
            "metadata": {
                "error": "No analyzable text",
                "sentencesAnalyzed": 0,
                "wordsAnalyzed": 0
            }
        }

    articleSentences = tokenizeSentences(textToAnalyze)
    articleWords = tokenizeWords(articleSentences)

    stockSearchPattern = r"[0-9]|[%$£€]|thousand|million|billion|trillion"
    keySentences = extractKeySentences(articleSentences, stockSearchPattern)
    wordsPerSentence = getWordsPerSentence(articleSentences)

    wordsPosTagged = nltk.pos_tag(articleWords)
    articleWordCleansed = cleansedWordList(wordsPosTagged)

    # WordCloud (safe)
    wordCloudFilePath = None
    if articleWordCleansed:
        wordCloudFilePath = "result/wordcloud.png"
        wordcloud = WordCloud(
            width=1000,
            height=700,
            random_state=1,
            background_color="salmon",
            colormap="Pastel1",
            collocations=False
        ).generate(" ".join(articleWordCleansed))
        wordcloud.to_file(wordCloudFilePath)

    sentimentResult = sentimentAnalyzer.polarity_scores(textToAnalyze)

    return {
        "data": {
            "keySentences": keySentences,
            "wordsPerSentence": round(wordsPerSentence, 1),
            "sentiment": sentimentResult,
            "wordCloudFilePath": wordCloudFilePath
        },
        "metadata": {
            "sentencesAnalyzed": len(articleSentences),
            "wordsAnalyzed": len(articleWordCleansed)
        }
    }

# -------------------- RUN AS SCRIPT --------------------
def runAsFile():
    welcomeUser()
    username = getUsername()
    greetUser(username)

    #Extract and tokenize Text
    articleTextRaw = getArticleText()
    result = analyzedText(articleTextRaw)

    print(json.dumps(result, indent=2))