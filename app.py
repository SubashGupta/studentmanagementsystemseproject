from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import join
from sqlalchemy.sql import select
from datetime import date
import sqlite3
import sqlalchemy as db1
from flask_caching import Cache
cache = Cache()
global fullname, admissionNo, fname,lname,mails,admissionNo,fullname, person_type, dealing_class, sections
fullname = ""
admissionNo = ""

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProjectDB.sqlite3'
app.config['SECRET_KEY'] = "secret key"
con = sqlite3.connect("ProjectDB.sqlite3",check_same_thread=False)
db = SQLAlchemy(app)                #initializing the SQLAlchemy database.

class Login(db.Model):      #database fields Creation with constraints for login
    mailid = db.Column(db.String(255), primary_key=True)
    password = db.Column(db.String(255))
    timestamp = db.Column(db.String(50))

    def __init__(self,mailid,password,timestamp):
        self.mailid=mailid
        self.password=password
        self.timestamp=timestamp
def flnames():
    full = g.user
    full_1 = full.split(" ")
    if len(full_1) == 2:
        f_name = full_1[0].lower()
        l_name = full_1[1].lower()
    elif len(full_1) >2 :
        l_name = full_1[-1].lower()
        full_1.pop()
        f_name = " ".join(c for c in full_1).lower()
    return (l_name,f_name)
def add_to_dict(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value

@app.route("/", methods=['GET','POST'])
def initial():
    session.clear()
    return render_template("initial.html")
 
@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':    #check the form method is post or not
        session.pop('user',None)            #making sure the seesion user is poped out and made None
        firstname=request.form['firstname'].lower()
        print(firstname)
        lastname=request.form['lastname'].lower()
        print(lastname)
        mailid_signup=request.form['mailid'].lower()
        print(mailid_signup)
        admissionno_signup=request.form['admissionnumber']
        print(admissionno_signup)
        password_signup=request.form['password']
        print(password_signup)
        confirmpassword_signup=request.form['confirmpassword']
        print(confirmpassword_signup)
        with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
            cur = con.cursor()
            res = cur.execute("SELECT First_Name,Last_Name,Email,Admission_id FROM studentdetails WHERE First_Name = ? and Last_Name = ?  and Admission_Id= ? ;",[firstname,lastname,admissionno_signup]).fetchall()
            print(res)
        if len(res) > 0:
            if password_signup == confirmpassword_signup:
                if len(password_signup) <=8:
                    flash("Password should be more than 8 characters. Kindly Re-Enter the Signup form.",'error')
                    return redirect(url_for('signup'))
                else:
                    with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
                        cur = con.cursor()
                        check_in_logintable = cur.execute("SELECT mailid,password FROM Login WHERE Admission_Id= ?;",[admissionno_signup]).fetchall()
                        if len(check_in_logintable) > 0:
                            flash("An account already exist with this student details kindly login with the existing credentials else contact Administrator",'error')
                            return redirect(url_for('signup'))
                        else:
                            from datetime import datetime
                            p=datetime.now()
                            type_signup = "student"
                            res = cur.execute("INSERT INTO Login (Admission_id,mailid,password,type,timestamp) VALUES(?, ?, ?, ?, ?);",[admissionno_signup,mailid_signup,password_signup,type_signup,p])
                            con.commit()
                            flash("Account was created successfully. Kindly login with your credentials.",'error')
                            return redirect(url_for("beforelogin"))
            else:
                flash("Password and Confirm Password were not matched. Kindly Re-Enter the Signup form.",'error')
                return redirect(url_for('signup'))
        else:
            flash("Due to Mismatch with the existing system data we are unable to find the student details and create an account. Kindly contact administrator.",'error')
            return redirect(url_for('signup'))
    else:
        return render_template("Signup.html")
    return render_template("Signup.html")

@app.route('/login',methods=['GET','POST'])
def beforelogin():
    if request.method == 'POST':    #check the form method is post or not
        session.pop('user',None)            #making sure the seesion user is poped out and made None
        mailid=request.form['username']
        password=request.form['password']
        #if the name and password are not present in the db then it will show an error
        #x =Login.query.filter_by(mailid=mailid , password=password).first()    #checking whether they are in db userstore table or not
        #print(x)
        with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
            cur = con.cursor()
            res = cur.execute("SELECT mailid,password,type FROM Login WHERE mailid= ? and password = ? ;",[mailid,password]).fetchall()
            print(type(res))
            print(res)
        if len(res) > 0:
            #session['user']=mailid                #Making the username as a session for the login  purpose
            with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
                cur = con.cursor()              #creating a cursor object
                from datetime import datetime
                p=datetime.now()
                e="UPDATE Login SET timestamp = ? WHERE mailid = ? and password =? ; "
                cur.execute(e,[p,mailid,password])            #updating the timestamp of the user everytime he/she logs in
                con.commit()                          #saving the changes in the db using commit function
                if (res[0][2] == "student"):
                    login_studentdetailsquery = cur.execute("SELECT First_Name,Last_Name,Email,Admission_id, person_type FROM studentdetails WHERE Email= ? ;",[mailid]).fetchall()
                    print(login_studentdetailsquery)
                    if len(login_studentdetailsquery) > 0:
                        #global fname,lname,mails,admissionNo,fullname, person_type, dealing_class, sections
                        fname = login_studentdetailsquery[0][0]
                        lname = login_studentdetailsquery[0][1]
                        mails = login_studentdetailsquery[0][2]
                        admissionNo = login_studentdetailsquery[0][3]
                        person_type = login_studentdetailsquery[0][4]
                        fullname = fname.capitalize()+" "+lname.capitalize()
                        session['user'] = fullname
                        add_to_dict(session, 'admissionNumber', admissionNo)
                        add_to_dict(session, 'user_type', person_type)
                        
                    else:
                        flash("Unable to find the student details, kindly contact system administrator.",'error')
                        return redirect(url_for('beforelogin'))
                    return redirect(url_for('home'))
                elif res[0][2] == "class teacher" :
                    login_teacherdetailsquery = cur.execute("SELECT First_Name,Last_Name,Email,ClassTeacherId,type, Dealing_Class, Section FROM classteacherdetails WHERE Email= ? ;",[mailid]).fetchall()
                    print(login_teacherdetailsquery)
                    if len(login_teacherdetailsquery) > 0:
                        #global fname,lname,mails,admissionNo,fullname, person_type, dealing_class, sections
                        fname = login_teacherdetailsquery[0][0]
                        lname = login_teacherdetailsquery[0][1]
                        mails = login_teacherdetailsquery[0][2]
                        admissionNo = login_teacherdetailsquery[0][3]
                        person_type = login_teacherdetailsquery[0][4]
                        dealing_class = login_teacherdetailsquery[0][5]
                        sections = login_teacherdetailsquery[0][6]
                        fullname = fname.capitalize()+" "+lname.capitalize()
                        session['user'] = fullname
                        add_to_dict(session, 'admissionNumber', admissionNo)
                        add_to_dict(session, 'user_type', person_type)
                    else:
                        flash("Unable to find the teacher details, kindly contact system administrator.",'error')
                        return redirect(url_for('beforelogin'))
                    return redirect(url_for('homeT'))
                elif res[0][2] == "principal" :
                    login_principalsquery = cur.execute("SELECT First_Name,Last_Name,Email,ClassTeacherId,type FROM classteacherdetails WHERE Email= ? ;",[mailid]).fetchall()
                    print(login_principalsquery)
                    if len(login_principalsquery) > 0:
                        #global fname,lname,mails,admissionNo,fullname, person_type, dealing_class, sections
                        fname = login_principalsquery[0][0]
                        lname = login_principalsquery[0][1]
                        mails = login_principalsquery[0][2]
                        admissionNo = login_principalsquery[0][3]
                        person_type = login_principalsquery[0][4]
                        fullname = fname.capitalize()+" "+lname.capitalize()
                        session['user'] = fullname
                        add_to_dict(session, 'admissionNumber', admissionNo)
                        add_to_dict(session, 'user_type', person_type)
                    else:
                        flash("Unable to find the Principal details, kindly contact system administrator.",'error')
                        return redirect(url_for('beforelogin'))
                    return redirect(url_for('homeT'))
        else:                   #Else displaying the credentials are wrong
            flash("Invalid Credentials Kindly check them.",'error')
            return redirect(url_for('beforelogin'))
    else:
        return render_template('login.html')
    return render_template('login.html')
# from werkzeug.security import generate_password_hash, check_password_hash
#-------------------------------------------------------------------------------------------------
# global user check
@app.before_request
def before_request():
    g.user=None         #setting up global user as None
    g.user1=None        #g.admissionNo=None
    if 'user' in session:           #checking if there is an user in the session
        g.user=session["user"]    #if user is there then making the user as a global session

#--------------------
 
@app.route("/ChangePwd",methods=["GET","POST"])
def ChangePwd():
    if g.user:
        if request.method == "POST":
            print("camein")
            previouspwd = request.form['previous_password']
            newpwd = request.form['New_password']
            newpwd_confirm = request.form['New_password_confirm']
            with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
                cur = con.cursor()
                pwd_check = cur.execute("SELECT password FROM Login WHERE password= ? ;",[previouspwd]).fetchall()
                if len(pwd_check)>0:
                    ADMISSION_OF_USER = session['admissionNumber']
                    print(ADMISSION_OF_USER)
                    if newpwd == newpwd_confirm:
                        if len(newpwd) <=8:
                            flash("Password should be more than 8 characters. Unable to proceed with the password change.",'error')
                            if session['user_type'] == "student":
                                return redirect(url_for("home"))
                            elif session['user_type'] == "class teacher" or session['user_type'] == "principal":
                                return redirect(url_for("homeT"))
                        else:
                            upd="UPDATE Login SET password =? WHERE Admission_id = ?; "
                            cur.execute(upd,[newpwd,ADMISSION_OF_USER])
                            con.commit()
                            print("Updated")
                            flash("Updating the password is completed.",'error')   #flashing an error message
                    else:
                        print("Not updated")
                        flash("Passwords didnot matched. Try again!","error")
                    if session['user_type'] == "student":
                        return redirect(url_for("home"))
                    elif session['user_type'] == "class teacher" or session['user_type'] == "principal":
                        return redirect(url_for("homeT"))
                else:
                    msg = "You are not entering your password. Kindly enter your actual password to proceed further."
                    flash(msg,'error')   #flashing an error message
                    if session['user_type'] == "student":
                        return redirect(url_for("home"))
                    elif session['user_type'] == "class teacher" or session['user_type'] == "principal":
                        return redirect(url_for("homeT"))
        else:
            return render_template("changepassword.html")
    return redirect(url_for("initial"))           

@app.route("/home",methods=["GET","POST"])
def home():
    if g.user:
        print("g.user : ", g.user)
        return render_template('StudentHome.html', fullnames = g.user)
    return redirect(url_for('initial'))
    
@app.route("/homeT",methods=["GET","POST"])
def homeT():
    if g.user:
        print(fullname)
        print("g.user : ", g.user)
        return render_template('TeacherHome.html', fullnames = g.user)
    return redirect(url_for('initial'))

@app.route("/StudentMyDetails",methods=["GET","POST"])
def StudentMyDetails():
    if g.user:
        print("user:",g.user)
        datavalues = []
        l_name, f_name = flnames()
        with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
            cur = con.cursor()
            datavalues = cur.execute("SELECT Admission_id, Class, Section, First_Name, Last_Name, Phone, Email, Father_Name, Mother_Name, Date_Of_Birth, Father_Phone, Mother_Phone, Father_Email, Mother_Email, Address, Class_Teacher, Class_Teacher_Phone, Class_Teacher_Email, Class_Teacher_id FROM studentdetails WHERE First_Name= ? and Last_Name = ?;",[f_name,l_name]).fetchall()
            print(datavalues)
            ClassSection = str(datavalues[0][1])+"/"+datavalues[0][2]
            print(ClassSection)
            flash("Student Data Fetch is Successful.",'error')
            return render_template("StudentMyDetails.html", data = datavalues, ClassSection = ClassSection)
    return redirect(url_for("initial"))
    
@app.route("/StudentMyAttendance",methods=["GET","POST"])
def StudentMyAttendance():
    if g.user:
        l_name,f_name = flnames()
        admission_no = session['admissionNumber']
        with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
            cur = con.cursor()
            datavalues_attendance = cur.execute("SELECT Admission_id, August,September,October,November,December,January,February, March, April FROM studentAttendance WHERE Admission_Id = ?;",[admission_no]).fetchall()
            print(datavalues_attendance)
            if len(datavalues_attendance)>0:
                flash("Student Attendance Data Fetch is Successful.",'error')
                return render_template("StudentMyAttendance.html", data = datavalues_attendance)
            else:
                flash("Attendance was not assigned for the student. Wait for the class teacher to add the attendance.","error")
                return redirect(url_for("home"))
    return redirect(url_for("initial"))

@app.route("/StudentSearch",methods=["GET","POST"])
def StudentSearchT():
    if g.user:
        if request.method == 'POST':
            searchinput = request.form['search']
            print(searchinput,type(searchinput))
            if searchinput:
                Teacher_admission_id = session['admissionNumber']
                print(Teacher_admission_id, type(Teacher_admission_id))
                if searchinput.isnumeric():
                    with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
                        cur = con.cursor()
                        if session['user_type'] == "principal":
                            Teachsearchvalues = cur.execute("SELECT Admission_id, Class, Section, First_Name, Last_Name, Phone, Email, Father_Name, Mother_Name, Date_Of_Birth, Father_Phone, Mother_Phone, Father_Email, Mother_Email, Address, Class_Teacher, Class_Teacher_Phone, Class_Teacher_Email, Class_Teacher_id FROM studentdetails WHERE Admission_id= ?;",[searchinput]).fetchall()
                        else:
                            Teachsearchvalues = cur.execute("SELECT Admission_id, Class, Section, First_Name, Last_Name, Phone, Email, Father_Name, Mother_Name, Date_Of_Birth, Father_Phone, Mother_Phone, Father_Email, Mother_Email, Address, Class_Teacher, Class_Teacher_Phone, Class_Teacher_Email, Class_Teacher_id FROM studentdetails WHERE Admission_id= ? and Class_Teacher_id = ?;",[searchinput,Teacher_admission_id]).fetchall()
                        print(Teachsearchvalues)
                        if len(Teachsearchvalues)>0:
                            Class_section = str(Teachsearchvalues[0][1])+"/"+Teachsearchvalues[0][2]
                            search_attendance = cur.execute("SELECT Admission_id, August,September,October,November,December,January,February, March, April FROM studentAttendance WHERE Admission_Id = ?;",[searchinput]).fetchall()
                            print(search_attendance)
                            if len(search_attendance) >0:
                                flash("Student Data Fetch is Successful.",'error')
                                return render_template("TeacherStudentSearchResults.html",data = Teachsearchvalues, ClassSection = Class_section, data1 = search_attendance)
                            else:
                                flash("Attendance was not added to the student by the class teacher. Only the student details are available. ","error")
                                return render_template("TeacherStudentSearchResults.html",data = Teachsearchvalues, ClassSection = Class_section, data1 = search_attendance)
                        else:
                            flash("Unable to find the student with the given input. Check if the student is assigned to your class or not.","error")
                            return redirect(url_for("StudentSearchT"))
                else:
                    flash("Please enter the vaild AdmissionNumber which are in Numbers","error")
                    return redirect(url_for("StudentSearchT"))
            else:
                flash("Please provide an input to search the student details","error")
                return redirect(url_for("StudentSearchT"))
        else:
            return render_template("TeacherStudentSearch.html")
    return redirect(url_for("initial"))
    
@app.route("/AddStudentAttendance",methods=["GET","POST"])
def AddStudentAttendanceT():
    if g.user:
        if request.method == 'POST':
            session.pop('studentAdmissionNo',None)
            searchinput = request.form['search']
            print(searchinput,type(searchinput))
            if searchinput:
                Teacher_admission_id = session['admissionNumber']
                print(Teacher_admission_id, type(Teacher_admission_id))
                if searchinput.isnumeric():
                    with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
                        cur = con.cursor()
                        if session['user_type'] == "principal":
                            searchvalues = cur.execute("SELECT Admission_id, Class, Section, First_Name, Last_Name FROM studentdetails WHERE Admission_id= ?;",[searchinput]).fetchall()
                        else:
                            searchvalues = cur.execute("SELECT Admission_id, Class, Section, First_Name, Last_Name FROM studentdetails WHERE Admission_id= ? and Class_Teacher_id = ?;",[searchinput,Teacher_admission_id]).fetchall()
                        print(searchvalues)
                        if len(searchvalues)>0:
                            Class_section = str(searchvalues[0][1])+"/"+searchvalues[0][2]
                            add_to_dict(session, 'studentAdmissionNo', searchinput)
                            search_attendance = cur.execute("SELECT Admission_id, August,September,October,November,December,January,February, March, April FROM studentAttendance WHERE Admission_Id = ?;",[searchinput]).fetchall()
                            print(search_attendance)
                            if len(search_attendance) >0:
                                flash("Student Data Fetch is Successful. Kindly enter the attendance now.",'error')
                                return render_template("Teacher_StudentAttendanceshow.html",data = searchvalues, ClassSection = Class_section, data1 = search_attendance)
                                #attendance not there you need to enter it now.
                            else:
                                search_attendance = [('', '', '','' , '', '', '', '', '', '')]
                                flash("Student does not have atleast one month attendance entered. Kindly enter the attendance now.","error")
                                return render_template("Teacher_StudentAttendanceshow.html",data = searchvalues, ClassSection = Class_section, data1 = search_attendance)
                        else:
                            flash("Unable to find the student with the given input. Check if the student is assigned to your class or not.","error")
                            return redirect(url_for("StudentSearchT"))
                else:
                    flash("Please enter the vaild AdmissionNumber or RollNumber which are in Numbers.","error")
                    return redirect(url_for("AddStudentAttendanceT"))
            else:
                flash("Please provide an input to search the student details.","error")
                return redirect(url_for("AddStudentAttendanceT"))
        else:
            return render_template("TeacherAttendanceSearch.html")
    return redirect(url_for("initial"))
    
@app.route("/SaveAttendance",methods=["GET","POST"])
def SaveAttendance():
    if g.user:
        if request.method == 'POST':
            Aug = request.form['August']
            Sept = request.form['September']
            Oct = request.form['October']
            Nov = request.form['November']
            Dec = request.form['December']
            Jan = request.form['January']
            Feb = request.form['February']
            Mar = request.form['March']
            Apr = request.form['April']
            studentadmission_number = session['studentAdmissionNo']
            print(studentadmission_number,type(studentadmission_number))
            with sqlite3.connect("ProjectDB.sqlite3") as con:    #connecting to the hosp.sqlite3 database
                cur = con.cursor()
                search_attendance = cur.execute("SELECT Admission_id FROM studentAttendance WHERE Admission_Id = ?;",[studentadmission_number]).fetchall()
                if len(search_attendance) > 0:
                    upd="UPDATE studentAttendance SET August = ?, September = ?, October = ?, November = ?, December = ?, January = ?, February = ?, March = ?, April =? WHERE Admission_id = ?; "
                    cur.execute(upd,[Aug,Sept,Oct,Nov,Dec,Jan,Feb,Mar,Apr,studentadmission_number])
                    con.commit()
                else:
                    ins = "INSERT INTO studentAttendance (Admission_id,August,September,October,November,December,January,February,March,April) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
                    cur.execute(ins,[studentadmission_number,Aug,Sept,Oct,Nov,Dec,Jan,Feb,Mar,Apr])
                    con.commit()
                flash("Student Attendance was saved Successfully. Kindly proceed with the next student.","error")
                return redirect(url_for("AddStudentAttendanceT"))
        else:
            return redirect(url_for("AddStudentAttendanceT"))
    return redirect(url_for("initial"))

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('user',None)            #popping out the created session which was created during the login
    session.pop('admissionNumber',None)
    session.pop('studentAdmissionNo',None)
    flash("logout was initiated successfully",'error')   #flashing an error message
    return redirect(url_for("initial"))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=8080, debug = True)