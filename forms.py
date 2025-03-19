from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField,DateTimeField,TimeField,TextAreaField, FileField,IntegerField, DateField
from wtforms import HiddenField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo,Optional,NumberRange
from models import Category, ProfessionalProfile, Booking
from datetime import datetime


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=60)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('client', 'Client'), ('professional', 'Professional')], validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    client_id = StringField('Client ID', validators=[DataRequired()])
    professional_id = StringField('Professional', validators=[DataRequired()])
    category_id =  StringField('Category', validators=[DataRequired()])
    scheduled_time = DateField('Scheduled Time', format='%Y-%m-%d', validators=[DataRequired()])
    message = TextAreaField('Message (Optional)', default="No message provided")

class ClientProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=15)])
    address = TextAreaField('Address', validators=[Optional(), Length(max=200)])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[Optional()])
    profile_picture = FileField('Profile Picture', validators=[Optional()])
    submit = SubmitField('Save Changes')

class ProfessionalProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[Optional()])
    profile_picture = FileField('Profile Picture', validators=[Optional()])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=15)])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    address = TextAreaField('Address', validators=[Optional(), Length(max=200)])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    experience = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0)])
    availability_status = SelectField(
        'Availability Status',
        choices=[('available', 'Available'), ('unavailable', 'Unavailable')],
        validators=[Optional()]
    )
    submit = SubmitField('Save Changes')

class UpdateBookingForm(FlaskForm):
    booking_id = IntegerField('Booking ID', validators=[DataRequired()])
    status = SelectField("Status", choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")])
    submit = SubmitField("Update")

class AdminEditUserForm(FlaskForm):
    username = StringField('Username',validators=[ DataRequired(), Length(min=3, max=50, message="Username must be between 3 and 50 characters.")])
    email = StringField('Email',validators=[DataRequired(),Email(message="Invalid email address.")])
    user_type = SelectField('User Type',choices=[('client', 'Client'), ('professional', 'Professional'),('admin', 'admin')],validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete User')

class CreateCategoryForm(FlaskForm):
    name = StringField("Category Name", validators=[DataRequired(), Length(max=100)])
    description = TextAreaField("Description", validators=[Length(max=500)])
    image = FileField("Category Image (optional)")
    submit = SubmitField("Create Category")