
from flask_wtf import FlaskForm
from wtforms import PasswordField, TextAreaField
from wtforms.validators import DataRequired


class ChangePassForm(FlaskForm):
    old_pass = PasswordField('Old Password',
                             id='old_pass',
                             validators=[DataRequired()])
    new_pass = PasswordField('New Password',
                             id='new_pass',
                             validators=[DataRequired()])

class TextInputForm(FlaskForm):
    text_input = TextAreaField('Text For spaCy',
                               id='text_input',
                               validators=[DataRequired()],
                               render_kw={"rows": 15, "cols": 11})
