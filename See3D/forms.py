from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length

class SubmitForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            InputRequired(message="A title is required."),
            Length(max=31, message="The title must be less than 32 characters.")
        ]
    )

    description = TextAreaField(
        'Description',
        validators=[
            InputRequired(message="A description is required."),
            Length(max=1023, message="The description must be less than 1024 characters.")
        ]
    )
