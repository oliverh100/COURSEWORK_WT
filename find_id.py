from fuzzywuzzy import fuzz
from models import Teacher, Activity, Room, TeacherActivityLink


def find_id_teacher(name):
    if type(name) != str:
        raise TypeError

    best_ratio, t_id = 0, None
    for teacher in Teacher.query.all():
        if fuzz.ratio(name, teacher.s_name) > best_ratio:
            best_ratio, t_id = fuzz.ratio(name, teacher.s_name), teacher.id
    return t_id


def find_id_room(r_name):
    if type(r_name) != str:
        raise TypeError

    best_ratio, t_id = 0, None
    for room in Room.query.all():
        if fuzz.ratio(r_name, room.r_name) > best_ratio:
            best_ratio, t_id = fuzz.ratio(r_name, room.r_name), room.id
    return t_id


def find_id_activity(a_name):
    if type(a_name) != str:
        raise TypeError

    best_ratio, a_id = 0, None
    for activity in Activity.query.all():
        if fuzz.ratio(a_name, activity.a_name) > best_ratio:
            best_ratio, a_id = fuzz.ratio(a_name, activity.a_name), activity.id
    return a_id