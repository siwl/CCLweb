from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import student
from .. import db
from ..models import User, Student, Session, Permission
from ..email import send_email
from .forms import NewStudentForm, RegisterSessionForm, EditProfileForm
from ..decorators import authority_required


#ST1
@student.route('/student?student=<student_id>', methods=['GET', 'POST'])
@login_required
def profile(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    user_id = student.user_id
    user = User.query.filter_by(id=user_id).first_or_404()
    sessions = student.get_sessions()
    if not current_user.has_student(student) and not current_user.is_admin() \
    and not current_user.is_teacing(student):
        abort(403)
    return render_template('student/student.html', student=student, user = user, sessions = sessions)


#ST2
@student.route('/add?user=<user_id>', methods=['GET', 'POST'])
@login_required
@authority_required(Permission.ADMIN)
def addstudent(user_id):
    form = NewStudentForm()
    if form.validate_on_submit():
        student = Student(last_name = form.lastname.data,
                    first_name = form.firstname.data,
                    middle_name = form.middlename.data,
                    chinese_name = form.chname.data,
                    birthday = form.birthday.data,
                    user = User.query.filter_by(id=user_id).first_or_404())
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('user.account',user_id=user_id))
    return render_template("student/addstudent.html", form=form)


#ST3
@student.route('/edit?student=<student_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    form = EditProfileForm()
    if form.validate_on_submit():
        student.last_name = form.lastname.data
        student.first_name = form.firstname.data
        student.middle_name = form.middlename.data
        student.chinese_name = form.chinesename.data
        db.session.add(student)
        flash('The student profile has been updated.')
        return redirect(url_for('.profile', student_id=student.id))
    form.firstname.data = student.first_name
    form.lastname.data = student.last_name
    form.middlename.data = student.middle_name
    form.chinesename.data = student.chinese_name
    return render_template('student/edit_student.html', form=form, student=student)


#S
@student.route('/sessionlist??student=<student_id>', methods=['GET', 'POST'])
@login_required
def sessionlist(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    sessions = Session.query.all()
    return render_template('student/sessionlist.html', sessions=sessions, student=student)




#ST4
@student.route('/register?student=<student_id>&session=<session_id>', methods=['GET', 'POST'])
@login_required
def register(student_id,session_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    session = Session.query.filter_by(id=session_id).first_or_404()
    student.register(session)
    flash('Student %s are now enrolled.'%(student.first_name))
    return redirect(url_for('.profile',student_id=student.id))


@student.route('/register?student=<student_id>', methods=['GET', 'POST'])
@login_required
def enroll(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    session = Session.query.filter_by(id=session_id).first_or_404()
    student.register(session)
    flash('You are noe enrolled.')
    return redirect(url_for('.profile',student_id=student.id))


#ST5
@student.route('/browse', methods=['GET', 'POST'])
def browse():
    students = Student.query.all()
    return render_template("student/student_browse.html", students=students)

@student.route('/quit?student=<student_id>&session=<session_id>', methods=['GET', 'POST'])
def quit():
    pass


@student.route('/delete?student=<student_id>', methods=['GET', 'POST'])
def delete(student_id):
    student = Student.query.filter_by(id=student_id).first_or_404()
    if not current_user.has_student(student) and not current_user.is_admin():
        abort(403)
    db.session.delete(student)
    db.session.commit()
    flash('Student is deleted.')
    return render_template('ccl.html')