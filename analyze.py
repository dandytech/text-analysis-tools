#Welcome User
from random_username.generate import generate_username

#Welcome User
def welcomeUser():
    print("\nWelcome to the text analysis tool, I will mine and analyze a body of text from a file you give me!")

#Get username
def getUsername():
    #Print a message, prompting user to input their username
    usernameFromInput = input("\nTo begin, please enter your username\n")
    
    if len(usernameFromInput) < 5 or not usernameFromInput.isidentifier():
        return usernameFromInput;
    else:
        print("Your username must be atleast 5 characters long, alphanumerics only (a-z/A-Z/0-9), have no spaces, and cannot start with numbers! ")
        print("Assigning new username: ")
        return usernameFromInput;

#Great th User
def greatUser(name):
    print("Hello, " + name )

def runProgram(): #calling functions in a function
    welcomeUser();
    username = getUsername()
    greatUser(username)


runProgram();
