from flask import Flask, request, render_template, redirect, url_for,flash
import pymysql

global id
global password
app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def login():
    return render_template("login_page.html")

@app.route('/home',methods=["POST"])
def home():
    global id
    global password
    id=request.form['student_id']
  #  a=type(a)
    password=request.form['password']
   # b=type(b)
  #  db = pymysql.connect(host="localhost", user="root", password="keekkeek", database="sujith")
    db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                         database="sujithkh_maxo_project", autocommit=True)
    cur = db.cursor()
    query ="select * from student_details"
    exe = cur.execute(query)
    data = cur.fetchall()
    for i in range(0,len(data)):
        if id==str(data[i][0]) and password==str(data[i][1]):
            return render_template("home_page.html", username=id, password=password)


           # return render_template("home_page.html", username=a, password=b)

    flash("Invalid Credentials!!! Please try again", category="error")
    return redirect(url_for('login'))
         #   return render_template("home_page.html", username=a, password=b)
         #   flash('Logged in succesfully')
           # return redirect(url_for(flask1.home))
           # return redirect(url_for('home'))

@app.route('/logout',methods=["POST"])
def logout():
    return render_template('login_page.html')


@app.route('/subjecta_a_attendence',methods=["POST"])
def attendence_percentage_subject_a():
    student_id=id
    #db = pymysql.connect(host="localhost", user="root", password="keekkeek", database="sujith")
    db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                         database="sujithkh_maxo_project", autocommit=True)
    cur = db.cursor()
    #query ="select * from subjecta_att where student_id=(%s) "
    query="select * from subject_a_attendence where student_id=(%s) "
    studentid=(student_id)
    q = cur.execute(query,studentid)
    data=cur.fetchall()
    return  render_template("subject_a_attendence.html",data=data)
    #return "keekkeeekkeek"


@app.route('/subject_a', methods=["POST"])
def subject_a_details():
    global id
    student_id=id

    #db = pymysql.connect(host="localhost", user="root", password="keekkeek", database="sujith")
    db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                         database="sujithkh_maxo_project", autocommit=True)
    cur = db.cursor()
  #  q = f"select subject_code from subjecta where student_id= '{student_id}' "
    q = f"select subject_code from subject_a where student_id= '{student_id}' "
    cur.execute(q)
    sub_code_tuple=cur.fetchone()
    sub_code=sub_code_tuple[0]

    query = f"select * from subject_a where student_id='{student_id}'"
    cur.execute(query)
    data = cur.fetchall()
    status_list = []
    for i in data:
        for j in range(0, len(i)):
            if i[j] == None:
                status_list.append('None')
            elif i[j].startswith('P') or i[j].startswith('p') or i[j].startswith('N') or i[j].startswith('n'):
                status_list.append(i[j])
            else:
                continue

    query = "show columns from subject_a"
    cur.execute(query)
    column_names= cur.fetchall()
    date_list = []

    for i in column_names:
        if i[0].startswith("s"):
            continue
        else:
            inverted_comma_date=i[0][1:-1]
            date_list.append(inverted_comma_date)

    #empty_dict = {}
    dict_details ={}

    for i in range(0, len(date_list)):
        dict_details[date_list[i]] = status_list[i]

    #print(dict_details)
    return render_template('subject_a.html',data=data,Student_ID=student_id,Subject_Code=sub_code,empty_dict=dict_details,len=len(date_list))


@app.route('/insert',methods=["POST"])
def insert():
    try:
        date='03-11-2020'
        dict= {'b1':'P', 'b2':'A'}
       # db = pymysql.connect(host="localhost", user="root", password="keekkeek", database="sujith")
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)

        cur = db.cursor()
        query = "alter table subject_a add column (%s) "
        cur.execute(query,(date))
        for id,status in dict.items():
            update ="update subject_a set (%s)=(%s) where student_id=(%s) "
            values=(date,status,id)
            cur.execute(update,values)
        return "updated"
    except Exception as e:
        return "not updtes"


if __name__ =='__main__':
    app.run(debug=True, host="localhost", port=4001)