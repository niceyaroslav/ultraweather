from flask import Flask, request, render_template, redirect, flash
import sys
from WeatherService import WeatherService
from config import Config, BASE_DIR
from flask_sqlalchemy import SQLAlchemy
import os


# Declaration of main class instances


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"City({self.id}, {self.name})"


service = WeatherService()


@app.route('/', methods=['GET', 'POST'])
def index():
    if os.path.isfile(f'{BASE_DIR}/weather.db'):
        data = []
        for i in City.query.all():
            try:
                data.append(service.get_gata_dict(i.name))
            except TypeError:
                pass
        for j in data:
            if j:
                j['id'] = City.query.filter_by(name=j['city']).first().id
        return render_template('dynamic.html', data=data)
    else:
        return render_template('index.html')


@app.route("/add", methods=['POST'])
def add():
    city = request.values.get('city_name')
    if os.path.isfile(f'{BASE_DIR}/weather.db'):
        pass
    else:
        db.create_all()
    if city == '':
        return redirect('/')
    if city in [i.name for i in City.query.all()]:
        flash('The city has already been added to the list!')
    elif city not in [i.name for i in City.query.all()]:
        if service.get_gata_dict(city) == 'Wrong city name!':
            flash("The city doesn't exist!")
        else:
            city_instance = City(name=city)
            db.session.add(city_instance)
            db.session.commit()
    return redirect('/')


@app.route('/delete/<value>', methods=['GET', 'POST'])
def delete(value):
    city = City.query.filter_by(id=value).first()
    print(city.name)
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run(debug=True)