from flask import Flask, request, jsonify
from flask_mail import Mail
from config import Config
import pandas as pd
from utils import get_info

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

count = 0

@app.route('/update_count', methods=['GET'])
def update_count():
    global count
    count = request.args.get('count', type=int)
    return f"Count updated to {count}"

@app.route('/')
def index():
    return f"<h1>{count} people in the room</h1>"

@app.route('/people_in_room')
def show_people_in_room():
    return jsonify()

@app.route('/send_mail', methods=["GET"])
def send_mail():
    from mailUtil import send_library_entry_mail    
    reg_no = request.args.get('reg_no', type=int)
    time = request.args.get('time', type=str)
    result = get_info(reg_no)
    if result is None:
        return jsonify({"error": "Invalid registration number"})
    name, email = result
    send_library_entry_mail(email, name, reg_no, time)
    return f"Mail sent to {email}"
    

if __name__ == '__main__':
    app.run(debug=True, port=8000)
