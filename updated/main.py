from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, make_response
import pymysql
from dbsetup import create_connection, select_all_items, update_item
from flask_cors import CORS, cross_origin
from pusher import Pusher
import simplejson

exec(open('dbsetup.py').read())
global id
global password
global teacher_id
global teacher_password
global table_name
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# sqlite database connection for poll system
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
pusher = Pusher(app_id=u'109121', key=u'3a2a219040583d8ee1b4',
                secret=u'09b8686698072e44711d', cluster=u'mt1')
database = "./pythonsqlite.db"
conn = create_connection(database)
c = conn.cursor()


def main():
    global conn, c


@app.route('/')
# for students
def login():
    return render_template("login_page.html")

# for teachers


@app.route('/login_teacher')
def login_teacher():
    return render_template("login_page_teachers.html")

# for student


@app.route('/logout', methods=["POST"])
def logout():
    return render_template('login_page.html')

# for teachers


@app.route('/logout_teacher', methods=["POST"])
def logout_teacher():
    return render_template('login_page_teachers.html')


# for student
@app.route('/forgot_password', methods=["POST"])
def forgot_password():
    return render_template("forgot_password.html")

# for teachers


@app.route('/forgot_password_teacher', methods=["POST"])
def forgot_password_teacher():
    return render_template("forgot_password_teacher.html")

# for students


@app.route('/update_password', methods=["POST"])
def update_password():
    student_ids = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10']
    student_id = request.form['student_id1']
    upassword = request.form['password1']
    reupassword = request.form['password11']
    values = (upassword, student_id)
    if student_id not in student_ids:
        flash("Invalid Student ID",  category="error")
        return render_template('forgot_password.html')
    elif (upassword != reupassword):
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


# for teachers
@app.route('/update_password_teacher', methods=["POST"])
def update_password_teacher():
    teacher_ids = ['t1', 't2', 't3', 't4', 't5']
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


# home page for students
@app.route('/home', methods=["POST"])
def home():
    global id
    global password
    id = request.form['student_id']
    password = request.form['password']
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

@app.route('/home')
def homenew():
    return render_template('home_page.html')

# home page for teachers
@app.route('/home_teacher', methods=["POST"])
def home_teacher():
    global teacher_id
    global teacher_password
    teacher_id = request.form['teacher_id']
    teacher_password = request.form['teacher_password']
    teacher_ids = ['t1', 't2', 't3', 't4', 't5']
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

@app.route('/home_teacher')
def hometeacher():
    return render_template('home_page_teacher.html')

# attendence percentage details for subject a
# for students
@app.route('/subjecta_a_attendence', methods=["POST"])
def attendence_percentage_subject_a():
    global table_name
    table_name = "subject_a"
    print(table_name)
    student_id = id
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


# attendence percentage details for subject a
# for teachers
@app.route('/subject_a_attendence_teacher', methods=["POST"])
def attendence_percentage_subject_a_teacher():
    global table_name
    table_name = "subject_a"
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


# attendence percentage details for subject b
# for students
@app.route('/subjecta_b_attendence', methods=["POST"])
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


# attendence percentage details for subject b
# for teachers
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

# attendence percentage details for subject c
# for students


@app.route('/subjecta_c_attendence', methods=["POST"])
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


# attendence percentage details for subject c
# for teachers
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


# attendence details with date for students
@app.route('/attendence_details', methods=["POST"])
def attendence_details():
    global id
    global table_name
    student_id = id
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
        print(date_list)
        print(status_list)
        
        for i in range(0, len(date_list)):
            dict_details[date_list[i]] = status_list[i]
        print("hello")

        return render_template('attendence_details.html', data=data, Student_ID=student_id, Subject_Code=sub_code,
                               empty_dict=dict_details, len=len(date_list))
    except Exception as e:
        print(e)
        return "this is error page"


# attendence details with date for teachers
@app.route('/attendence_details_teacher', methods=["POST"])
def attendence_details_teacher():
    global table_name
    student_id = request.form['stud_id']
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

#Give Attendance
@app.route('/attend')
def attend():
    return render_template('give_attendance.html')

@app.route('/upattend', methods=['POST'])
def upattend():
    sub = request.form['sub']
    dat = request.form['date']
    b11 = request.form['b1']
    b22 = request.form['b2']
    b33 = request.form['b3']
    b44 = request.form['b4']
    b55 = request.form['b5']
    b66 = request.form['b6']
    b77 = request.form['b7']
    b88 = request.form['b8']
    b99 = request.form['b9']
    b1010 = request.form['b10']
    print(b11)
    #inserting a table name
    #select date and subject table name
    #date = '{}'.format(dat)
    date = dat
    table_name='subject_{}'.format(sub)
    corr_table='subject_{}_attendence'.format(sub)
    #print(date)A
    details = {'b1': b11, 'b2': b22,'b3':b33,'b4':b44,'b5':b55,'b6':b66,'b7':b77,'b8':b88,'b9':b99,'b10':b1010}
    # details = {'100': 'A', '101': 'A', '102': 'A','103':'A','104':'A','105':'A','106':'A','107':'P','108':'P','109':'P'}
    try:
        # db = pymysql.connect(host="localhost", user="root", password="keekkeek", database="dbms", autocommit=True)
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject", database="sujithkh_maxo_project",autocommit=True)
        cur = db.cursor()
        print("connected")

        #extra
        #q="select * from subject_a"
        #cur.execute(q)
        #print(cur.fetchall())

        #####main
        query = f"alter table {table_name} add column(`%s` varchar(20))"
        #query = "alter table subject_b add column(`%s` varchar(20))"
        cur.execute(query,(date))

        #query="show columns from subject_a"
        #query="alter table subject_a drop column `%s` "

        #cur.execute(query)
        #print(cur.fetchall())

        #####updating values  #main
        date=f"'{date}'"
        print(date)
        for id, status in details.items():
            print(status, id)
            values = (status, id) #    print(values)
            update = f"update {table_name} set `{date}`=%s where student_id=%s "
            cur.execute(update, values)
            print("1 done")
        print(cur.fetchall())

        #updating the percentage table
        query = f"show columns from {table_name}"
        cur.execute(query)
        aa = cur.fetchall()
        no_of_classes_conducted = len(aa) - 2
        print(no_of_classes_conducted)
        student_ids = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10']
        # student_ids=['100','101','102','103','104','105','106','107','108','109']
        #print(len(student_ids))
        #print(student_ids[0])

        for i in range(0, len(student_ids)):
            print(i)
            bb = f"select * from {table_name} where student_id='{student_ids[i]}'"
            cur.execute(bb)
            val = cur.fetchall()
            print(val)
            #print(val[0])
            no_of_classes_attended = val[0].count('P' or 'p')
            print(no_of_classes_attended)
            attendence_percent = (no_of_classes_attended / no_of_classes_conducted) * 100
            print(attendence_percent)
            query = f"""update {corr_table} set No_of_classes_conducted='{no_of_classes_conducted}',
            No_of_classes_attended='{no_of_classes_attended}',
            percentage='{attendence_percent}'
            where student_id='{student_ids[i]}' """
            cur.execute(query)
            bbd=cur.fetchall()
            print(bbd)
            q=f"select * from {corr_table}"
            cur.execute(q)
            print(cur.fetchall())
            db.close()
            flash("Attendence Update sucessfully", category="error")
            return render_template('give_attendance.html')

    except Exception as e:
        return f"this is error page  {e}"


# Routes for poll system
@app.route('/polly')
def index():
    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True, cursorclass=pymysql.cursors.DictCursor)
        cur = db.cursor()
        query = "SELECT * FROM Questions"
        cur.execute(query)
        data = cur.fetchone()
        db.close()
        return render_template('index.html', question=data['question'], option1=data['option1'], option2=data['option2'], option3=data['option3'], option4=data['option4'])

    except Exception as e:
        return f"this is error page  {e}"


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

# quiz


@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/game')
def game():
    return render_template('game.html')


@app.route('/end')
def end():
    return render_template('end.html')

    # question form


@app.route('/question_form')
def question_form():
    return render_template('question_form.html')


@app.route('/question_review', methods=['POST'])
def question_review():
    question = request.form['question']
    option1 = request.form['option1']
    option2 = request.form['option2']
    option3 = request.form['option3']
    option4 = request.form['option4']
    correctOption = request.form['radio-set']
    try:
        db = pymysql.connect(host="sujithkh.heliohost.org", user="sujithkh_maxoproject", password="maxoproject",
                             database="sujithkh_maxo_project", autocommit=True)
        cur = db.cursor()
        query = """CREATE TABLE IF NOT EXISTS Questions(
                    question varchar(500),
                    option1 varchar(250),
                    option2 varchar(250),
                    option3 varchar(250),
                    option4 varchar(250),
                    correctOption varchar(10)
                ); """
        cur.execute(query)
        cur.execute("DELETE FROM Questions;")
        query = f"INSERT INTO Questions VALUES('{question}', '{option1}', '{option2}', '{option3}', '{option4}', '{correctOption}');"
        cur.execute(query)
        db.close()
        return render_template('question_review.html', question=question, option1=option1, option2=option2, option3=option3, option4=option4, correctOption=correctOption)

    except Exception as e:
        return f"this is error page  {e}"


if __name__ == '__main__':
    main()
    app.run(debug=True)
