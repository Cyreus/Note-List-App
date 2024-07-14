import uuid
from flask_migrate import Migrate
from models import db, Elements, Circles
from flask import Flask, render_template, request, redirect, url_for
import hmac
import hashlib
import base64
from flask import current_app

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cyreus:2003ocak9A!@localhost/notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'AyXak4783nsk89jré!'

db.init_app(app)

migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_notes')
def add_notes():
    return render_template('add_notes.html')


@app.route('/add', methods=['POST'])
def add_note():
    val = uuid.uuid4()
    message = str(val).encode('utf-8')
    secret_key = current_app.secret_key.encode('utf-8')
    signature = hmac.new(secret_key, message, hashlib.sha256).digest()
    hashed = base64.urlsafe_b64encode(signature).decode('utf-8')
    title = request.form['title']
    detail = request.form.getlist('detail')
    new_title = Elements(title=title, noteKey=hashed)
    db.session.add(new_title)
    db.session.commit()
    for d in detail:
        new_detail = Circles(detail=d, hashKey=hashed)
        db.session.add(new_detail)
    db.session.commit()

    return render_template('add_notes.html')


@app.route('/notes', methods=['GET'])
def get_notes():
    notes_x = Elements.query.all()
    notes_y = Circles.query.all()

    return render_template('notes.html', notes_x=notes_x, notes_y=notes_y)


@app.route('/delete_note/<key>', methods=['POST'])
def delete_note(key):
    note = Elements.query.filter_by(noteKey=key).first()
    try:
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for('get_notes'))

    except:
        return "There was a problem deleting that note."


@app.route('/note/<key>')
def note_details(key):
    try:
        note = Elements.query.filter_by(noteKey=key).first()
        if note:
            details = Circles.query.filter_by(hashKey=key).all()
            detail_list = [d.detail for d in details]

            return render_template('note_details.html', title=note.title, details=detail_list, key=key)
        else:
            return 'Note does not exist.'
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run()
