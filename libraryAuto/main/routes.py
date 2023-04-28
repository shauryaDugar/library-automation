from flask import request, jsonify, Blueprint, send_file
from libraryAuto.utils import get_info
from libraryAuto.mailUtil import send_library_exit_mail, send_library_entry_mail   
from libraryAuto import db
from libraryAuto.models import Record
from datetime import datetime
import csv

count = 0

main = Blueprint('main', __name__)

@main.route('/update_count', methods=['GET'])
def update_count():
    global count
    count = request.args.get('count', type=int)
    return f"Count updated to {count}"

@main.route('/')
def index():
    return f"<h1>{count} people in the room</h1>"


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
def show_people_inside():
    records = Record.query.filter_by(exit_time=None).all()
    return jsonify({"people_inside": [(rec.name, rec.reg_no, rec.entry_time) for rec in records]})

@main.route('/download_records')
def download_records():
    with open('test.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['id', 'reg_no', 'name', 'entry_time', 'exit_time'])
        for rec in Record.query.all():
            csvwriter.writerow([rec.id, rec.reg_no, rec.name, rec.entry_time, rec.exit_time])

    return send_file('../test.csv',
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name='logs.csv')
