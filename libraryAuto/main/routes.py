from flask import request, jsonify, Blueprint
from libraryAuto.utils import get_info
from libraryAuto.mailUtil import send_library_exit_mail, send_library_entry_mail   

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