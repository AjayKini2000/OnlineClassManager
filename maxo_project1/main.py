from flask import Flask, request, render_template, redirect, url_for,flash,jsonify, make_response
import pymysql
from dbsetup import create_connection, select_all_items, update_item
from flask_cors import CORS, cross_origin
from pusher import Pusher
import simplejson

global id
global password
global teacher_id
global teacher_password
global table_name
app=Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#sqlite database connection for poll system
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
pusher = Pusher(app_id=u'109121', key=u'3a2a219040583d8ee1b4', secret=u'09b8686698072e44711d', cluster=u'mt1')
database = "./pythonsqlite.db"
conn = create_connection(database)
c = conn.cursor()

def main():
	global conn, c


@app.route('/')
#for students
def login():
    return render_template("login_page.html")

#for teachers
@app.route('/login_teacher')
def login_teacher():
    return render_template("login_page_teachers.html")

#for student
@app.route('/logout',methods=["POST"])
def logout():
    return render_template('login_page.html')

#for teachers
@app.route('/logout_teacher',methods=["POST"])
def logout_teacher():
    return render_template('login_page_teachers.html')


#for student
@app.route('/forgot_password',methods=["POST"])
def forgot_password():
    return render_template("forgot_password.html")

#for teachers
@app.route('/forgot_password_teacher',methods=["POST"])
def forgot_password_teacher():
    return render_template("forgot_password_teacher.html")

#for students
@app.route('/update_password',methods=["POST"])
def update_password():
    student_ids=['b1','b2','b3','b4','b5','b6','b7','b8','b9','b10']
    student_id=request.form['student_id1']
    upassword = request.form['password1']
    reupassword = request.form['password11']
    values=(upassword,student_id)
    if student_id not in student_ids:
        flash("Invalid Student ID",  category="error")
        return render_template('forgot_password.html')
    elif (upassword !=reupassword):
        flash("Passwords do not match!!! Please try again", category="error")
        return render_template('forgot_password.html')
    else:
        try:
            db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                                 database="sujithkh_maxo_project", autocommit=True)
            cur = db.cursor()
            query = "update student_details set password=%s where student_id=%s "
            cur.execute(query, values)
            print("updated")
            flash("Password updated. Please Login", category="error")
            db.close()
            return render_template('forgot_password.html')
        except Exception as e:
            return "this is error page"


#for teachers
@app.route('/update_password_teacher',methods=["POST"])
def update_password_teacher():
    teacher_ids = ['t1','t2','t3','t4','t5']
    teacher_id = request.form['teacher_id1']
    upassword = request.form['pass']
    reupassword = request.form['pass1']
    values = (upassword, teacher_id)
    if teacher_id not in teacher_ids:
        flash("Invalid Teacher ID", category="error")
        return render_template('forgot_password_teacher.html')
    elif (upassword != reupassword):
        flash("Passwords do not match!!! Please try again", category="error")
        return render_template('forgot_password_teacher.html')
    else:
        try:
            db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                                 database="sujithkh_maxo_project", autocommit=True)
            cur = db.cursor()
            query = "update teacher_details set password=%s where teacher_id=%s "
            cur.execute(query, values)
            print("updated")
            flash("Password updated. Please Login", category="error")
            db.close()
            return render_template('forgot_password_teacher.html')
        except Exception as e:
            return "this is error page"


#home page for students
@app.route('/home',methods=["POST"])
def home():
    global id
    global password
    id=request.form['student_id']
    password=request.form['password']
    student_ids = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10']
    if id not in student_ids:
        flash("Invalid Student Id", category="error")
        return redirect(url_for('login'))
    else:
        try:
            db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                                 database="sujithkh_maxo_project", autocommit=True)
            cur = db.cursor()
            query = "select * from student_details"
            exe = cur.execute(query)
            data = cur.fetchall()
            db.close()
            for i in range(0, len(data)):
                if id == str(data[i][0]) and password == str(data[i][1]):
                    return render_template("home_page.html")

            flash("Invalid Password", category="error")
            return redirect(url_for('login'))
        except Exception as e:
            return "this is error page"



#home page for teachers
@app.route('/home_teacher',methods=["POST"])
def home_teacher():
    global teacher_id
    global teacher_password
    teacher_id=request.form['teacher_id']
    teacher_password=request.form['teacher_password']
    teacher_ids=['t1','t2','t3','t4','t5']
    if teacher_id not in teacher_ids:
        flash("Invalid Student Id", category="error")
        return redirect(url_for('login_teacher'))
    else:
        try:
            db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                                 database="sujithkh_maxo_project", autocommit=True)
            cur = db.cursor()
            query = "select * from teacher_details"
            exe = cur.execute(query)
            data = cur.fetchall()
            db.close()
            for i in range(0, len(data)):
                if teacher_id == str(data[i][0]) and teacher_password == str(data[i][1]):
                    return render_template("home_page_teacher.html")

            flash("Invalid Password", category="error")
            return redirect(url_for('login_teacher'))
        except Exception as e:
            return "this is error page"





#attendence percentage details for subject a
#for students
@app.route('/subjecta_a_attendence',methods=["POST"])
def attendence_percentage_subject_a():
    global table_name
    table_name = "subject_a"
    print(table_name)
    student_id=id
    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        query = "select * from subject_a_attendence where student_id=(%s) "
        studentid = (student_id)
        q = cur.execute(query, studentid)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage.html", data=data)

    except Exception as e:
        return "this is error page"


#attendence percentage details for subject a
#for teachers
@app.route('/subject_a_attendence_teacher', methods=["POST"])
def attendence_percentage_subject_a_teacher():
    global table_name
    table_name="subject_a"
    print(table_name)
    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        q = "select subject_code from subject_a_attendence"
        cur.execute(q)
        sub_code_tuple = cur.fetchone()
        sub_code = sub_code_tuple[0]
        query = "select * from subject_a_attendence "
        q = cur.execute(query)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage_teacher.html", data=data, subject_code=sub_code)


    except Exception as e:
        return "this is error page"


#attendence percentage details for subject b
#for students
@app.route('/subjecta_b_attendence',methods=["POST"])
def attendence_percentage_subject_b():
    student_id = id
    global table_name
    table_name = "subject_b"
    print(table_name)
    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        query = "select * from subject_b_attendence where student_id=(%s) "
        studentid = (student_id)
        q = cur.execute(query, studentid)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage.html", data=data)
    except Exception as e:
        return "this is error page"



#attendence percentage details for subject b
#for teachers
@app.route('/subject_b_attendence_teacher', methods=["POST"])
def attendence_percentage_subject_b_teacher():
    global table_name
    table_name = "subject_b"
    print(table_name)
    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        q = "select subject_code from subject_b_attendence"
        cur.execute(q)
        sub_code_tuple = cur.fetchone()
        sub_code = sub_code_tuple[0]

        query = "select * from subject_b_attendence "
        q = cur.execute(query)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage_teacher.html", data=data, subject_code=sub_code)
    except Exception as e:
        return "this is error page"

#attendence percentage details for subject c
#for students
@app.route('/subjecta_c_attendence',methods=["POST"])
def attendence_percentage_subject_c():
    global table_name
    table_name = "subject_c"
    student_id = id
    print(table_name)

    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        query = "select * from subject_c_attendence where student_id=(%s) "
        studentid = (student_id)
        q = cur.execute(query, studentid)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage.html", data=data)
    except Exception as e:
        return "this is error page"


#attendence percentage details for subject c
#for teachers
@app.route('/subject_c_attendence_teacher', methods=["POST"])
def attendence_percentage_subject_c_teacher():
    global table_name
    table_name = "subject_c"
    print(table_name)
    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        q = "select subject_code from subject_c_attendence"
        cur.execute(q)
        sub_code_tuple = cur.fetchone()
        sub_code = sub_code_tuple[0]
        query = "select * from subject_c_attendence"
        q = cur.execute(query)
        data = cur.fetchall()
        db.close()
        return render_template("attendence_percentage_teacher.html", data=data, subject_code=sub_code)
    except Exception as e:
        return "this is error page"


#attendence details with date for students
@app.route('/attendence_details', methods=["POST"])
def attendence_details():
    global id
    global table_name
    student_id=id
    table = table_name
    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        q = f"select subject_code from {table} where student_id= '{student_id}' "
        cur.execute(q)
        sub_code_tuple = cur.fetchone()
        sub_code = sub_code_tuple[0]

        query = f"select * from {table} where student_id='{student_id}'"
        cur.execute(query)
        data = cur.fetchall()

        status_list = []
        for i in data:
            for j in range(0, len(i)):
                if i[j] == None:
                    status_list.append('None')
                elif i[j].startswith('P') or i[j].startswith('p') or i[j].startswith('A') or i[j].startswith('a'):
                    status_list.append(i[j])
                else:
                    continue

        query = f"show columns from  {table}"
        cur.execute(query)
        column_names = cur.fetchall()
        db.close()
        date_list = []

        for i in column_names:
            if i[0].startswith("s"):
                continue
            else:
                inverted_comma_date = i[0][1:-1]
                date_list.append(inverted_comma_date)


        dict_details = {}

        for i in range(0, len(date_list)):
            dict_details[date_list[i]] = status_list[i]


        return render_template('attendence_details.html', data=data, Student_ID=student_id, Subject_Code=sub_code,
                               empty_dict=dict_details, len=len(date_list))
    except Exception as e:
        return "this is error page"


#attendence details with date for teachers
@app.route('/attendence_details_teacher',methods=["POST"])
def attendence_details_teacher():
    global table_name
    student_id=request.form['stud_id']
    table = table_name



    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        q = f"select subject_code from {table} where student_id= '{student_id}' "
        cur.execute(q)
        sub_code_tuple = cur.fetchone()
        sub_code = sub_code_tuple[0]

        query = f"select * from {table} where student_id='{student_id}'"
        cur.execute(query)
        data = cur.fetchall()
        status_list = []
        for i in data:
            for j in range(0, len(i)):
                if i[j] == None:
                    status_list.append('None')
                elif i[j].startswith('P') or i[j].startswith('p') or i[j].startswith('A') or i[j].startswith('a'):
                    status_list.append(i[j])
                else:
                    continue

        query = f"show columns from {table}"
        cur.execute(query)
        db.close()
        column_names = cur.fetchall()
        date_list = []

        for i in column_names:
            if i[0].startswith("s"):
                continue
            else:
                inverted_comma_date = i[0][1:-1]
                date_list.append(inverted_comma_date)


        dict_details = {}

        for i in range(0, len(date_list)):
            print(len)
            dict_details[date_list[i]] = status_list[i]


        return render_template('attendence_details.html', data=data, Student_ID=student_id, Subject_Code=sub_code,
                               empty_dict=dict_details, len=len(date_list))
    except Exception as e:
        return "this is error page"

#Routes for poll system
@app.route('/polly')
def index():
	return render_template('index.html')

@app.route('/admin')
def admin():
	return render_template('admin.html')

@app.route('/vote', methods=['POST'])
def vote():
	data = simplejson.loads(request.data)
	update_item(c, [data['member']])
	output = select_all_items(c, [data['member']])
	pusher.trigger(u'poll', u'vote', output)
	return request.data

#quiz 
@app.route('/start')
def start():
	return render_template('start.html')

@app.route('/game')
def game():
	return render_template('game.html')

@app.route('/end')
def end():
	return render_template('end.html')



if __name__ =='__main__':
    main()
    app.run(debug=True)