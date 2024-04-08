                                            STUDENT MANAGEMENT SYSTEM
                                                                                    BY K.SUBASH GUPTA

**For running this code :**

First you need to install virtual environment in the particular directory you desired.
For installation type the command in the command prompt: py -3 -m virtualenv virtualenv
Now virtual environment is installed. A folder is created in that respective directory. Copy all the files in the zip-file you download and paste them in that folder
which has a virtualenv folder.
In the command prompt go to the directory where all the files with code are there and type virtualenv\scripts\activate to activate the virtual environment

Please make sure that all the requirements in the requirements.txt file are installed prior to the running of the code by using pip commands.

Now to run the app.py file use the command in the command prompt: python app.py

Go to your localhost URL (http://127.0.0.1:5000/) or the link shown in the command prompt to view and use the application
------------------------------------------------------------------------------------------------------------------------------------

What is this application doing?

In this student management system, I have created two views, one for the students (parents) and the other for the class teachers.

**Account Creation:**

  Firstly, the student's parent will create the student account.
  An account for the teacher has already been created by the administrator. So no account creation is provided for the teacher.

**Working:**

  **Parent/Student point of view:**
  Now, when the parent logins with their child credentials (student view), they will be able to see the student's My Details page and the View Attendance page.
  On the My Details page, all the students real details will be shown. Along with the student registration details, the class teacher's name, email address, and phone number are also included.
  
  On the View Attendance page, the student's attendance details and marks will be displayed.

  **Class teacher's point of view:**
  Now, when the class teacher logs in with their credentials (in the class teacher view), they will be able to be routed to the teacher's home page. On top, in the navigation bar, they can see the Search Student and Add Attendance options.
  
  When the class teacher clicks on the search student, the search page is routed. The class teacher should enter the student registration/roll call number. Once you type the number and click the search button, the student details, if found, will be displayed. 
  
  **Note:** Only the students within the class the teacher assigned can be searched. If the registration number of the student from another class is known, it cannot be found. A class restriction is given.
  
  When the class teacher clicks on Add Attendance, the search page is routed. The class teacher should enter the student registration/roll call number. Once you type the number and click the search button, the student's basic details and the attendance details saved previously will be displayed. 
  
  The teacher can update the details, add the new attendance, and click save. Once saved, the data is updated, the page is refreshed, and a flash message is shown saying that the data was saved successfully.
  **Note:** Only the students within the class the teacher assigned can be searched. If the registration number of the student from another class is known, it cannot be found. A class restriction is given.
  
  On clicking Logout, the class teacher or student will be logged out. As session-based login is created, when logged out, the sessions are cleared, and the user cannot go back to the previous page using the back arrow button or history of the browser.

------------------------------------------------------------------------------------------------------------------------------------

In Project code folder  the  **" ProjectDB.sqlite3 "** has the tables with values in it.

------------------------------------------------------------------------------------------------------------------------------------

***** IF YOU FIND ANY PROBLEMS RELATED THIS PROGRAM, FEEL FREE TO CONTACT ME *****

***** LEAVE A COMMENT IF YOU LOVED MY WORK *****

THANK YOU FOR DOWNLOADING :)

                                                                               BY K.SUBASH GUPTA
