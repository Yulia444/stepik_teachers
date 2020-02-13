from flask import Flask, render_template, request, abort
from flask_wtf.csrf import CSRFProtect
import json
from flask_sqlalchemy import SQLAlchemy
from forms import Booking, Request
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


with open(r"static/data/days.json", 'r', encoding="utf-8") as json_file:
    json_days = json.load(json_file)

days = json_days["days"]

with open(r"static/data/goals.json", 'r', encoding="utf-8") as json_file:
    study_goals = json.load(json_file)





app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_string'
csrf = CSRFProtect(app)
csrf.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from models import db
db.init_app(app)
migrate = Migrate(app, db, compare_type=True)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
from models import Teachers, Bookings, Requests

@app.route('/')
def main():
    lang_teachers = list(teachers)
    sorted_by_rating = sorted(lang_teachers, key = lambda i: i['rating'], reverse=True)[:6]
    sorted_by_price = sorted(sorted_by_rating, key = lambda i: i['price'])
    return render_template("index.html", teachers = sorted_by_price)

@app.route('/all/')
def all():
    with app.app_context():
        db.create_all()
        teachers = db.session.query(Teachers).all()
    return render_template("all.html", teachers=teachers)

@app.context_processor
def schedule():
    def _schedule(hour, day):
        
        bool_hour = []
        for key in day.keys():
            bool_hour.append({key: day[key][hour]})
        return bool_hour
    return dict(schedule=_schedule)


@app.route('/goals/<goal>/')
def goals(goal):
    with app.app_context():
        db.create_all()
        teachers = db.session.query(Teachers).filter(Teachers.goals.like("%{}%".format(goal))
        ).order_by(Teachers.rating.desc()).all()
    return render_template("goal.html", teachers = teachers, goal = study_goals["goals"][goal])

@app.route('/profiles/<int:id>/')
def profiles(id):
    id_goals = []
    with app.app_context():
        db.create_all()
        teachers = db.session.query(Teachers).all()
    if id >= len(teachers):
        abort(404, description="Teacher is not found")
    else:
        for key, value in study_goals["goals"].items():
            for goal in teachers[id].goals.split(' '):
                if goal == key:
                    id_goals.append(value)
    teacher_schedule = json.loads(teachers[id].schedule)
    return render_template("profile.html", teacher = teachers[id], goal_values = id_goals,
     teacher_schedule = teacher_schedule['free'])

@app.route('/request/')
def do_request():
    form = Request()
    return render_template("request.html", form=form)

@app.route('/request_done/', methods=['GET','POST'])
def request_done():    
    goal = request.args.get('goal')
    time = request.args.get('time')
    clientName = request.args.get("clientName")
    clientPhone = request.args.get("clientPhone")

    with app.app_context():
        db.create_all()
        new_request = Requests(goal=goal, time=time, clientName=clientName, clientPhone=clientPhone)
        db.session.add(new_request)
        db.session.commit()

    return render_template("request_done.html", goal=study_goals['goals'][goal],
     time=time, clientName=clientName, clientPhone=clientPhone)

@app.route('/booking/<int:id>/<string:day>-<string:hour>')
def booking(id, day, hour):
    form = Booking()
    with app.app_context():
        db.create_all()
        teachers = db.session.query(Teachers).all()
    teacher = teachers[id]
    return render_template("booking.html", teacher=teacher, day=days[day], hour=hour, form=form)

@app.route('/booking_done/<int:teacher_id>-<string:day>-<string:hour>', methods=['GET', 'POST'])
def booking_done(teacher_id, day, hour):
    clientName = request.args.get("clientName")
    clientPhone = request.args.get("clientPhone")

    with app.app_context():
        db.create_all()
        new_booking = Bookings(clientName=clientName, clientPhone=clientPhone, dayOfWeek=day,
         hour=hour, teacher_id=teacher_id)
        db.session.add(new_booking)
        db.session.commit()
    
    return render_template("booking_done.html", day=day, hour=hour, clientName=clientName,
    clientPhone=clientPhone)

if __name__ == "__main__":
    manager.run()
