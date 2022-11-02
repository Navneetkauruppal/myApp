import re
# Password validation in Python
# using naive method

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


# Define a function for
# for validating an Email
def checkEmail(email):

  # pass the regular expression
  # and the string into the fullmatch() method
  if (re.fullmatch(regex, email)):
    return True
  else:
    return False


def checkUserPhone(params):
  if (params):
    return True
  else:
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


def throw_error_message(params):
  print(params)


def registerUser():
  userEmail = ''
  userName = ''
  userPhone = ''
  userPassword = ''
  userConfirmPassword = ''
  userName = input("Please Enter Your Name")
  if (userName == '' or len(userName) < 3):
    throw_error_message(
      'Please enter a valid Username and it should not be empty and greater than 3 character'
    )
  else:
    userEmail = input("Please Enter Your Email")
    if (checkEmail(userEmail)):
      userPhone = input("Please Enter Your Phone Number")
      if (checkUserPhone(userPhone)):
        userPassword = input("Please Enter Your Password")
        if (password_check(userPassword)):
          userConfirmPassword = input("Please Confirm Your Password")
          if (userConfirmPassword == userPassword):
            print("thanks")
          else:
            throw_error_message(
              "Password and confirm password doesn't matched")
        else:
          throw_error_message(
            "Please Enter a valid password with alpha numeric values and symbols"
          )
      else:
        throw_error_message("Please Enter a valid phone number eg: 0111222333")
    else:
      throw_error_message("Please Enter a email address eg: abc@yopmail.com")


# Main method
def main():
  print("Please Enter 1 for Sign up")
  print("Please Enter 2 for Login")
  print("Please Enter 3 Quit")
  userInput = input()
  print(userInput)
  if (userInput == '1'):
    print("you enterd 1")
    registerUser()


passwd = 'Geek12@'

if (password_check(passwd)):
  print("Password is valid")
else:
  print("Invalid Password !!")

# Driver Code
if __name__ == '__main__':
  main()
