from flask import redirect,flash, url_for, Flask, request, render_template, make_response
import sqlite3
from datetime import datetime
import time
timeofSleep=0
app = Flask(__name__)
import string    
import random 
app.secret_key = "hello"
def get_db_connection():
    connection = sqlite3.connect('links.db', check_same_thread=False)
    return connection
@app.route('/create', methods=['POST'])
def create():
   S = 5
   url = request.host_url
   url=str(url)
   link = request.form.get('link')
   current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   connection = get_db_connection()
   cursor = connection.cursor()
   ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))   
   cursor.execute("SELECT EXISTS(SELECT 1 FROM links WHERE id = ?)",(ran,))
   chk=cursor.fetchone()
   while list(chk)[0] == 1:
        ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        cursor.execute("SELECT EXISTS (SELECT 1 FROM links WHERE id = ?)", (ran,))
        chk = cursor.fetchone()
   owk = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))   
   cursor.execute("SELECT EXISTS(SELECT 1 FROM links WHERE id = ?)",(ran,))
   chko=cursor.fetchone()
   while list(chko)[0] == 1:
        owk = ''.join(random.choices(string.ascii_letters + string.digits, k=S))
        cursor.execute("SELECT EXISTS (SELECT 1 FROM links WHERE id = ?)", (ran,))
        chko = cursor.fetchone()
    
   cursor.execute('''INSERT INTO links (id,rlink, LV, owi, VT) VALUES (?,?, ?, ?, ?)''', (ran,link, current_time, owk, "Never"))
   connection.commit()
    
   cursor.execute('SELECT id FROM links WHERE rlink = ?', (link,))
   id = list(cursor.fetchall()[-1:][0])[0]
   connection.close()
   id=url+str(id)
   return f"<p>Your link is: {id}</p></br><p>your owner key is : {owk}</p>"
@app.route('/')
def index():
   return render_template('index.html')
@app.route('/r')
def redi():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT rid FROM links ORDER BY rid DESC LIMIT 1;')
    rid=cursor.fetchone()
    rid=random.randint(1,int(rid[0]))

    cursor.execute('SELECT rlink FROM links WHERE rid = ?', (rid,))
    link = cursor.fetchone()
    
    if not link:
    	   return "Link not found", 404
    
    link = link[0]
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute(''' UPDATE links  SET VT = VT + 1, LV = ? WHERE rid = ? ''', (current_time, rid))
    connection.commit()
    connection.close()

    time.sleep(timeofSleep)
    return redirect(link)
@app.route('/<x>')
def redirection(x):

    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('SELECT rlink FROM links WHERE id = ?', (x,))
    link = cursor.fetchone()
    
    if not link:
    	   return "Link not found", 404
    
    link = link[0]
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute(''' UPDATE links  SET VT = VT + 1, LV = ? WHERE id = ? ''', (current_time, x))
    connection.commit()
    connection.close()

    time.sleep(timeofSleep)
    return redirect(link)

@app.route('/dele', methods=['GET'])
def dele():
    owi=request.args.get("owk")
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM links WHERE owi = ?', (owi,))
    connection.commit()
    flash('deleted !')
    return redirect(url_for('index'))
@app.route('/check', methods=['POST'])
def check():
 connection = get_db_connection()
 cursor = connection.cursor()
 owi = request.form.get('owk')
 cursor.execute("SELECT EXISTS (SELECT 1 FROM links WHERE owi = ?)", (owi,))
 chke = cursor.fetchone()
 if list(chke)[0]==0 :    
  
  return "<p>Doesnt Exist !</p>"
 else:
    
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT id FROM links WHERE owi =?', (owi,))
    id = list(cursor.fetchone())[0]   

    cursor.execute('SELECT LV FROM links WHERE owi =?', (owi,))
    lv = list(cursor.fetchone())[0]
    
    cursor.execute('SELECT VT FROM links WHERE owi =?', (owi,))
    vt = list(cursor.fetchone())[0]
    connection.close()
   
    data=[id,lv,vt]
    
    return f"<p>id : {data[0]}</p> </br> <p>last visite: {data[1]}</p> </br> <p>total visits :{data[2]} </p>  </br><a href='/dele?owk={owi}'>delete</a>  "

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True,port=5001)
