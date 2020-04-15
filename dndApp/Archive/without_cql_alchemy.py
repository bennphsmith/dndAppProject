'''
#############
Archive of first attempt to create User and Login credentials
Quereies all fucntioning by it's difficult to incorporate the User profiles
Therefore changing to try and use OO CQL Alchemy approach
Author: Ben Smith
Last Edited: 13.04.20
#############
'''

#############Routes###############
#Route to app main/registration page
@app.route('/', methods=['GET', 'POST'])
@app.route('/register/', methods=['GET', 'POST'])
def Register():
    regForm = RegistrationForm()
    if (regForm.validate_on_submit() == True):
        hpass = bcrypt.generate_password_hash(regForm.password.data).decode('utf-8') #hash password and make into string
        session.execute(
            "INSERT INTO user(email, first_name, last_name, password) VALUES(%s, %s, %s, %s)", 
            (regForm.email.data, regForm.first_name.data, regForm.last_name.data, hpass)) #Pass data to Cass Database
        flash('Success', 'success') #Display flash success message
        return redirect(url_for('Login'))
    return render_template('register_form.html', form=regForm)

#Route to login page
@app.route('/login/', methods=['GET', 'POST'])
def Login():
    logForm = LoginForm()
    if (logForm.validate_on_submit() == True):
        return redirect(url_for('Home'))
    return render_template('login_form.html', form=logForm)



###################Forms##################

#RegistrationFrom
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        cluster = Cluster(['127.0.0.1']) #Initialise Cluster
        session = cluster.connect('main') #Connect to keyspace
        users_list = session.execute(
            "SELECT * FROM user WHERE email = %s", [email.data]) #Return tuples where email address is same as one entered
        try:
            user = users_list[0] #Get single tuple
        except IndexError:
            return
        else:
            raise ValidationError('Email address already registered!')

#LoginForm
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Login')

    def validate_email(self, email):
        cluster = Cluster(['127.0.0.1']) #Initialise Cluster
        session = cluster.connect('main') #Connect to keyspace
        users_list = session.execute(
            "SELECT * FROM user WHERE email = %s", [email.data]) #Return tuples where email address is same as one entered
        try:
            user = users_list[0] #Get single tuple
        except IndexError:
            raise ValidationError('Email address not registered!')
        else:
            return