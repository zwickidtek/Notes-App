## __init__.py

from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)

# import is after db declaration to prevent circular imports in models.py
from contains.models import Note

# configure database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# global variable is a list of all notes from query
notesParam = Note.query.all()


###########
# @Purpose:     home page redefines notesParam for redirects from add, delete, or update notes.
#               renders home screen template with default params without updateNote flag, rangeLength is used to sort
#               elements by time
###########
@app.route("/")
def homePage():
    notesParam = Note.query.all()
    return render_template('notesHome.html', notes=notesParam,
                           rangeLength=len(notesParam)-1, updateNote=False)


###########
# @Purpose:    check to make sure query returned valid id before loading the template with updateNote Flag
# @Param:      n - is the target note object filtered by the id
###########
@app.route("/confirmNote/<id>", methods=['POST', 'GET'])
def confirmNote(id):
    n = Note.query.filter_by(id=int(id)).first()
    if n:
        notesParam = Note.query.all()
        return render_template('notesHome.html', notes=notesParam, rangeLength=len(notesParam)-1,
                           updateNote=True, updateText=n.text, noteId=id)


###########
# @Purpose:    to update text on a note from form input, query's Note Object by id and changes
#              the text to form data newNoteNext and commiting to db with session.commit()
# @Param[in]:  priorNote - is the id of the target note sent by the hidden input element
###########
@app.route("/updateNote", methods=['POST', 'GET'])
def updateNote():
    newNoteText = request.form.get('noteUFormData')
    priorNote = request.form.get('noteId')
    n = Note.query.filter_by(id=int(priorNote)).first()
    n.text = newNoteText
    db.session.commit()
    return redirect("/")


###########
# @Purpose: to create a new note from form input, add's Note Object to database which has
#           an auto gen'd id number and time submitted at UTC
# @Param[in]: string - noteText is the form input data from the textarea element
###########
@app.route("/createNote", methods=['POST'])
def createNote():
    noteText = request.form.get('noteFormData')
    print(noteText)
    newNote = Note(text=noteText)
    db.session.add(newNote)
    db.session.commit()
    # notesParam = Note.query.all()
    return redirect("/")


###########
# @Purpose: to delete a note from app, query's database and uses .delete()
# @Param[in]: delId is the id for the note you want to delete
###########
@app.route('/delNote/<delId>')
def deleteNote(delId):
    Note.query.filter_by(id=int(delId)).delete()
    db.session.commit()
    return redirect("/")


###########
# @Purpose: to query db for all notes and get json object to use data elsewhere
# @Param[out]: Json List for all of the note objects
###########
@app.route("/listnotes")
def listNotes():
    return jsonify(json_list=[i.serialize for i in Note.query.all()])


###########
# @Purpose: to query db for a note by id
# @Param[in]: id
# @Param[out]: Json object for note with matching id
###########
@app.route("/getbyid/<id>")
def getById(id):
    n = Note.query.filter_by(id=int(id)).first()
    return jsonify(n.serialize)