from server import app
from EventSystem import Eventsystem
from event import User, Event,Seminar,Session,db
from flask import Flask, render_template, request, url_for, redirect,flash
from flask_login import current_user, login_required, login_user, logout_user


@app.route('/')
def index():
    return render_template('index.html', events = Event.query.all(), seminars = Seminar.query.all())
    
@app.route('/about')
def about():
    return render_template('about.html')
    
    
@app.route('/login/',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        zid = request.form['zid']
        password = request.form['password']

        if Eventsystem.check_digital(zid):
            if Eventsystem.validate_login(int(zid), password):
                login_user(Eventsystem.validate_login(int(zid), password))
                return redirect(url_for('index'))
            else:
                return render_template('login.html', val = True, message = 'Invalid zid or passsword')
        else:
            return render_template('login.html', val = True, message = 'Please enter zid as an integer')
    return render_template('login.html')


@app.route('/post/',methods = ['POST','GET'])
@login_required
def post():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        capacity = request.form['capacity']
        detail = request.form['detail']
        status = 'OPEN'

        if Eventsystem.check_data(start,end) and Eventsystem.check_digital(capacity):
            event = Event(title,detail,start,end,capacity,status,current_user.name)
            db.session.add(event)
            db.session.commit()
            return redirect(url_for('index'))
        elif Eventsystem.check_data(start,end) == False:
            return render_template('post.html', post = True, post_info = 'End date should less than start data!')
        elif Eventsystem.check_digital(capacity) == False:
            return render_template('post.html', post = True, post_info = 'Enter capacity as integer!')

    return render_template('post.html')

@app.route('/info/<eventId>',methods = ['POST','GET'])
@login_required
def info(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    return render_template('info.html', event = event)


@app.route('/seminarinfo/<seminarId>',methods = ['POST','GET'])
@login_required
def seminarinfo(seminarId):
    seminar = Seminar.query.filter_by(seminar_id = int(seminarId)).one()
    sessions = seminar.seminar_all.all()
    return render_template('seminarinfo.html', seminar = seminar, sessions = sessions)


@app.route('/cancele/<eventId>',methods = ['POST','GET'])
@login_required
def cancele(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    event.status = 'CANCELED'
    db.session.add(event)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/cance/',methods = ['POST','GET'])
@login_required
def cance():
    return render_template('canele.html',events = Event.query.all())

@app.route('/register/<eventId>',methods = ['POST','GET'])
@login_required
def register(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    user = User.query.filter_by(zid = current_user.zid).one()

    if user in event.events_all.all():
        flash('You alreay register this event!')
    else:
        event.users.append(user)
        # user.events.append(event)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/dashboard/')
@login_required
def dashboard():
    user = User.query.filter_by(zid = current_user.zid).one()
    return render_template('dashboard.html',regists = user.event_users_all.all())

@app.route('/user_curr/')
@login_required
def user_curr():
    user = User.query.filter_by(zid = current_user.zid).one()
    return render_template('usercurr.html',regists = user.events_all.all())

@app.route('/user_info/<eventId>',methods = ['POST','GET'])
@login_required
def user_info(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    return render_template('userinfo.html', event = event)

@app.route('/user_past/',methods = ['POST','GET'])
@login_required
def user_past():
    user = User.query.filter_by(zid = current_user.zid).one()
    return render_template('userpast.html', regists = user.event_users_all.all())


@app.route('/user_cancele/<eventId>',methods = ['POST','GET'])
@login_required
def user_cancele(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    user = User.query.filter_by(zid = current_user.zid).one()
    if user in event.users:
        event.users.remove(user)
        # user.events.remove(event)
        db.session.commit()
    else:
        return render_template('userinfo.html',val = True, message = 'deregister', event = event)

@app.route('/currpost/',methods = ['POST','GET'])
@login_required
def currpost():
    events = Event.query.filter_by(creater = current_user.name).all()
    return render_template('currpost.html',events = events)

@app.route('/pastpost/',methods = ['POST','GET'])
@login_required
def pastpost():
    events = Event.query.filter_by(creater = current_user.name).all()
    return render_template('pastpost.html',events = events)

@app.route('/info/<eventId>/participant/',methods = ['POST','GET'])
@login_required
def participant(eventId):
    event = Event.query.filter_by(event_id = int(eventId)).one()
    return render_template('participant.html',user = event.event_users_all.all())

@app.route('/postSeminar/',methods = ['POST','GET'])
@login_required
def postSeminar():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        capacity = request.form['capacity']
        detail = request.form['detail']
        convenor = request.form['convenor']
        status = 'OPEN'

        if Eventsystem.check_data(start,end) and Eventsystem.check_digital(capacity):
            seminar = Seminar(title,detail,start,end,capacity,status,current_user.name, convenor)
            db.session.add(seminar)
            db.session.commit()
            return redirect(url_for('index'))
        elif Eventsystem.check_data(start,end) == False:
            return render_template('postseminar.html', post = True, post_info = 'End date should less than start data!')
        elif Eventsystem.check_digital(capacity) == False:
            return render_template('postseminar.html', post = True, post_info = 'Enter capacity as integer!')

    return render_template('postseminar.html')

@app.route('/Seminarcancele/<SeminarId>',methods = ['POST','GET'])
@login_required
def Seminarcancele(SeminarId):
    seminar = Seminar.query.filter_by(seminar_id = int(SeminarId)).one()
    seminar.status = 'CANCELED'
    db.session.add(seminar)
    db.session.commit()
    return redirect(url_for('index'))


"""
这一部分还没写完
"""
@app.route('/seminarinfo/<SeminarId>/addsession',methods = ['POST','GET'])
@login_required
def addsession(SeminarId):
    seminar = Seminar.query.filter_by(seminar_id = int(SeminarId)).one()
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        capacity = request.form['capacity']
        detail = request.form['detail']
        speaker = request.form['speaker']
        status = 'OPEN'
        if Eventsystem.check_data(start,end) and Eventsystem.check_digital(capacity):
            session = Session(title,detail,start,end,capacity,status,current_user.name, speaker)
            db.session.add(session)
            db.session.commit()
            seminar.sessions.append(session)
            db.session.commit()
            return redirect(url_for('index'))
        elif Eventsystem.check_data(start,end) == False:
            return render_template('postsession.html', post = True, post_info = 'End date should less than start data!')
        elif Eventsystem.check_digital(capacity) == False:
            return render_template('postsession.html', post = True, post_info = 'Enter capacity as integer!')
    return render_template('postsession.html')

@app.route('/sessioninfo/<sessionId>',methods = ['POST','GET'])
@login_required
def sessioninfo(sessionId):
    sessions= Session.query.filter_by(session_id = sessionId).one()
    return render_template('sessioninfo.html', sessions = sessions)


@app.route('/registsession/<sessionId>',methods = ['POST','GET'])
@login_required
def registsession(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    user = User.query.filter_by(zid = current_user.zid).one()

    if user in session.sessions_all.all():
        flash('You alreay register this event!')
    else:
        session.users.append(user)
        # user.events.append(event)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/Sessioncancele/<sessionId>',methods = ['POST','GET'])
@login_required
def Sessioncancele(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    session.status = 'CANCELED'
    db.session.add(session)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/sessioninfo/<sessionId>/participant_session/',methods = ['POST','GET'])
@login_required
def participant_session(sessionId):
    session = Session.query.filter_by(session_id = int(sessionId)).one()
    return render_template('participant_session.html',user = session.sessions_all.all())


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



