from flask import Flask, request, url_for, render_template, redirect, session
import datetime

# sqllite import(사용가능하게 설정)
import sqlite3

app = Flask(__name__) 

@app.route('/')
@app.route('/mainpage')
def mainpage(): 
    return render_template("mainpage.html")

@app.route('/searchRestaurant', methods=['GET', 'POST'])
def select():
    search=request.form.get("restaurant_name", "")
    conn=sqlite3.connect('C:/Users/응나야/AppData/Local/Programs/Python/finalproject/finalproject.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql="SELECT Name, Tel FROM Restaurant WHERE Name LIKE ?"
    cur.execute(sql, ('%'+search+'%',))
    rows = cur.fetchall()
    conn.close()

    return render_template('searchRestaurant.html', data=rows)


@app.route('/customerinfo' , methods=['GET', 'POST'])
def customerinfohtml():
    rName=request.args.get("rName", "")
    rTel=request.args.get("rTel", "")

    return render_template("customerinfo.html", rName=rName, rTel=rTel)

@app.route('/saveCustomerinfo' , methods=['GET', 'POST'])
def saveCustomerinfo():
    try:         
        fullname=request.form.get("fullname", "")
        phoneNum=request.form.get("phoneNum", "")
        accompany=request.form.get("accompany", "")
        rName=request.form.get("rName", "")
        rTel=request.form.get("rTel", "")
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

        conn=sqlite3.connect('C:/Users/응나야/AppData/Local/Programs/Python/finalproject/finalproject.db')
        cur = conn.cursor()
        sql="INSERT INTO Waitings (cName, cPhone, cAccompany, rName, rTel, timestamp) VALUES (?,?,?,?,?,?)"
        cur.execute(sql, (fullname,phoneNum,accompany,rName,rTel,nowDatetime))
        conn.commit()

        print("Recod successfully added")
    except Exception as e:
        conn.rollback()
        print('db error:', e)
        print("Error in insert operation")
    finally : 
        conn.close()
        return redirect(url_for('waitingListForCustomer',rName=rName))
        
@app.route('/waitingListForCustomer' , methods=['GET', 'POST'])
def waitingListForCustomer():
    rName=request.args.get("rName", "")
    
    conn=sqlite3.connect('C:/Users/응나야/AppData/Local/Programs/Python/finalproject/finalproject.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql="SELECT cName, cPhone, cAccompany, timestamp FROM Waitings WHERE rName = ? ORDER BY timestamp"
    cur.execute(sql, (rName,))
    rows = cur.fetchall()
    conn.close()

    return render_template("waitingListForCustomer.html", rName=rName, data=rows)

@app.route('/restaurantLogin')
def restaurantinfohtml():
    return render_template("restaurantLogin.html")

@app.route('/restaurantList')
def restaurantList():
    rName=request.args.get("userId", "")

    conn=sqlite3.connect('C:/Users/응나야/AppData/Local/Programs/Python/finalproject/finalproject.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql="SELECT cName, cPhone, cAccompany, timestamp FROM Waitings WHERE rName = ? ORDER BY timestamp"
    cur.execute(sql, (rName,))
    rows = cur.fetchall()
    conn.close()

   # return render_template("waitingListForCustomer.html", rName=rName, data=rows)
    #cursor.execute("select * from Waitings where rName='식당'")
    return render_template("restaurantList.html", rName=rName, data=rows)

@app.route('/delWaitingListForRsr')
def delWaitingListForRsr():
    try:         
        cName=request.args.get("cName", "")
        cPhone=request.args.get("cPhone", "")
        rName=request.args.get("rName", "")

        conn=sqlite3.connect('C:/Users/응나야/AppData/Local/Programs/Python/finalproject/finalproject.db')
        cur = conn.cursor()
        sql="DELETE FROM Waitings WHERE cName = ? AND cPhone = ?"
        cur.execute(sql, (cName,cPhone))
        conn.commit()

        print("Recod successfully delete")
    except Exception as e:
        conn.rollback()
        print('db error:', e)
        print("Error in delete operation")
    finally : 
        conn.close()
        return redirect(url_for('restaurantList',userId=rName))

@app.route('/restaurantLogin_proc',methods=['post'])
def restaurantLogin_proc():
    userId=request.form.get("ID", "")
    userPwd=request.form.get("PSWD", "")

    if len(userId)==0 or len(userPwd)==0:
         return '로그인 정보를 입력해주세요.'
    else:
        conn=sqlite3.connect('C:/Users/응나야/AppData/Local/Programs/Python/finalproject/finalproject.db')
        conn.isolation_level = None
        conn.row_factory = sqlite3.Row
        cur=conn.cursor()
        sql="select ID, PSWD from RestaurantLogin where ID=?"
        cur.execute(sql, (userId,))
        rows=cur.fetchall()
        conn.close()
        for rs in rows:
            if userId==rs[0] and userPwd==rs[1]:
                session['logFlag']=True
                session['userId']=userId

                return redirect(url_for('restaurantList',userId=userId))
            else:
                return '<script> alert("다시 로그인해주세요.");  document.location="/restaurantLogin" </script>'


    

if __name__ == '__main__':
    app.secret_key='123456789'
    app.run(host='0.0.0.0', port='8080', debug=True)