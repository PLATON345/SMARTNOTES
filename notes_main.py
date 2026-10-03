#почни тут створювати додаток з розумними замітками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QListWidget,QLineEdit,QTextEdit,QInputDialog,QHBoxLayout,QVBoxLayout
import json
import os
app = QApplication([])
notes_file = 'notes_data.json'
if os.path.exists(notes_file):
    with open(notes_file,'r',encoding = 'utf-8')as file:
        notes = json.load(file)
else:
    notes = {
        'get start':{
            'text':'welcome to smart notes',
            'tags':['start','end']
        }
    }
    with open(notes_file,'w',encoding = 'utf-8')as file:
        json.dump(notes,file,ensure_ascii = False,indent = 2)
w = QWidget()
w.setWindowTitle('smartnote')
w.resize(900,600)
ListnoteLabel = QLabel('list of notes')
listnotes = QListWidget()
Btnnotecreate = QPushButton('create note')
Btnnotedel = QPushButton('delete note')
Btnnotesave = QPushButton('save note')
listtaglabel = QLabel('list of tags')
listtag = QListWidget()
fildtag = QLineEdit()
Btntagadd= QPushButton('add tag')
Btndeletetag = QPushButton('delete tag')
Btntagfind = QPushButton('serchbytag')
fildtext = QTextEdit()

mainlayout = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(fildtext)
col2.addWidget(ListnoteLabel)
col2.addWidget(listnotes)
row1 = QHBoxLayout()
row1.addWidget(Btnnotecreate)
row1.addWidget(Btnnotedel)
col2.addLayout(row1)
col2.addWidget(Btnnotesave)

col2.addWidget(listtaglabel)
col2.addWidget(listtag)
col2.addWidget(fildtag)
row2 = QHBoxLayout()
row2.addWidget(Btntagadd)
row2.addWidget(Btndeletetag)
col2.addLayout(row2)
col2.addWidget(Btntagfind)

mainlayout.addLayout(col1,2)
mainlayout.addLayout(col2,1)
w.setLayout(mainlayout)

def show_note():
    name = listnotes.selectedItems()[0].text()
    fildtext.setText(notes[name]['text'])
    listtag.clear()
    listtag.addItems(notes[name]['tags'])
def addnote():
    notename,ok = QInputDialog.getText(w,'addnote','note name')
    if ok and notename.strip()!='':
        notes[notename ]={'text':'','tags':[]}
        listnotes.addItem(notename)
        listtag.addItems(notes[notename]['tags'])
def savenote():
    if listnotes.selectedItems():
        name = listnotes.selectedItems()[0].text()
        notes[name]['text'] = fildtext.toPlainText()
        with open(notes_file,'w',encoding = 'utf-8')as file:
            json.dump(notes,file,ensure_ascii = False,indent = 2)
def deletenote():
    if listnotes.selectedItems():
        name = listnotes.selectedItems()[0].text()
        del notes[name]
        listnotes.clear()
        listtag.clear()
        fildtext.clear()
        listnotes.addItems(notes)
        with open(notes_file,'w',encoding = 'utf-8')as file:
            json.dump(notes,file,ensure_ascii = False,indent = 2)
def addtag():
    if listnotes.selectedItems():
        name = listnotes.selectedItems()[0].text()
        tag = fildtag.text().strip()
        if tag and not tag in notes[name]['tags']:
            notes[name]['tags'].append(tag)
            listtag.addItem(tag)
            fildtag.clear()
            with open(notes_file,'w',encoding = 'utf-8')as file:
                json.dump(notes,file,ensure_ascii = False,indent = 2)
def deletetag():
    if listtag.selectedItems():
        name = listnotes.selectedItems()[0].text()
        tag = listtag.selectedItems()[0].text()
        notes[name]['tags'].remove(tag)
        listtag.clear()
        listtag.addItems(notes[name]['tags'])
        with open(notes_file,'w',encoding = 'utf-8')as file:
            json.dump(notes,file,ensure_ascii = False,indent = 2)
def findtag():
    tag = fildtag.text().strip()
    if tag:
        notesfiltered = {}
        for note in notes:
            if tag in notes[note]['tags']:
                notesfiltered[note] = notes[note]
        listnotes.clear()
        listtag.clear()
        listnotes.addItems(notesfiltered)
    else:
        listnotes.clear()
        listtag.clear
        listnotes.addItems(notes)



listnotes.itemClicked.connect(show_note)
Btnnotecreate.clicked.connect(addnote)
Btnnotesave.clicked.connect(savenote)
Btnnotedel.clicked.connect(deletenote)
Btntagadd.clicked.connect(addtag)
Btndeletetag.clicked.connect(deletetag)
Btntagfind.clicked.connect(findtag)
listnotes.addItems(notes)


w.show()
app.exec_()