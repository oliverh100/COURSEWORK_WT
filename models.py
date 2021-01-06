from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String(64))
    s_name = db.Column(db.String(64))
    initials = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    title = db.Column(db.String(64))

    activities = db.relationship('Activity', secondary='teacher_activity_link')

    def iterable(self):
        return [self.f_name, self.s_name, self.initials, self.email, self.title]

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, edit_form):
        categories = ['f_name', 's_name', 'initials', 'email', 'title']
        for category in categories:
            setattr(self, category, getattr(edit_form, category).data)
        db.session.commit()


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String(64))
    building = db.Column(db.String(64))

    activities = db.relationship('Activity', backref='room')

    def iterable(self):
        return [self.r_name, self.building]

    def add(self):
        db.session.add(self)
        db.session.commit()

    def edit(self, edit_form):
        categories = ['r_name', 'building']
        for category in categories:
            setattr(self, category, getattr(edit_form, category).data)
        db.session.commit()


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a_name = db.Column(db.String(64))
    r_id = db.Column(db.Integer(), db.ForeignKey('room.id'))
    week = db.Column(db.String(64))
    day = db.Column(db.String(64))
    time = db.Column(db.String(64))
    max_attendees = db.Column(db.String(64))
    food_supplied = db.Column(db.String(64))

    teachers = db.relationship('Teacher', secondary='teacher_activity_link')

    def iterable(self):
        teacher_list = [f'{t.f_name} {t.s_name}, ' for t in self.teachers]
        teacher_list_str = ''
        for teacher in teacher_list:
            teacher_list_str += teacher
        teacher_list_str = teacher_list_str[:-2]
        return [self.a_name, self.room.r_name, self.week, self.day, self.time, self.max_attendees, self.food_supplied, teacher_list_str]

    def iterable_datetime(self):
        arr = self.iterable()
        datetime = f'Week {self.week} {self.day}, {self.time}'
        arr.pop(2)
        arr.pop(2)
        arr.pop(2)
        arr.insert(2, datetime)
        return arr

    def add(self):
        db.session.add(self)
        db.session.commit()


class TeacherActivityLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    a_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    t_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

    def add(self):
        db.session.add(self)
        db.session.commit()


