from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length

class SubmitForm(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            InputRequired(message="A title is required."),
            Length(max=32, message="The title must be 16 characters or less.")
        ]
    )

    description = TextAreaField(
        'Description',
        validators=[
            InputRequired(message="A description is required."),
            Length(max=512, message="The description must be 64 characters or less.")
        ]
    )

