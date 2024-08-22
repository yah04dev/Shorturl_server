from flask import redirect,url_for,Flask, request,render_template,make_response
import sqlite3
app = Flask(__name__)
connection = sqlite3.connect('links.db', check_same_thread=False)
cursor = connection.cursor()

@app.route('/index')
def index():
   return render_template('index.html')
@app.route('/create')
def create():
   link = request.args.get('link')
   com="INSERT INTO links (rlink) VALUES('"+link+"');"
   cursor.execute(com)
   com="SELECT id FROM links WHERE rlink = "+link
   id = cursor.fetchall()
   id=list(id[0])[0]
   return render_template('created.html',id=id)
   

@app.route('/r/<x>')
def redirection(x): 
    com="SELECT rlink FROM links WHERE id = "+x
    cursor.execute(com)
    link = cursor.fetchall()
    link=list(link[0])[0]
    return redirect(link)
  
app.run()