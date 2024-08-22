from flask import redirect,url_for,Flask, request,render_template,make_response
import sqlite3
from datetime import datetime

app = Flask(__name__)
connection = sqlite3.connect('links.db', check_same_thread=False)
cursor = connection.cursor()

@app.route('/index')
def index():
   return render_template('index.html')
@app.route('/create')
def create():
    link = request.args.get('link')
    if link is None:
        return "Error: No link provided", 400
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor = connection.cursor()
    cursor.execute('''INSERT INTO links (rlink, LV, owi, VT) VALUES (?, ?, ?, ?)''', 
                   (link, current_time, 0, "0"))
    connection.commit() 

    
    cursor.execute('SELECT id FROM links WHERE rlink = ?', (link,))
    id = cursor.fetchall()
    id = list(id.pop())[0]
    print(id)
    return render_template('created.html',id=id)
    connection.close()   

@app.route('/r/<x>')
def redirection(x): 
    com="SELECT rlink FROM links WHERE id = "+x
    cursor.execute(com)
    link = cursor.fetchall()
    link=list(link[0])[0]
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        UPDATE links
        SET VT = VT + 1,
            LV = ?
        WHERE id = ?
    ''', (current_time,x))
    connection.commit() 
    connection.close()
    return redirect(link)
@app.route('/check')
def check():
    id = request.args.get('id')
    cursor.execute('SELECT LV FROM links WHERE id =?', (id,) )
    lv = cursor.fetchone()
    cursor.execute('SELECT VT FROM links WHERE id =?', (id,) )
    vt = cursor.fetchone()
    data=["id",id,"totalVisite",vt,"LastVisite",lv]
    connection.close()
    return render_template('view.html',data=data)

app.run(debug=True)