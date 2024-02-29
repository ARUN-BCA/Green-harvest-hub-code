from flask import Flask, render_template, request, session, flash, send_file

import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/NewAdmin')
def NewAdmin():
    return render_template('NewAdmin.html')


@app.route('/FarmerLogin')
def FarmerLogin():
    return render_template('FarmerLogin.html')


@app.route('/CustomerLogin')
def CustomerLogin():
    return render_template('CustomerLogin.html')


@app.route('/NewCustomer')
def NewCustomer():
    return render_template('NewCustomer.html')


@app.route('/NewFarmer')
def NewFarmer():
    return render_template('NewFarmer.html')


@app.route("/ANewMachine")
def ANewMachine():
    return render_template('ANewMachine.html')


@app.route("/ANewProduct")
def ANewProduct():
    return render_template('ANewProduct.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/AFarmerInfo")
def AFarmerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmertb  ")
    data = cur.fetchall()
    return render_template('AFarmerInfo.html', data=data)


@app.route("/newadmin", methods=['GET', 'POST'])
def newadmin():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO ownertb VALUES ('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('Owner Register successfully')
    return render_template('AdminLogin.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['oname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from ownertb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('AdminLogin.html')
        else:
            session['mob'] = data[2]
            session['add'] = data[4]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM ownertb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)


@app.route("/newmachine", methods=['GET', 'POST'])
def newmachine():
    if request.method == 'POST':
        pname = request.form['pname']
        mno = request.form['mno']
        ptype = request.form['ptype']

        rdate = request.form['rdate']
        sdate = request.form['sdate']
        htype = request.form['htype']

        price = request.form['price']
        Horsepower = request.form['Horsepower']
        sinfo = request.form['sinfo']
        info = request.form['info']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)

        file1 = request.files['file1']
        fnew1 = random.randint(1111, 9999)
        savename1 = str(fnew1) + ".png"
        file1.save("static/upload/" + savename1)

        oname = session['oname']
        mob = session['mob']
        add = session['add']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO  mechinetb VALUES ('','" + pname + "','" + mno + "','" + ptype + "','" + rdate + "','" +
            sdate + "','" + htype + "','" + price + "','" + Horsepower + "','" + savename + "','" + savename1 + "','" +
            sinfo + "','" + info + "','" + oname + "','" + mob + "','" + add + "')")
        conn.commit()
        conn.close()

    flash('New Machine Register successfully')
    return render_template('ANewMachine.html')


@app.route("/anewproduct", methods=['GET', 'POST'])
def anewproduct():
    if request.method == 'POST':
        oname = session['oname']
        pname = request.form['pname']
        ptype = request.form['ptype']
        price = request.form['price']
        qty = request.form['qty']
        info = request.form['info']
        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO   protb VALUES ('','" + pname + "','" + ptype + "','" + price + "','" + qty + "','" + info + "','" + savename + "','" + oname + "')")
        conn.commit()
        conn.close()

    flash('New Product Register successfully')
    return render_template('ANewProduct.html')


@app.route("/AMachineInfo")
def AMachineInfo():
    oname = session['oname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM mechinetb where  OwnerName='" + oname + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb where  OwnerName='" + oname + "' ")
    data1 = cur.fetchall()

    return render_template('AMachineInfo.html', data=data, data1=data1)


@app.route("/ARemove")
def ARemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from mechinetb where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('Machine  info Remove Successfully!')
    return AMachineInfo()


@app.route("/APRemove")
def APRemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from protb where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('Product  info Remove Successfully!')
    return AMachineInfo()


@app.route("/ASalesInfo")
def ASalesInfo():
    oname = session['oname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM fmbooktb where   ownername='" + oname + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fcarttb where ownername='" + oname + "' and Status='1' ")
    data1 = cur.fetchall()
    return render_template('ASalesInfo.html', data=data, data1=data1)


@app.route("/newfarmer", methods=['GET', 'POST'])
def newfarmer():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO farmertb VALUES ('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')
    return render_template('FarmerLogin.html')


@app.route("/flogin", methods=['GET', 'POST'])
def flogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['fname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from farmertb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('FarmerLogin.html')
        else:
            session['add'] = data[4]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM farmertb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('FarmerHome.html', data=data)


@app.route("/FarmerHome")
def FarmerHome():
    fname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM farmertb where UserName='" + fname + "'  ")
    data = cur.fetchall()
    return render_template('FarmerHome.html', data=data)


@app.route("/FSearchM")
def FSearchM():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM mechinetb  ")
    data = cur.fetchall()
    return render_template('FSearchM.html', data=data)


@app.route("/fsm", methods=['GET', 'POST'])
def fsm():
    if request.method == 'POST':
        ptype = request.form['ptype']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM mechinetb where  ProductType ='" + ptype + "'")
        data = cur.fetchall()
        return render_template('FSearchM.html', data=data)


@app.route("/Addm")
def Addm():
    id = request.args.get('id')
    session['mid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM mechinetb  where id='" + id + "' ")
    data = cur.fetchall()
    return render_template('FMachineBook.html', data=data)


@app.route("/fmbook", methods=['GET', 'POST'])
def fmbook():
    if request.method == 'POST':

        from datetime import datetime

        # dates in string format
        str_d1 = request.form['d1']

        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        pid = session['mid']
        uname = session['fname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM mechinetb  where  id='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[1]
            Producttype = data[3]

            htype = data[6]
            price = data[7]
            oname = data[13]


        else:
            return 'No Record Found!'

        d2 = request.form['d2']

        tprice = float(price) * float(d2)

        if htype == 'Week':
            dd = int(d2) * 7
            date_1 = datetime.datetime.strptime(str_d1, "%Y-%m-%d")
            end_date = date_1 + datetime.timedelta(days=int(dd))
        elif htype == 'Day':

            date_1 = datetime.datetime.strptime(str_d1, "%Y-%m-%d")
            end_date = date_1 + datetime.timedelta(days=int(d2))
        else:
            date_1 = datetime.datetime.strptime(str_d1, "%Y-%m-%d")
            end_date = date_1 + datetime.timedelta(days=0)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fmbooktb VALUES ('','" + uname + "','" + session[
                'add'] + "','" + ProductName + "','" + Producttype + "','" + str(
                price) + "','"+ d2 +"','"+ str(tprice) +"','" +
            htype + "','" + date + "','" + str(str_d1) + "','" + str(end_date) + "','" + oname + "','0')")
        conn.commit()
        conn.close()

        return render_template('FMPayment.html', amt=tprice)


@app.route("/fmpayment", methods=['GET', 'POST'])
def fmpayment():
    if request.method == 'POST':
        pid = session['mid']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "update   fmbooktb set status='1' where id='" + pid + "' ")
        conn.commit()
        conn.close()
        flash('Machine Book Successfully!')
        return FReport()


@app.route("/FReport")
def FReport():
    uname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM fmbooktb where   username='" + uname + "' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fcarttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fbooktb where username='" + uname + "'")
    data2 = cur.fetchall()
    return render_template('FReport.html', data=data, data1=data1, data2=data2)


@app.route("/FSearchP")
def FSearchP():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  ")
    data = cur.fetchall()
    return render_template('FSearchP.html', data=data)


@app.route("/fsp", methods=['GET', 'POST'])
def fsp():
    if request.method == 'POST':
        ptype = request.form['ptype']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM protb where  ProductType ='" + ptype + "'")
        data = cur.fetchall()

        return render_template('FSearchP.html', data=data)


@app.route("/Addp")
def Addp():
    id = request.args.get('id')
    session['pid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM protb  where id='" + id + "' ")
    data = cur.fetchall()
    return render_template('FAddCart.html', data=data)


@app.route("/Faddcart", methods=['GET', 'POST'])
def Faddcart():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        pid = session['pid']
        uname = session['fname']
        qty = request.form['qty']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM protb  where  id='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[1]
            Producttype = data[2]
            price = data[3]
            cQty = data[4]

            Image = data[6]
            oname = data[7]

        else:
            return 'No Record Found!'

        tprice = float(price) * float(qty)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fcarttb VALUES ('','" + uname + "','" + ProductName + "','" + Producttype + "','" + str(
                price) + "','" + str(qty) + "','" + str(tprice) + "','" +
            Image + "','" + date + "','0','','" + oname + "','" + session['add'] + "')")
        conn.commit()
        conn.close()

        flash('Add To Cart  Successfully')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM protb  where id='" + pid + "' ")
        data = cur.fetchall()
        return render_template('FAddCart.html', data=data)







@app.route("/FCart")
def FCart():
    uname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]
    else:
        return 'No Record Found!'

    return render_template('FCart.html', data=data, tprice=tprice)


@app.route("/FRemoveCart")
def FemoveCart():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from fcarttb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product Remove Successfully!')

    uname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]

    return render_template('FCart.html', data=data, tprice=tprice)


@app.route("/fppayment", methods=['GET', 'POST'])
def fppayment():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        uname = session['fname']
        cname = request.form['cname']
        Cardno = request.form['cno']
        Cvno = request.form['cvno']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  fcarttb where UserName='" + uname + "' and Status='0' ")
        data1 = cursor.fetchone()
        if data1:
            tqty = data1[0]
            tprice = data1[1]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) As count  FROM fbooktb ")
        data = cursor.fetchone()
        if data:
            bookno = data[0]
            print(bookno)

            if bookno == 'Null' or bookno == 0:
                bookno = 1
            else:
                bookno += 1

        else:
            return 'Incorrect username / password !'

        bookno = 'BOOKID' + str(bookno)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "update   fcarttb set status='1',Bookid='" + bookno + "' where UserName='" + uname + "' and Status='0' ")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fbooktb VALUES ('','" + uname + "','" + bookno + "','" + str(tqty) + "','" + str(
                tprice) + "','" + cname + "','" + Cardno + "','" + Cvno + "','" + date + "')")
        conn.commit()
        conn.close()

    return FReport()


@app.route("/FNewProduct")
def FNewProduct():
    uname = session['fname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb where fname='" + uname + "'")
    data = cur.fetchall()
    return render_template('FNewProduct.html', data=data)


@app.route("/FSales")
def FSales():
    uname = session['fname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where fname='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()
    return render_template('FSales.html', data1=data1)


@app.route("/fnewproduct", methods=['GET', 'POST'])
def fnewproduct():
    if request.method == 'POST':
        pname = request.form['pname']
        ptype = request.form['ptype']
        price = request.form['price']
        qty = request.form['qty']
        info = request.form['info']
        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)
        uname = session['fname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO   uprotb VALUES ('','" + pname + "','" + ptype + "','" + price + "','" + qty + "','" + info + "','" + savename + "','" + uname + "')")
        conn.commit()
        conn.close()

    flash('New Product Register successfully')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb where fname='" + uname + "'")
    data = cur.fetchall()
    return render_template('FNewProduct.html', data=data)


@app.route("/FPRemove")
def FPRemove():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from uprotb where id='" + id + "'")
    conn.commit()
    conn.close()
    flash('Product  info Remove Successfully!')
    return FNewProduct()


@app.route("/newcust", methods=['GET', 'POST'])
def newcust():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('NewCustomer.html')


@app.route("/clogin", methods=['GET', 'POST'])
def clogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['cname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('CustomerLogin.html')
        else:
            session['mob'] = data[2]
            session['add'] = data[4]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('CustomerHome.html', data=data)


@app.route("/CustomerHome")
def CustomerHome():
    uname = session['cname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb where username='" + uname + "'  ")
    data = cur.fetchall()

    return render_template('CustomerHome.html', data=data)


@app.route("/CSearch")
def CSearch():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb ")
    data = cur.fetchall()
    return render_template('CSearch.html', data=data)


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        ptype = request.form['ptype']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM uprotb where  ProductType ='" + ptype + "'")
        data = cur.fetchall()

        return render_template('CSearch.html', data=data)


@app.route("/Add")
def Add():
    id = request.args.get('id')
    session['pid'] = id
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM uprotb  where id='" + id + "' ")
    data = cur.fetchall()
    return render_template('AddCart.html', data=data)


@app.route("/addcart", methods=['GET', 'POST'])
def addcart():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')

        pid = session['pid']
        uname = session['cname']
        qty = request.form['qty']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM uprotb  where  id='" + pid + "'")
        data = cursor.fetchone()

        if data:
            ProductName = data[1]
            Producttype = data[2]
            price = data[3]
            cQty = data[4]

            Image = data[6]
            fname = data[7]

        else:
            return 'No Record Found!'


        tprice = float(price) * float(qty)
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO carttb VALUES ('','" + uname + "','" + ProductName + "','" + Producttype + "','" + str(
                price) + "','" + str(qty) + "','" + str(tprice) + "','" +
            Image + "','" + date + "','0','','" + fname + "','"+ session['mob'] +"','"+session['add']+"')")
        conn.commit()
        conn.close()

        flash('Add To Cart  Successfully')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM uprotb  where id='" + pid + "' ")
        data = cur.fetchall()
        return render_template('AddCart.html', data=data)





@app.route("/Cart")
def Cart():
    uname = session['cname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]
    else:
        return 'No Record Found!'

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)


@app.route("/RemoveCart")
def RemoveCart():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from carttb where id='" + id + "'")
    conn.commit()
    conn.close()

    flash('Product Remove Successfully!')

    uname = session['cname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
    data1 = cursor.fetchone()
    if data1:
        tqty = data1[0]
        tprice = data1[1]

    return render_template('Cart.html', data=data, tqty=tqty, tprice=tprice)


@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        uname = session['cname']
        cname = request.form['cname']
        Cardno = request.form['cno']
        Cvno = request.form['cvno']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  sum(Qty) as qty ,sum(Tprice) as Tprice   FROM  carttb where UserName='" + uname + "' and Status='0' ")
        data1 = cursor.fetchone()
        if data1:
            tqty = data1[0]
            tprice = data1[1]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  count(*) As count  FROM booktb ")
        data = cursor.fetchone()
        if data:
            bookno = data[0]
            print(bookno)

            if bookno == 'Null' or bookno == 0:
                bookno = 1
            else:
                bookno += 1

        else:
            return 'Incorrect username / password !'




        bookno = 'BOOKID' + str(bookno)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "update   carttb set status='1',Bookid='" + bookno + "' where UserName='" + uname + "' and Status='0' ")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO booktb VALUES ('','" + uname + "','" + bookno + "','" + str(tqty) + "','" + str(
                tprice) + "','" + cname + "','" + Cardno + "','" + Cvno + "','" + date + "')")
        conn.commit()
        conn.close()
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
        data1 = cur.fetchall()

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
        cur = conn.cursor()
        cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
        data2 = cur.fetchall()

    return render_template('CBookInfo.html', data1=data1, data2=data2)


@app.route("/CBookInfo")
def CBookInfo():
    uname = session['cname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
    data2 = cur.fetchall()

    return render_template('CBookInfo.html', data1=data1, data2=data2)


@app.route("/ESalesInfo")
def ESalesInfo():
    uname = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  carttb where UserName='" + uname + "' and Status='1' ")
    data1 = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  booktb where username='" + uname + "'")
    data2 = cur.fetchall()

    return render_template('ESalesInfo.html', data1=data1, data2=data2)


@app.route("/alogin", methods=['GET', 'POST'])
def alogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            return render_template('AHome.html', data=data)

        else:
            flash('Username or Password is wrong')
            return render_template('Admin.html')


@app.route("/AOwnerInfo")
def AOwnerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  ownertb  ")
    data = cur.fetchall()
    return render_template('AOwnerInfo.html', data=data)


@app.route("/AHome")
def AHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  regtb  ")
    data = cur.fetchall()
    return render_template('AHome.html', data=data)


@app.route("/AAFarmerInfo")
def AAFarmerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='4greenharvestdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  farmertb  ")
    data = cur.fetchall()
    return render_template('AAFarmerInfo.html', data=data)


@app.route("/Admin")
def Admin():
    return render_template('Admin.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
