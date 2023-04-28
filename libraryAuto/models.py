from libraryAuto import db

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_no = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(40), nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False)
    exit_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"Record('{self.id}', '{self.reg_no}', '{self.name}', '{self.entry_time}', '{self.exit_time}')"