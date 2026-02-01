#Welcome User
def welcomeUser():
    print("\nWelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

#Get username
def getUsername():
    #Print a message, prompting user to input their username
    usernameFromInput = username=input("\nTo begin, please enter your username\n")
    return usernameFromInput;

#Great th User
def greatUser(name):
    print("Hello, " + name )

def runProgram(): #calling functions in a function
    welcomeUser();
    username = getUsername()
    greatUser(username)


runProgram();
