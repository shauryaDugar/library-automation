from libraryAuto import login_manager
import os
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

class Admin(User):
    def __init__(self, id, name, password):
        super().__init__(id, name, password)
    

admins = [Admin(1, 'admin', os.environ.get('ADMIN_PASSWORD'))]

@login_manager.user_loader
def load_user(user_id):
    for admin in admins:
        if admin.id == int(user_id):
            return admin
        return None
    