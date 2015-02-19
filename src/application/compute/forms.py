import flask_wtf
import wtforms


class ComputeForm(flask_wtf.Form):
    a = wtforms.IntegerField(label='a', validators=[wtforms.validators.DataRequired()])
    b = wtforms.IntegerField(label='b', validators=[wtforms.validators.DataRequired()])
