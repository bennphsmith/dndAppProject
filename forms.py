'''#####################
Forms classes for registering new users and logging current users
Including methods for authenticating email
Author: Benjamin Smith
Last Edit: 09/04/2020
#####################'''

# Create Registration From for user
# Username takes the for of an email with is inherently unique (primary key)
# Password must be between 2 & 20 characters
# Confirm password checks that user entered the intended password
class RegistrationForm(FlaskForm):
    email = emailCheck('Username')
    password = passCheck('Password')
    confirm_password = passConfirm('Password')

# Create Login Form for user
class LoginForm(FlaskForm):
    email = emailCheck('Username')
    password = passCheck('Password')

# Design methods for checking user inputs
# Check for '@' and '.' to verify email authenticity 
def emailCheck(email):
    if '@' not in email or '.' not in email:
        return 'error'
    else:
        return email

# Check password length is longer that 2 and shorter than 20
def passCheck(password):
    if len(password) < 2 or len(password) > 20:
        return 'error'
    else:
        return password
'''
# Check the password that they entered is correct
def passConfirm(password):
    '''