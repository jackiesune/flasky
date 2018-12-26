from flask_wtf import FlaskForm as Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required


class NameForm(Form):
    name=StringField('What is your name?',validators=[Required()])
    submit=SubmitField('submit')

