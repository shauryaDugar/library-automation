from flask_mail import Message
from libraryAuto import mail 
from threading import Thread

#threading needed for mail sending to be done in the background
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_library_entry_mail(mail_id, name, reg_no, time):
    msg = Message('Library Entry Mail Notification',
            sender='librarymnnit@gmail.com', recipients=[mail_id])
    msg.body = f'Entry for {name} ({reg_no}) recorded into the library at {time}.'
    from app import app 
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

def send_library_exit_mail(mail_id, name, reg_no, time):
    msg = Message('Library Exit Mail Notification',
                  sender='librarymnnit@gmail.com', recipients=[mail_id])
    msg.body = f'Exit for {name} ({reg_no}) recorded from the library at {time}.'
    from app import app 
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

