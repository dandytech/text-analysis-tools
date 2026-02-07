from random_username.generate import generate_username

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

def runProgram():
    welcomeUser()
    username = getUsername()
    greetUser(username)

runProgram()