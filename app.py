from flask import Flask, render_template, request
import json
with open(r"static/data/days.json", 'r', encoding="utf-8") as json_file:
    json_days = json.load(json_file)

with open(r"static/data/teachers.json", 'r', encoding="utf-8") as json_file:
    json_data = json.load(json_file)

with open(r"static/data/goals.json", 'r', encoding="utf-8") as json_file:
    study_goals = json.load(json_file)

teachers = json_data["teachers"]
days = json_days["days"]

app = Flask(__name__)

@app.route('/')
def main():
    lang_teachers = list(teachers)
    sorted_by_rating = sorted(lang_teachers, key = lambda i: i['rating'], reverse=True)[:6]
    sorted_by_price = sorted(sorted_by_rating, key = lambda i: i['price'])
    return render_template("index.html", teachers = sorted_by_price)

@app.route('/all/')
def all():
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
    lang_teachers = list(teachers)
    filter_by_goal = [teacher for teacher in lang_teachers if goal in teacher["goals"]]
    sorted_by_rating = sorted(filter_by_goal, key = lambda i: i['rating'], reverse=True)
    return render_template("goal.html", teachers = sorted_by_rating, goal = study_goals["goals"][goal])

@app.route('/profiles/<int:id>/')
def profiles(id):
    id_goals = []
    for key, value in study_goals["goals"].items():
        for goal in teachers[id]["goals"]:
            if goal == key:
                id_goals.append(value)
    teacher_schedule = teachers[id]["free"]
    return render_template("profile.html", teacher = teachers[id], goal_values = id_goals,
     teacher_schedule = teacher_schedule)

@app.route('/request/')
def do_request():
    return render_template("request.html")

@app.route('/request_done/', methods=['GET','POST'])
def request_done():    
    goal = request.args.get('goal')
    time = request.args.get('time')
    clientName = request.args.get("clientName")
    clientPhone = request.args.get("clientPhone")
    data = {
        "goal" : goal,
        "time": time,
        "clientName" : clientName,
        "clientPhone" : clientPhone
    }
    with open(r"static/data/request.json", "r", encoding="utf-8") as f:
        request_data = json.load(f)

    request_data["clients"].append(data)

    with open(r"static/data/request.json", 'w') as f:
        json.dump(request_data, f)

    return render_template("request_done.html", goal=study_goals['goals'][goal],
     time=time, clientName=clientName, clientPhone=clientPhone)

@app.route('/booking/<int:id>/<string:day>-<string:hour>')
def booking(id, day, hour):
    teacher = teachers[id]
    return render_template("booking.html", teacher=teacher, day=days[day], hour=hour)

@app.route('/booking_done/<int:teacher_id>-<string:day>-<string:hour>', methods=['GET', 'POST'])
def booking_done(teacher_id, day, hour):
    clientName = request.args.get("clientName")
    clientPhone = request.args.get("clientPhone")
    data = {
        "teacher_id" : teacher_id,
        "day" : day,
        "hour" : hour,
        "clientName" : clientName,
        "clientPhone" : clientPhone
    }
    
    with open(r"static/data/booking.json", 'r', encoding="utf-8") as f:
        booking_data = json.load(f)
    
    booking_data["booking"].append(data)

    with open(r"static/data/booking.json", 'w', encoding="utf-8") as f:
        json.dump(booking_data, f)

    return render_template("booking_done.html", day=day, hour=hour, clientName=clientName,
    clientPhone=clientPhone)

if __name__ == "__main__":
    app.run()
