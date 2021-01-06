from flask import Flask, render_template, request, redirect, flash, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from fuzzywuzzy import fuzz
from werkzeug.urls import url_parse

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
config = {
    "CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)
login = LoginManager(app)
login.login_view = 'login'

from models import Teacher, Activity, Room, TeacherActivityLink
from forms import *


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = MenuSelectionForm()
    if form.validate_on_submit():
        return redirect(f'/{form.option.data}')
    return render_template('index.html', form=form)


@app.route('/teachers', methods=['GET', 'POST'])
@login_required
def teachers():
    teacher_table = [teacher.iterable() for teacher in Teacher.query.all()]

    find_edit_id_form = FindEditIdFormTeacher()
    edit_teacher_form = EditTeacherForm()
    add_teacher_form = AddTeacherForm()
    delete_teacher_form = DeleteTeacherForm()
    teacher_form = TeacherForm()
    fields = ['f_name', 's_name', 'initials', 'email', 'title']
    show_options = {
        'edit_id': False,
        'edit': False,
        'add': False,
        'delete': False
    }

    data = request.form

    if 'add' in data:
        show_options['add'] = True
        redirect('teachers')

    if 'edit' in data:
        show_options['edit_id'] = True
        redirect('teachers')

    if 'delete' in data:
        show_options['delete'] = True
        redirect('teachers')

    if add_teacher_form.submit_add.data and add_teacher_form.validate_on_submit():
        new_teacher = Teacher(f_name=add_teacher_form.f_name.data, s_name=add_teacher_form.s_name.data, initials=add_teacher_form.initials.data,
                              email=add_teacher_form.email.data, title=add_teacher_form.title.data)
        new_teacher.add()
        return redirect('teachers')

    if find_edit_id_form.submit_edit_id.data and find_edit_id_form.validate_on_submit():
        teacher_id = find_id_teacher(find_edit_id_form.s_name.data)
        teacher_to_edit = Teacher.query.get(teacher_id)
        edit_teacher_form.process(obj=teacher_to_edit)
        cache.set('teacher_to_edit_id', teacher_id)
        show_options['edit'] = True
        return render_template('teachers.html', teacher_table=teacher_table, edit_teacher_form=edit_teacher_form, teacher_to_edit=teacher_to_edit,
                               find_edit_id_form=find_edit_id_form, show_options=show_options)

    if edit_teacher_form.submit_edit.data and edit_teacher_form.validate_on_submit():
        teacher_to_edit = Teacher.query.get(cache.get('teacher_to_edit_id'))
        teacher_to_edit.edit(edit_teacher_form)
        return redirect('teachers')

    if delete_teacher_form.submit_delete_id and delete_teacher_form.validate_on_submit():
        teacher_id = find_id_teacher(delete_teacher_form.s_name.data)
        Teacher.query.filter(Teacher.id == teacher_id).delete()
        db.session.commit()
        return redirect('teachers')

    teacher_table = [teacher.iterable() for teacher in Teacher.query.all()]
    return render_template('teachers.html', teacher_table=teacher_table, add_teacher_form=add_teacher_form, find_edit_id_form=find_edit_id_form,
                           edit_teacher_form=edit_teacher_form, delete_teacher_form=delete_teacher_form, show_options=show_options)


@app.route('/rooms', methods=['GET', 'POST'])
@login_required
def rooms():
    room_table = [room.iterable() for room in Room.query.all()]

    find_edit_id_form = FindEditIdFormRoom()
    edit_room_form = EditRoomForm()
    add_room_form = AddRoomForm()
    delete_room_form = DeleteRoomForm()
    room_form = RoomForm()
    fields = ['r_name', 'building']
    show_options = {
        'edit_id': False,
        'edit': False,
        'add': False,
        'delete': False
    }

    data = request.form

    if 'add' in data:
        show_options['add'] = True
        redirect('rooms')

    if 'edit' in data:
        show_options['edit_id'] = True
        redirect('rooms')

    if 'delete' in data:
        show_options['delete'] = True
        redirect('rooms')

    if add_room_form.submit_add.data and add_room_form.validate_on_submit():
        new_room = Room(r_name=add_room_form.r_name.data, building=add_room_form.building.data)
        new_room.add()
        return redirect('rooms')

    if find_edit_id_form.submit_edit_id.data and find_edit_id_form.validate_on_submit():
        room_id = find_id_room(find_edit_id_form.r_name.data)
        room_to_edit = Room.query.get(room_id)
        edit_room_form.process(obj=room_to_edit)
        cache.set('room_to_edit_id', room_id)
        show_options['edit'] = True
        return render_template('rooms.html', room_table=room_table, edit_room_form=edit_room_form, room_to_edit=room_to_edit,
                               find_edit_id_form=find_edit_id_form, show_options=show_options)

    if edit_room_form.submit_edit.data and edit_room_form.validate_on_submit():
        room_to_edit = Room.query.get(cache.get('room_to_edit_id'))
        room_to_edit.edit(edit_room_form)
        return redirect('rooms')

    if delete_room_form.submit_delete_id and delete_room_form.validate_on_submit():
        room_id = find_id_room(delete_room_form.r_name.data)
        Room.query.filter(Room.id == room_id).delete()
        db.session.commit()
        return redirect('rooms')

    room_table = [room.iterable() for room in Room.query.all()]
    return render_template('rooms.html', room_table=room_table, add_room_form=add_room_form, find_edit_id_form=find_edit_id_form,
                           edit_room_form=edit_room_form, delete_room_form=delete_room_form, show_options=show_options)


@app.route('/activities', methods=['GET', 'POST'])
@login_required
def activities():

    add_activity_form = AddActivityForm()
    show_options = {
        'edit_id': False,
        'edit': False,
        'add': False,
        'delete': False
    }

    data = request.form

    if 'add' in data:
        show_options['add'] = True
        redirect('activities')

    if 'edit' in data:
        show_options['edit_id'] = True
        redirect('activities')

    if 'delete' in data:
        show_options['delete'] = True
        redirect('activities')

    if add_activity_form.submit_add.data and add_activity_form.validate_on_submit():
        teacher_s_names = []
        for k, v in data.items(multi=True):
            if 'teacher' in k:
                teacher_s_names.append(v)

        r_id = find_id_room(add_activity_form.r_name.data)

        new_activity = Activity(a_name=add_activity_form.a_name.data, r_id=r_id, week=add_activity_form.week.data, day=add_activity_form.day.data,
                                time=add_activity_form.time.data, max_attendees=add_activity_form.max_attendees.data,
                                food_supplied=add_activity_form.food_supplied.data)
        new_activity.add()

        teacher_ids = [find_id_teacher(t_s_name) for t_s_name in teacher_s_names]
        for t_id in teacher_ids:
            TeacherActivityLink(a_id=new_activity.id, t_id=t_id).add()

        return redirect('activities')

    activities_table = [activity.iterable_datetime() for activity in Activity.query.all()]

    return render_template('activities.html', activities_table=activities_table, add_activity_form=add_activity_form, show_options=show_options)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/sort', methods=['GET', 'POST'])
@login_required
def sort():

    sort_teachers_form = SortTeachersForm()
    sort_rooms_form = SortRoomsForm()
    sort_activities_form = SortActivitiesForm()
    show_options = {
        'teachers': False,
        'rooms': False,
        'activities': False,
    }

    data = request.form
    table = None

    if 'teachers' in data:
        show_options['teachers'] = True
        redirect('sort')

    if 'rooms' in data:
        show_options['rooms'] = True
        redirect('sort')

    if 'activities' in data:
        show_options['activities'] = True
        redirect('sort')

    if sort_teachers_form.submit_sort_teachers.data and sort_teachers_form.validate_on_submit():
        if sort_teachers_form.activity.data:
            a_id = find_id_activity(sort_teachers_form.activity.data)
            teacher_list = db.session.query(Teacher).filter(Teacher.activities.any(TeacherActivityLink.a_id == a_id))
            table = [t.iterable() for t in teacher_list]
        redirect('sort')

    if sort_rooms_form.submit_sort_rooms.data and sort_rooms_form.validate_on_submit():
        if sort_rooms_form.activity.data:
            a_id = find_id_activity(sort_rooms_form.activity.data)
            room_list = Room.query.filter(Room.activities.any(Activity.id == a_id))
            table = [r.iterable() for r in room_list]
        redirect('sort')

    if sort_activities_form.submit_sort_activities.data and sort_activities_form.validate_on_submit():
        activity_list_1 = []
        activity_list_2 = []
        if sort_activities_form.teacher.data:
            t_id = find_id_teacher(sort_activities_form.teacher.data)
            activity_list_1 = db.session.query(Activity).filter(Activity.teachers.any(TeacherActivityLink.t_id == t_id))

        if sort_activities_form.room.data:
            r_id = find_id_room(sort_activities_form.room.data)
            activity_list_2 = Activity.query.filter(Activity.r_id == r_id)

        activity_list = intersection(activity_list_1, activity_list_2)
        table = [a.iterable() for a in activity_list]
        redirect('sort')

    return render_template('sort.html', show_options=show_options, sort_teachers_form=sort_teachers_form, sort_rooms_form=sort_rooms_form,
                           sort_activities_form=sort_activities_form, table=table)


def find_id_teacher(name):
    best_ratio, t_id = 0, None
    for teacher in Teacher.query.all():
        if fuzz.ratio(name, teacher.s_name) > best_ratio:
            best_ratio, t_id = fuzz.ratio(name, teacher.s_name), teacher.id
    return t_id


def find_id_room(r_name):
    best_ratio, t_id = 0, None
    for room in Room.query.all():
        if fuzz.ratio(r_name, room.r_name) > best_ratio:
            best_ratio, t_id = fuzz.ratio(r_name, room.r_name), room.id
    return t_id


def find_id_activity(a_name):
    best_ratio, a_id = 0, None
    for activity in Activity.query.all():
        if fuzz.ratio(a_name, activity.a_name) > best_ratio:
            best_ratio, a_id = fuzz.ratio(a_name, activity.a_name), activity.id
    return a_id


def intersection(*arrays):
    arrays = [arr for arr in arrays if arr != []]
    return list(set.intersection(*[set(arr) for arr in arrays]))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#
#     if form.validate_on_submit():
#         flash('Login requested for user {}, remember_me={}'.format(
#             form.username.data, form.remember_me.data))
#         return redirect('/index')
#     return render_template('login.html', title='Sign In', form=form)


if __name__ == '__main__':
    app.run()
