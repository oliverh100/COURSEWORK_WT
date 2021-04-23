from flask import Flask, render_template, request, redirect, flash, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

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
from find_id import *


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
        print(teacher_id)
        cache.set('teacher_to_edit_id', teacher_id)
        show_options['edit'] = True
        return render_template('teachers.html', teacher_table=teacher_table, edit_teacher_form=edit_teacher_form, teacher_to_edit=teacher_to_edit,
                               find_edit_id_form=find_edit_id_form, show_options=show_options)

    if edit_teacher_form.submit_edit.data and edit_teacher_form.validate_on_submit():
        teacher_to_edit = Teacher.query.get(cache.get('teacher_to_edit_id'))
        teacher_to_edit.edit(edit_teacher_form)
        print(edit_teacher_form.title.data)
        return redirect('teachers')

    if delete_teacher_form.submit_delete_id.data and delete_teacher_form.validate_on_submit():
        teacher_to_delete = Teacher.query.filter(Teacher.s_name == delete_teacher_form.s_name.data.title()).first()
        if not teacher_to_delete:
            flash('Couldn\'t find teacher')
        else:
            activities_with_teachers = TeacherActivityLink.query.filter(TeacherActivityLink.t_id == teacher_to_delete.id).first()
            if activities_with_teachers:
                flash('Cannot delete teacher. Teacher is part of an activity')
                return redirect('teachers')
            Teacher.query.filter(Teacher.s_name == delete_teacher_form.s_name.data.title()).delete()
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

    if delete_room_form.submit_delete_id.data and delete_room_form.validate_on_submit():
        room_to_delete = Room.query.filter(Room.r_name == delete_room_form.r_name.data.upper()).first()
        if not room_to_delete:
            flash('Couldn\'t find room')
        else:
            activities_in_room = Activity.query.filter(Activity.r_id == room_to_delete.id).first()
            if activities_in_room:
                flash('Cannot delete room. It is being used for an activity')
                return redirect('rooms')
            Room.query.filter(Room.r_name == delete_room_form.r_name.data.upper()).delete()
            db.session.commit()
        return redirect('rooms')

    room_table = [room.iterable() for room in Room.query.all()]
    return render_template('rooms.html', room_table=room_table, add_room_form=add_room_form, find_edit_id_form=find_edit_id_form,
                           edit_room_form=edit_room_form, delete_room_form=delete_room_form, show_options=show_options)


@app.route('/activities', methods=['GET', 'POST'])
@login_required
def activities():
    add_activity_form = AddActivityForm()
    find_times_form = FindTimesForm()
    find_rooms_form = FindRoomsForm()
    delete_activity_form = DeleteActivityForm()
    activities_table = [activity.iterable_datetime() for activity in Activity.query.all()]

    def datetime_sorter(combined_datetime):
        weeks = ['A', 'B']
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        times = ['Before school', 'Lunch', 'After school']

        combined_datetime = combined_datetime.split()
        week = combined_datetime[1]
        day = combined_datetime[2][:-1]
        time = combined_datetime[3]

        try:
            time += ' ' + combined_datetime[4]
        except IndexError:
            pass

        week = weeks.index(week)
        day = days.index(day)
        time = times.index(time)

        return (week * 7 + day) * 3 + time

    activities_table = sorted(activities_table, key=lambda x: datetime_sorter(x[2]))
    show_options = {
        'edit_id': False,
        'edit': False,
        'add': False,
        'delete': False,
        'find_times': False,
        'find_rooms': False
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

    if 'find_times' in data:
        show_options['find_times'] = True
        redirect('activities')

    if 'find_rooms' in data:
        show_options['find_rooms'] = True
        redirect('activities')

    if add_activity_form.submit_add.data and add_activity_form.validate_on_submit():
        teacher_s_names = []
        for k, v in data.items(multi=True):
            if 'teacher' in k:
                teacher_s_names.append(v)

        r_id = find_id_room(add_activity_form.r_name.data)

        if Activity.query.filter(Activity.r_id == r_id and Activity.week == add_activity_form.week.data and Activity.day == add_activity_form.day.data and
                                 Activity.time == add_activity_form.time.data).all():
            flash('Room not available at this time')
            return redirect('activities')

        new_activity = Activity(a_name=add_activity_form.a_name.data, r_id=r_id, week=add_activity_form.week.data, day=add_activity_form.day.data,
                                time=add_activity_form.time.data, max_attendees=add_activity_form.max_attendees.data,
                                food_supplied=add_activity_form.food_supplied.data)
        new_activity.add()

        teacher_ids = [find_id_teacher(t_s_name) for t_s_name in teacher_s_names]
        for t_id in teacher_ids:
            TeacherActivityLink(a_id=new_activity.id, t_id=t_id).add()

        return redirect('activities')

    if find_times_form.submit_find_times.data and find_times_form.validate_on_submit():
        r_id = find_id_room(find_times_form.room.data)

        weeks = ['A', 'B']
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        times = ['Before school', 'Lunch', 'After school']

        all_times = {week: {day: {time: None for time in times} for day in days} for week in weeks}

        activities_in_room = Activity.query.filter(Activity.r_id == r_id).all()
        for activity in activities_in_room:
            all_times[activity.week][activity.day][activity.time] = activity

        available_times = [f'Week {week} {day}, {time}' for week in weeks for day in days for time in times if not all_times[week][day][time]]

        return render_template('activities.html', activities_table=activities_table, add_activity_form=add_activity_form, show_options=show_options,
                               available_times=available_times, find_times_form=find_times_form, available_times_room=Room.query.get(r_id).r_name)

    if find_rooms_form.submit_find_rooms.data and find_rooms_form.validate_on_submit():
        week = find_rooms_form.week.data
        day = find_rooms_form.day.data
        time = find_rooms_form.time.data

        all_rooms = {room: None for room in Room.query.all()}
        activities_at_times = Activity.query.filter(Activity.week == week, Activity.day == day, Activity.time == time).all()

        for activity in activities_at_times:
            all_rooms[Room.query.get(activity.r_id)] = activity

        available_rooms = [room.r_name for room in all_rooms if not all_rooms[room]]

        datetime = f'Week {week} {day}, {time}'

        return render_template('activities.html', activities_table=activities_table, add_activity_form=add_activity_form, show_options=show_options,
                               available_rooms=available_rooms, find_times_form=find_times_form, available_rooms_datetime=datetime)

    if delete_activity_form.submit_delete_id.data and delete_activity_form.validate_on_submit():
        activity_to_delete = Activity.query.filter(Activity.a_name == delete_activity_form.a_name.data).first()
        if not activity_to_delete:
            flash('Couldn\'t find activity')
        else:
            TeacherActivityLink.query.filter(TeacherActivityLink.a_id == activity_to_delete.id).delete()
            Activity.query.filter(Activity.a_name == delete_activity_form.a_name.data).delete()
            db.session.commit()
        return redirect('activities')

    return render_template('activities.html', activities_table=activities_table, add_activity_form=add_activity_form, show_options=show_options,
                           find_times_form=find_times_form, find_rooms_form=find_rooms_form, delete_activity_form=delete_activity_form)


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
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/sort', methods=['GET', 'POST'])
@login_required
def search():
    search_teachers_form = SearchTeachersForm()
    search_rooms_form = SearchRoomsForm()
    search_activities_form = SearchActivitiesForm()
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

    if search_teachers_form.submit_search_teachers.data and search_teachers_form.validate_on_submit():
        if search_teachers_form.activity.data:
            a_id = find_id_activity(search_teachers_form.activity.data)
            teacher_list = db.session.query(Teacher).filter(Teacher.activities.any(TeacherActivityLink.a_id == a_id))
            table = [t.iterable() for t in teacher_list]
        redirect('search')

    if search_rooms_form.submit_search_rooms.data and search_rooms_form.validate_on_submit():
        if search_rooms_form.activity.data:
            a_id = find_id_activity(search_rooms_form.activity.data)
            room_list = Room.query.filter(Room.activities.any(Activity.id == a_id))
            table = [r.iterable() for r in room_list]
        redirect('search')

    if search_activities_form.submit_search_activities.data and search_activities_form.validate_on_submit():
        activity_list_1 = []
        activity_list_2 = []
        if search_activities_form.teacher.data:
            t_id = find_id_teacher(search_activities_form.teacher.data)
            activity_list_1 = db.session.query(Activity).filter(Activity.teachers.any(TeacherActivityLink.t_id == t_id))

        if search_activities_form.room.data:
            r_id = find_id_room(search_activities_form.room.data)
            activity_list_2 = Activity.query.filter(Activity.r_id == r_id)

        activity_list = intersection(activity_list_1, activity_list_2)
        table = [a.iterable() for a in activity_list]
        redirect('search')

    return render_template('search.html', show_options=show_options, search_teachers_form=search_teachers_form, search_rooms_form=search_rooms_form,
                           search_activities_form=search_activities_form, table=table)


# def intersection(*arrays):
#     for arr in arrays:
#         if type(arr) != list:
#             raise TypeError
#     return list(set.intersection(*[set(arr) for arr in arrays]))


def intersection(*arrays):
    for arr in arrays:
        if type(arr) != list:
            raise TypeError
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
