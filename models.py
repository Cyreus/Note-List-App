from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Elements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    noteKey = db.Column(db.String(45), nullable=False, unique=True)

    def __repr__(self):
        return f'<elements {self.id}>'


class Circles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    detail = db.Column(db.String(200), nullable=False)
    hashKey = db.Column(db.String(45), db.ForeignKey('elements.noteKey'), nullable=False, unique=True)

    def __repr__(self):
        return f'<circles {self.id}>'
