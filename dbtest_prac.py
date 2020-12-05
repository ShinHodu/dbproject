from flask flask
import sqlite3

app=Flask(_name_)

@app.route('/')
@app.route('/index')
def hello():
db=sqlite3.connect("dbtest.db")
db.row_factory=sqlite3.Row
items=db.execute(
//쿼리
    'SELECT sName, GPA FROM STUDENT'
).fetchall()
/*html*/
output=''
for item in items:
    output +=item['sName']+'<br>'
    output +=item['GPA']+'<br>'
   
    return output

if _name_=='__main__':
app.debug=True
app.run()