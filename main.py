import re, json, io, os
from datetime import date, datetime

# Regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regexMobile = '^0\d(?:\s\d{2})*$'
file_Name = "data.json"


# Define a function for
# for validating an Email
def checkEmail(email):

  # pass the regular expression
  # and the string into the fullmatch() method
  if (re.fullmatch(regex, email)):
    return True
  else:
    return False


# Define a funtion for
# for phone number validation
def checkUserPhone(params):
  # pass the regular expression
  # and the string into the fullmatch() method
  r = params.startswith("0")
  if r == True:
    if params.isdigit() and (len(params) == 9 or len(params) == 10):
      return True
    else:
      print("Please enter valid phone number starts with 0 (eg: 0470294174)")
    return False
  else:
    print("Please enter valid phone number starts with 0 (eg: 0470294174)")
    return False


# Define function to check and validate date of birth
def checkUserDob(dateOfBirth):
  try:
    datetime.strptime(dateOfBirth, "%d/%m/%Y")
    return True
  except:
    return False


def checkYears(dateOfBirth):
  todayDate = date.today()
  # convert string to date object
  d1 = datetime.strptime(todayDate, "%Y/%m/%d")
  d2 = datetime.strptime(dateOfBirth, "%Y/%m/%d")
  # difference between dates in timedelta
  diff = d1 - d2
  if (diff >= 21):
    return True
  else:
    print("You must be 21 years old to access this application!")
    return False


# Function to validate the password
def password_check(passwd):
  SpecialSym = ['$', '@', '#', '%']
  val = True

  if len(passwd) < 6:
    print('length should be at least 6')
    val = False

  if len(passwd) > 20:
    print('length should be not be greater than 8')
    val = False

  if not any(char.isdigit() for char in passwd):
    print('Password should have at least one numeral')
    val = False

  if not any(char.isupper() for char in passwd):
    print('Password should have at least one uppercase letter')
    val = False

  if not any(char.islower() for char in passwd):
    print('Password should have at least one lowercase letter')
    val = False

  if not any(char in SpecialSym for char in passwd):
    print('Password should have at least one of the symbols $@#')
    val = False
  if val:
    return val


# common function to print messages
def throw_error_message(params):
  print(params)
  return False


# define a function to find user for login
def findUserAndLogIn(userName, userPassword, attemptCounter):
  data = load_json()
  counter = 0
  for i in range(len(data['emp_details'])):
    if ((userName == data['emp_details'][i]['userName']
         or userName == data['emp_details'][i]['userPhone'])):
      counter = 1
      if (userPassword == data['emp_details'][i]['userPassword']):
        attemptCounter = 0
        print("Welcome " + data['emp_details'][i]['userName'])
        afterLoginSteps(i, data['emp_details'][i])
      else:
        attemptCounter = attemptCounter + 1
        print("You have entered the wrong password")
        print(attemptCounter)
        print("Please try again!")
        if (attemptCounter >= 3):
          showDoBForLogin()
        else:
          userName = input("Please enter your Username (Mobile Number): ")
          if (userName):
            userPassword = input("Please enter your password ")
            if (password_check(userPassword)):
              findUserAndLogIn(userName, userPassword, attemptCounter)
            else:
              print("Password is not valid, please try again")
              userMenu()
          else:
            print("Email is not valid, please try again!")
            userMenu()

  if (counter == 0):
    print(
      "You have not signedup with this Contact Number, Please Signup First")
    userMenu()


def showDoBForLogin():
  print("You have used the maximum attempts to login: ")
  print("Please reset the password by entering the following details: ")
  username = input("Please enter your Username (Mobile Number) to confirm: ")
  dateOfBirth = input(
    "Please enter your Date of Birth in DD/MM/YYYY format, to confirm : ")
  newPassword = input("Please enter you new password: ")
  confirmNewPassword = input("Please re-enter you new password: ")
  processForgotPassword(username, dateOfBirth, newPassword, confirmNewPassword)


def processForgotPassword(username, dateOfBirth, newPassword,
                          confirmNewPassword):
  if (checkUserDob(dateOfBirth)):
    if (newPassword == confirmNewPassword):
      data = load_json()
      for i in range(len(data['emp_details'])):
        if (username == data['emp_details'][i]['userName']
            or username == data['emp_details'][i]['userPhone']):
          updatePasswordInJsonFile(i, newPassword)
          print("Your password has been reset succesfully!")
          userMenu()
    else:
      throw_error_message("Password and confirm password doesn't matched!")
      print("Please start again!")
      showDoBForLogin()
  else:
    throw_error_message(
      "You have entered the Date of Birth in invalid format!")
    print("Please start again!")
    showDoBForLogin()


def afterLoginSteps(index, loggedInUserDetail):
  print("Please enter 1 for resetting the password: ")
  print("Please enter 2 for signout: ")
  selectedVal = input()
  if (selectedVal == '1'):
    username = input("Please enter Username(Mobile no): ")
    if (username == loggedInUserDetail['userPhone']
        or username == loggedInUserDetail['userName']):
      currentPassword = input("Please enter your old password: ")
      if (currentPassword == loggedInUserDetail['userPassword']):
        newPassword = input("Please enter your new password: ")
        updatedData = updatePasswordInJsonFile(index, newPassword)
        if (updatedData):
          print("Your password has been reset successfully!")
          afterLoginSteps(index, updatedData)

        else:
          print("Something went wrong!")
          print("Please try again!")
          afterLoginSteps(index, loggedInUserDetail)

      else:
        print("You have entered the wrong password")
        afterLoginSteps(index, loggedInUserDetail)

    else:
      print(
        "You have not signedup with this Contact Number, Please Sign up First")
      userMenu()

  else:
    print("Thank you for using the system")


# Helper login user function
def loginUser():
  userName = input("Please enter your Username (Mobile Number): ")
  if (userName):
    userPassword = input("Please enter your password ")
    if (password_check(userPassword)):
      findUserAndLogIn(userName, userPassword, 0)
    else:
      print("Password is not valid, please try again")
      userMenu()
  else:
    print("Email is not valid, please try again!")
    userMenu()


# define a function for register a user
def registerUser():
  userEmail = ''
  userName = ''
  userPhone = ''
  userPassword = ''
  userConfirmPassword = ''
  myDict = {}

  userName = input("Please Enter Your Name ")
  if (userName == '' or len(userName) < 3):
    throw_error_message(
      'Please enter a valid Username and it should not be empty and greater than 3 character'
    )
  else:
    myDict["userName"] = userName
    userEmail = input("Please Enter Your Email ")
    if (checkEmail(userEmail)):
      myDict["userEmail"] = userEmail
      userPhone = input("Please Enter Your Phone Number ")
      if (checkUserPhone(userPhone)):
        myDict["userPhone"] = userPhone
        userPassword = input("Please Enter Your Password ")
        if (password_check(userPassword)):
          userConfirmPassword = input("Please Confirm Your Password ")
          if (userConfirmPassword == userPassword):
            myDict["userPassword"] = userPassword
            userDob = input(
              "Please Enter Your Date of Birth # DD/MM/YYYY (No Space): ")
            if (checkUserDob(userDob)):
              myDict["userDob"] = userDob
            else:
              myDict = []
              throw_error_message(
                "You have entered the Date of Birth in invalid format!")
          else:
            throw_error_message(
              "Password and confirm password doesn't matched")
        else:
          myDict = []
      else:
        myDict = []
    else:
      myDict = []
      throw_error_message("Please enter a valid email")

  return myDict


# Show menu category
def userMenu():
  print("Please Enter 1 for Sign up ")
  print("Please Enter 2 for Login ")
  print("Please Enter 3 Quit ")
  userInput = input()
  selectCategory(userInput)
  return userInput


# define function to select category
def selectCategory(userInput):
  if (userInput == '1'):
    userDetails = registerUser()
    startupCheck()
    write_json(userDetails)
    if (userDetails):
      print("You have successfully Signed up!")
      userMenu()
    else:
      print("Please start again!")
      userMenu()
  elif (userInput == '2'):
    userlogin = loginUser()
    if (userlogin):
      print("You have successfully Signed in!")
    else:
      userMenu()
  else:
    print("Thank you for using the Aplication")


# checks if file exists
def startupCheck():
  ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

  if os.path.isfile(ROOT_DIR + '/' + file_Name) and os.access(
      ROOT_DIR + '/' + file_Name, os.R_OK):
    #File exists and is readable
    print('.')
  else:
    #Either file is missing or is not readable, creating file...
    with io.open(os.path.join(ROOT_DIR, file_Name), 'w') as db_file:
      db_file.write(json.dumps({"emp_details": []}))


# function to add to JSON
def write_json(new_data, filename=file_Name):
  with open(filename, 'r+') as file:
    # First we load existing data into a dict.
    file_data = json.load(file)
    # Join new_data with file_data inside emp_details
    file_data["emp_details"].append(new_data)
    # Sets file's current position at offset.
    file.seek(0)
    # convert back to json.
    json.dump(file_data, file, indent=4)


# load json from file
def load_json(filename=file_Name):
  with open(filename, 'r+') as file:
    # First we load existing data into a dict.
    file_data = json.load(file)
    return file_data


def updatePasswordInJsonFile(index, updatedValue):

  with open(file_Name, 'r+') as file:
    # First we load existing data into a dict.
    file_data = json.load(file)
    # Join new_data with file_data inside emp_details
    file_data["emp_details"][index]["userPassword"] = updatedValue
    file.seek(0)
    file.truncate()
    json.dump(file_data, file, indent=4)
    return file_data["emp_details"][index]


# Main method
def main():
  global userDetails
  userMenu()


# Driver Code
if __name__ == '__main__':
  main()
