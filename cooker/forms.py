from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from cooker.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class DeckForm(FlaskForm):
    name = StringField('Deck Name', validators=[DataRequired()])
    description = TextAreaField('Describe the deck!')
    deck_type = RadioField('Deck Type',
                           choices=[('Commander', 'Commander'),
                                    ('Vintage', 'Vintage'),
                                    ('Legacy', 'Legacy'),
                                    ('Modern', 'Modern')],
                           validators=[DataRequired()])
    submit = SubmitField('Add Deck')
