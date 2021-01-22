from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, FieldList, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class MenuSelectionForm(FlaskForm):
    option = RadioField(u'Choice', choices=[('teachers', 'teachers'), ('rooms', 'rooms'), ('activities', 'activities')], validate_choice=False)


class AddTeacherForm(FlaskForm):
    f_name = StringField('First name', validators=[DataRequired()], render_kw={'placeholder': 'First Name'})
    s_name = StringField('Surname', validators=[DataRequired()], render_kw={'placeholder': 'Surname'})
    initials = StringField('Initials', validators=[DataRequired()], render_kw={'placeholder': 'Initials'})
    email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder': 'Email'})
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    submit_add = SubmitField('Submit')


class FindEditIdFormTeacher(FlaskForm):
    s_name = StringField('Surname', validators=[DataRequired()], render_kw={'placeholder': 'Surname of teacher to edit'})
    submit_edit_id = SubmitField('Submit')


class EditTeacherForm(FlaskForm):
    f_name = StringField('First name', validators=[DataRequired()], render_kw={'placeholder': 'First Name'})
    s_name = StringField('Surname', validators=[DataRequired()], render_kw={'placeholder': 'Surname Name'})
    initials = StringField('Initials', validators=[DataRequired()], render_kw={'placeholder': 'Initials'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'Email'})
    title = StringField('Title', validators=[DataRequired()], render_kw={'placeholder': 'Title'})
    submit_edit = SubmitField('Submit')


class TeacherForm(FlaskForm):
    f_name = StringField('First name', validators=[DataRequired()])
    s_name = StringField('Surname', validators=[DataRequired()])
    initials = StringField('Initials', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeleteTeacherForm(FlaskForm):
    s_name = StringField('Surname', validators=[DataRequired()], render_kw={'placeholder': 'Surname of teacher to delete'})
    submit_delete_id = SubmitField('Submit')


class AddRoomForm(FlaskForm):
    r_name = StringField('Room name', validators=[DataRequired()], render_kw={'placeholder': 'Room Name'})
    building = StringField('Building', validators=[DataRequired()], render_kw={'placeholder': 'Building'})
    submit_add = SubmitField('Submit')


class FindEditIdFormRoom(FlaskForm):
    r_name = StringField('Room name', validators=[DataRequired()], render_kw={'placeholder': 'Room Name of room to edit'})
    submit_edit_id = SubmitField('Submit')


class EditRoomForm(FlaskForm):
    r_name = StringField('Room name', validators=[DataRequired()], render_kw={'placeholder': 'Room Name'})
    building = StringField('Building', validators=[DataRequired()], render_kw={'placeholder': 'Building'})
    submit_edit = SubmitField('Submit')


class RoomForm(FlaskForm):
    r_name = StringField('Room name', validators=[DataRequired()])
    building = StringField('Building', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DeleteRoomForm(FlaskForm):
    r_name = StringField('Room name', validators=[DataRequired()], render_kw={'placeholder': 'Room Name of room to delete'})
    submit_delete_id = SubmitField('Submit')


class AddActivityForm(FlaskForm):
    a_name = StringField('Activity name', validators=[DataRequired()], render_kw={'placeholder': 'Activity Name'})
    r_name = StringField('Room name', validators=[DataRequired()], render_kw={'placeholder': 'Room Name'})
    week = SelectField('Date time', choices=[('A', 'A'), ('B', 'B')], validators=[DataRequired()])
    day = SelectField('Date time', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                            ('Friday', 'Friday')], validators=[DataRequired()])
    time = SelectField('Date time', choices=[('Before school', 'Before school'), ('Lunch', 'Lunch'), ('After school', 'After school')],
                       validators=[DataRequired()])
    max_attendees = StringField('Max attendees', validators=[DataRequired()], render_kw={'placeholder': 'Max Attendees'})
    food_supplied = StringField('Food supplied', validators=[DataRequired()], render_kw={'placeholder': 'Food supplied?'})
    teacher_list = FieldList(StringField(), min_entries=0)
    submit_add = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SortTeachersForm(FlaskForm):
    activity = StringField('Activity')
    submit_sort_teachers = SubmitField('Submit')


class SortRoomsForm(FlaskForm):
    activity = StringField('Activity')
    submit_sort_rooms = SubmitField('Submit')


class SortActivitiesForm(FlaskForm):
    teacher = StringField('Teacher')
    room = StringField('Room')
    submit_sort_activities = SubmitField('Submit')


class FindTimesForm(FlaskForm):
    room = StringField('Room', validators=[DataRequired()], render_kw={'placeholder': 'Room Name'})
    submit_find_times = SubmitField('Find available times in this room')


class FindRoomsForm(FlaskForm):
    week = SelectField('Date time', choices=[('A', 'A'), ('B', 'B')], validators=[DataRequired()])
    day = SelectField('Date time', choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                            ('Friday', 'Friday')], validators=[DataRequired()])
    time = SelectField('Date time', choices=[('Before school', 'Before school'), ('Lunch', 'Lunch'), ('After school', 'After school')],
                       validators=[DataRequired()])
    submit_find_rooms = SubmitField('Find available rooms at this time')


class DeleteActivityForm(FlaskForm):
    a_name = StringField('Activity', validators=[DataRequired()], render_kw={'placeholder': 'Activity to delete'})
    submit_delete_id = SubmitField('Submit')
