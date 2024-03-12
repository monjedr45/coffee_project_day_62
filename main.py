from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired(), URL()])
    open_time = StringField('open time', validators=[DataRequired()])
    close_time = StringField('close time', validators=[DataRequired()])
    rating = SelectField('Coffee', choices=[('1', '☕'), ('2', '☕ ☕ '),('3', '☕☕☕ '), ('4', '☕☕☕☕ ')] ,validators=[DataRequired()])
    wifi = SelectField('wifi', choices=[('1', '💪'), ('2', '💪💪'),('3', '💪💪💪')] ,validators=[DataRequired()])
    power = SelectField('Power', choices=[('1', '🔌'), ('2', '🔌🔌'),('3', '🔌🔌🔌')] ,validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe_name = form.cafe.data
        location = form.location.data
        open_time = form.open_time.data
        close_time = form.close_time.data
        rating = form.rating.data
        wifi = form.wifi.data
        power = form.power.data
        list_ = [cafe_name, location, open_time, close_time, rating, wifi, power]
        with open('cafe-data.csv', 'a') as fd:
            line = ','.join(map(str, list_))
            fd.write('\n' + line)
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
