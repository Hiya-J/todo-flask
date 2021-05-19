from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
# import sqlite

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

class Songs(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable = True)
    #path = db.Column(db.String(500), nullable = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

@app.route('/', methods = ["GET","POST"])
def hello_world():
    if request.method == "POST":
        a = request.form['title']
        b = request.form['desc']
        todo = Todo(title = a, desc = b)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    print(allTodo)
    return render_template('index.html', allTodo=allTodo)

@app.route('/songs', methods = ["GET","POST"])
def songs():
    if request.method == "POST":
        a = request.form['name']
        song = Songs(name = a)
        db.session.add(song)
        db.session.commit()
    music = os.listdir("D:/music")
    allSong = Songs.query.all()
    return render_template('songs.html', allSong = allSong, music = music)

@app.route('/play/<int:sno>')
def play(sno):
    # music = os.listdir("D:/music")
    song = Songs.query.filter_by(sno = sno).first()
    p = "D:\music"
    os.startfile(os.path.join(p,song.name))
    return redirect("/songs")

@app.route('/delete_song/<int:sno>')
def delete_song(sno):
    son = Songs.query.filter_by(sno = sno).first()
    db.session.delete(son)
    db.session.commit()
    return redirect("/songs")

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    # print(allTodo)
    return redirect("/")

@app.route('/update/<int:sno>', methods = ['GET','POST'])
def update(sno):
    if request.method == 'POST':
        a = request.form['title']
        b = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = a
        todo.desc = b
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

if __name__ == '__main__':
    app.run(debug=True)