from flask import request, jsonify, Blueprint, send_file, render_template, redirect, url_for
from libraryAuto.utils import get_info
from libraryAuto.mailUtil import send_library_exit_mail, send_library_entry_mail   
from libraryAuto import db
from libraryAuto.models import Record
from datetime import datetime
import csv
from flask_login import login_user, login_required, current_user, logout_user
from libraryAuto.user import admins

main = Blueprint('main', __name__)

@main.route('/')
def index():
    recs = Record.query.filter_by(exit_time=None).all()
    today = Record.query.filter(Record.entry_time>datetime.combine(datetime.today(), datetime.min.time())).all()
    vis_month = Record.query.filter(Record.entry_time>datetime.combine(datetime.today().replace(day=1), datetime.min.time())).all()
    return render_template('home.html', count=len(recs), today=len(today), vis_month=len(vis_month), title="Home")

@main.route('/dashboard')
@login_required
def dashboard():
    data = Record.query.filter(Record.exit_time !=  None).all()
    entry_times = [record.entry_time for record in data]
    exit_times = [record.exit_time for record in data]
    visitors = list(set([record.reg_no for record in data]))
    num_entries = len(data)
    num_visitors = len(visitors)
    total_time = sum([(record.exit_time - record.entry_time).total_seconds() / 60 for record in data])
    avg_time = total_time / num_entries if num_entries > 0 else 0
    return render_template('dashboard.html', entry_times=entry_times, 
                           exit_times=exit_times, num_entries=num_entries, 
                           num_visitors=num_visitors, avg_time=avg_time, title="Dashboard")

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        for admin in admins:
            if admin.name == username and admin.password == password:
                login_user(admin, force=True)
                next_page = request.args.get('next')
                print(next_page)
                return redirect(next_page) if next_page else redirect(url_for('main.index'))

        return 'Invalid username or password'

    return render_template('login.html', title="Login")

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/send_entry_mail', methods=["GET"])
def send_entry_mail():
    reg_no = request.args.get('reg_no', type=str)
    time = request.args.get('time', type=str)
    result = get_info(reg_no)
    if result is None:
        return jsonify({"error": "Invalid registration number"})
    name, email = result
    send_library_entry_mail(email, name, reg_no, time)
    return f"Mail sent to {email}"
    

@main.route('/send_exit_mail', methods=["GET"])
def send_exit_mail():
    reg_no = request.args.get('reg_no', type=str)
    time = request.args.get('time', type=str)
    result = get_info(reg_no)
    if result is None:
        return jsonify({"error": "Invalid registration number"})
    name, email = result
    send_library_exit_mail(email, name, reg_no, time)
    return f"Mail sent to {email}"

@main.route('/add_record')
def add_record():
    reg_no = request.args.get('reg_no', type=int)
    name = request.args.get('name', type=str)
    time = request.args.get('time', type=str)
    dbtime = datetime.strptime(time, '%H:%M:%S %d-%m-%Y')
    rec = Record(reg_no=reg_no, name=name, entry_time=dbtime)
    db.session.add(rec)
    db.session.commit()
    return f"Record added successfully"

@main.route('/update_exit_time')
def update_exit_time():
    reg_no = request.args.get('reg_no', type=int)
    time = request.args.get('time', type=str)
    dbtime = datetime.strptime(time, '%H:%M:%S %d-%m-%Y')
    rec = Record.query.filter_by(reg_no=reg_no, exit_time=None).first()
    print(rec)
    rec.exit_time = dbtime
    db.session.commit()
    return f"Exit time updated successfully"

@main.route('/show_people_inside')
@login_required
def show_people_inside():
    records = Record.query.filter_by(exit_time=None).all()
    return render_template('history.html', records=records, title="People Inside")

@main.route('/download_records')
@login_required
def download_records():
    with open('test.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['id', 'reg_no', 'name', 'entry_time', 'exit_time'])
        for rec in Record.query.filter(Record.entry_time>datetime.combine(datetime.today(), datetime.min.time())).all():
            csvwriter.writerow([rec.id, rec.reg_no, rec.name, rec.entry_time, rec.exit_time])

    return send_file('../test.csv',
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='logs.csv')

@main.route('/display_records')
def display_records():
    start_time = datetime.fromisoformat(request.args.get('start_time'))
    end_time = datetime.fromisoformat(request.args.get('end_time'))
    with open('test1.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['id', 'reg_no', 'name', 'entry_time', 'exit_time'])
        for rec in Record.query.filter(Record.entry_time>start_time, Record.entry_time<end_time).all():
            csvwriter.writerow([rec.id, rec.reg_no, rec.name, rec.entry_time, rec.exit_time])

    return send_file('../test1.csv',
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='filteredLogs.csv')

@main.route('/show_recs')
@login_required
def show_recs():
    current_time = datetime.now()
    return render_template('logs.html', current_time=current_time, title="Logs")
