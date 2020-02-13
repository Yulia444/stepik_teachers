from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Teachers(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    about = db.Column(db.Text, nullable=False)
    goals = db.Column(db.String(64), nullable=False)
    picture = db.Column(db.String(64), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    schedule = db.Column(db.Text, nullable=False)
    students = db.relationship('Bookings', backref='teacher', lazy='dynamic')
    def __repr__(self):
        return '<Teacher {}>'.format(self.name)

class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    clientName = db.Column(db.String(32), nullable=False)
    clientPhone = db.Column(db.String(13), nullable=False)
    dayOfWeek = db.Column(db.String(16), nullable=False)
    hour = db.Column(db.String(4), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))

class Requests(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(16), nullable=False)
    time = db.Column(db.String(8), nullable=False)
    clientName = db.Column(db.String(32), nullable=False)
    clientPhone = db.Column(db.String(13), nullable=False)


