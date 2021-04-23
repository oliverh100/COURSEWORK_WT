from fuzzywuzzy import fuzz
from models import Teacher, Activity, Room, TeacherActivityLink


def find_id_teacher(name):
    if type(name) != str:
        raise TypeError

    best_ratio, t_id = 0, None
    for teacher in Teacher.query.all():
        if fuzz.ratio(name.lower(), teacher.s_name.lower()) > best_ratio:
            best_ratio, t_id = fuzz.ratio(name.lower(), teacher.s_name.lower()), teacher.id
    return t_id


def find_id_room(r_name):
    if type(r_name) != str:
        raise TypeError

    best_ratio, r_id = 0, None
    for room in Room.query.all():
        if fuzz.ratio(r_name.lower(), room.r_name.lower()) > best_ratio:
            best_ratio, r_id = fuzz.ratio(r_name.lower(), room.r_name.lower()), room.id
    return r_id


def find_id_activity(a_name):
    if type(a_name) != str:
        raise TypeError

    best_ratio, a_id = 0, None
    for activity in Activity.query.all():
        if fuzz.ratio(a_name.lower(), activity.a_name.lower()) > best_ratio:
            best_ratio, a_id = fuzz.ratio(a_name.lower(), activity.a_name.lower()), activity.id
    return a_id
