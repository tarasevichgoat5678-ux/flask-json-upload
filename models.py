from extensions import db

class DataEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.TIMESTAMP, nullable=False)

    def __repr__(self):
        return f'<DataEntry {self.name}>'
