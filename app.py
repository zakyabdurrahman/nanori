from flask import Flask, render_template, jsonify, request
import sqlite3

from werkzeug.utils import redirect


app = Flask(__name__)


@app.route('/')
def index():
  return render_template('main.html')
#display kanjis with readings meanings etc

@app.route('/search')
def search():
   #create db 
  con = sqlite3.connect('Kanji Database/kanji.db')
  db = con.cursor()
  
  kanjiList = []
  kanjiInput = request.args.get("k")
  if kanjiInput != None:
    for letter in kanjiInput:
      letterdict = {
        "literal": letter
      }
      #this line so inefficient i make a function 
      #meanings to dictionary
      meanings = db.execute("SELECT meaning FROM meanings WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", letter)
      meanings = meanings.fetchall()
      letterdict["meanings"] = find(meanings)
      

      #onyomi to dictionary
      onyomis = db.execute("SELECT onyomi FROM onyomis WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", letter)
      onyomis = onyomis.fetchall()
      letterdict["onyomis"] = find(onyomis)

      #kunyomi to dictionary
      kunyomis = db.execute("SELECT kunyomi FROM kunyomis WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", letter)
      kunyomis = kunyomis.fetchall()
      letterdict["kunyomis"] = find(kunyomis)
      #nanori to dictionary
      nanoris = db.execute("SELECT nanori FROM nanoris WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", letter)
      nanoris = nanoris.fetchall()
      letterdict["nanoris"] = find(nanoris)
      
      kanjiList.append(letterdict)
      print(kanjiList)

  con.close()
  return render_template("search.html", kanjiInput=kanjiInput, kanjiList=kanjiList)

# todo: make a function that combine either the nanoris, hiraganas, katakanas based on selected mode
@app.route('/combine')
def combine():
  kanji = request.args.get("k")
  mode = request.args.get('c')
  print(kanji)
  print(mode)
  #create db 
  con = sqlite3.connect('Kanji Database/kanji.db')
  db = con.cursor()
  respon = ['combination need two']
  #make an array for readings to combine, ignore readings after . with -
  if len(kanji) >= 2:
    kanji = kanji[0:2]
  readingPool = []
  if len(kanji) < 2:
    return jsonify(respon)
  if mode == "kunyomi":
  #combine kunyomi
  #make lists of reading for each character
    for letter in kanji:
      readings = db.execute("SELECT kunyomi FROM kunyomis WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", letter)
      readings = readings.fetchall()
      readingList = toList(readings)
      readingPool.append(readingList)
    combinations = combine(readingPool[0], readingPool[1])
    print(readingPool)
    print(combinations)
  
  if mode == "onyomi":
    for letter in kanji:
      readings = db.execute("SELECT onyomi FROM onyomis WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", letter)
      readings = readings.fetchall()
      readingList = toList(readings)
      readingPool.append(readingList)
    combinations = combine(readingPool[0], readingPool[1])
    
  if mode == "nanori":
    for letter in kanji:
      readings = db.execute("SELECT nanori FROM nanoris WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", letter)
      readings = readings.fetchall()
      readingList = toList(readings)
      readingPool.append(readingList)
    combinations = combine(readingPool[0], readingPool[1])

  if mode == "kun-on":
    readings1 = db.execute("SELECT kunyomi FROM kunyomis WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", kanji[0] )
    readings1 = readings1.fetchall()
    readingList1 = toList(readings1)
    readingPool.append(readingList1)

    readings2 = db.execute("SELECT onyomi FROM onyomis WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", kanji[1] )
    readings2 = readings2.fetchall()
    readingList2 = toList(readings2)
    readingPool.append(readingList2)
    combinations = combine(readingPool[0], readingPool[1])

  if mode == "on-kun":
    readings1 = db.execute("SELECT onyomi FROM onyomis WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", kanji[0] )
    readings1 = readings1.fetchall()
    readingList1 = toList(readings1)
    readingPool.append(readingList1)

    readings2 = db.execute("SELECT kunyomi FROM kunyomis WHERE kanji_id IN(SELECT id FROM kanjis WHERE literal = ?)", kanji[1] )
    readings2 = readings2.fetchall()
    readingList2 = toList(readings2)
    readingPool.append(readingList2)
    combinations = combine(readingPool[0], readingPool[1])

  return jsonify(combinations)

#helper functions
def find(items):
  
  
  if not items:
    output = None
  else:
    itemList = set()
    for item in items:
      itemList.add(item[0])
    output = ", ".join(itemList)  
  return output
      
#list maker from sql query
def toList(items):
  itemSet = set()
  itemList = []
  if items:
    for item in items:
      go = 1
      for i in range(len(item[0])):
        
        if item[0][i] == '.' or item[0][i] == '-':
          if item[0][0:i] != '':
            itemSet.add(item[0][0:i])
          go = 0
          break
        
      if go == 1:
        itemSet.add(item[0])         
    itemList = list(itemSet)
      
      
  return itemList

#function to combine lists and return list of strings
def combine(list1, list2):
  combinations = []
  if list1:
    for text in list1:
      if not list2:
        combinations.append(text)
        break
      for item in list2:
        combi = text+item
        combinations.append(combi)
  

  return combinations