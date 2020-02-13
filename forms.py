from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired

class Booking(FlaskForm):
    clientName = StringField('Вас зовут', validators=[DataRequired()])
    clientPhone = TelField('Ваш телефон', validators=[DataRequired()])
    submit = SubmitField('Записаться на пробный урок')

class Request(FlaskForm):
    goal = RadioField(choices=[('travel','Для путешествий'), ('study', 'Для школы'),
    ('work', 'Для работы'), ('relocate', 'Для переезда')])
    time = RadioField(choices=[('1-2', '1-2 часа в&nbsp;неделю'), ('3-5', '3-5 часа в&nbsp;неделю'),
    ('5-7', '5-7 часа в&nbsp;неделю'), ('7-10', '7-10 часа в&nbsp;неделю')])
    clientName = StringField('Вас зовут', validators=[DataRequired()])
    clientPhone = TelField('Ваш телефон', validators=[DataRequired()])
    submit=SubmitField('Найдите мне преподавателя', validators=[DataRequired()])

