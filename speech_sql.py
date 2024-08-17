# Importing necessary Python modules
import os
import time
import datetime
import pyttsx3
import speech_recognition as sr
import mysql.connector as sql
import pandas as pd

# init function to get an engine instance for speech synthesis
engine = pyttsx3.init('sapi5')             
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# greet function to greet user as per time of day
def greet():
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
            speak("Good Morning !")

    elif hour>= 12 and hour<18:
            speak("Good Afternoon !")

    else:
            speak("Good Evening !")

# Function to take commands from the user as speech and recognize using Google API
def takeCommand():
	
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, timeout=8,phrase_time_limit = 5)  
    try:
        print("Recognizing...")
        command = r.recognize_google(audio).lower()
        print("you said: " + command)
        
    except sr.UnknownValueError:
        print("Sorry, some exception error, Please say again")
        speak("Sorry, some exception error, Please say again")
        command = takeCommand()
    return command

# Check connection with DBMS (here MySQL)
def connection(status):
    if status:
        resp=("Connection with MySQL estabilished .\n You are ready to go forward! \n")
        print(resp)
        speak(resp)
    else:
        print("There is a problem with Data Server, I am unable to reach it.")
        speak("There is a problem with Data Server, I am unable to reach it.")        
        exit(0)

# Function for MySQL-Python connection
def db_connect():
    try:
        db_connection = sql.connect(host='localhost', user='root', password='Harry@24')
        # print(db_connection)
        if db_connection:
            connection(True)
            return(db_connection)
        else:
            resp="Oh! sorry, something went wrong while estabilshing the connection with database. Please try agin"
            print(resp)
            speak(resp)
            exit(0)    
    except:
        connection(False)
        exit(0)

# A combined function for all the covered queries that can be handled via speech
def query_engine(query):
    
    def show_dbs():
        db_cursor = sce.cursor()    
        db_cursor.execute('show databases')
        table_rows = db_cursor.fetchall()
        df = pd.DataFrame(table_rows)
        speak("Here is the list of Databases available in your store. ")
        print(df)
        return df.values.tolist()
    
    def db_select():
        rows=show_dbs()
        l=[]
        for i in range(len(rows)):
            l.append(rows[i][0])
        print("You can select any one of the given databases")
        speak("You can select any one of the given databases")
        return l
    
    def db_selected():
        rows=db_select()
        flag=0
        db=""
        for i in range(5):
            dbname=takeCommand()
            if any(s in dbname for s in  rows) :
                for s in rows:
                    if(s in dbname):
                        db=s
                print("Yes ,", db, " Database is in given list !")
                speak("Yes ,"+ db + " Database is in given list !")
                flag=1
                break
            else:
                print(" Nothing matched in given databases list")
                speak(" Nothing matched in given databases list")
        if(flag==0):
            speak("Sorry. Exceeded number of tries. Please try restarting the program")
            exit(0)
        db_cursor = sce.cursor() 
        db_cursor.execute('use '+db) 
        recorded.append('select database')       
        return sce, db
    
    def show_tables():
        if 'select database' not in recorded:
            speak("Please select a database first")
            conn,dbname=db_selected()
        else:
            conn=sce
            dbname=dtbname
        if conn is not False:     
            db_cursor = conn.cursor()    
            db_cursor.execute('show tables')
            table_rows1 = db_cursor.fetchall()
            df1 = pd.DataFrame(table_rows1)
            speak("Here is the list of Tables available in "+ dbname+ " Database.")
            print(df1)
            speak("If you can't find your desired table try changing the data base")
            speak("Current database is "+dbname)
            return df1.values.tolist(),conn
        else:
            exit(0) 

    def select_data():

        # Getting table name and its list of columns for further development of query
        table,conn=show_tables()
        tables=[]
        for i in range(len(table)):
            tables.append(table[i][0])
        print("tables",tables)
        flag=0
        tb=""
        for i in range(5):
            tbname=takeCommand()
            if any(t in tbname for t in  tables) :
                for t in tables:
                    if(t in tbname):
                        tb=t
                print("Okay! ", tb, " table is in given list")
                speak("OKay! "+tb+" Table is in given list")
                flag=1
                break
            else:
                print("Nothing matched in given Tables list")
                speak("Nothing matched in given Tables list")
        if(flag==0):
            speak("Sorry. Exceeded number of tries. Please try restarting the program")
            exit(0)
        db_cursor = conn.cursor() 
        qry= 'desc '+tb
        db_cursor.execute(qry)
        table_rows1 = db_cursor.fetchall()
        df1=pd.DataFrame(table_rows1)
        columns=df1[df1.columns[0]].values.tolist()
        print(columns)

        # Selecting all, none or particular set of  existing columns for display
        speak("Please say 'all' to show all columns or else say 'specifying'")
        print("Please specify the columns from their number (0-indexed) to display or say all")
        s_col=[]
        col=takeCommand()
        if('all' in col):
            s='*  '
        elif('none' in col):
            s="  "
        else: 
            l=[]
            try:
                print("Enter column numbers and write any string if you wish to stop input")
                while True:
                    l.append(int(input()))
            except:
                print(l)
            s=""
            for i in l:
                if(i<len(columns)):
                    s+=columns[i]
                    s_col.append(columns[i])
                    s+=", "
                else:
                    speak("Invalid input found, not including it ")

        # Selection of Aggregate functions
        a=['maximum','minimum','average','total']
        speak("Specify aggregate function if you wish to")
        b=takeCommand()
        flag=0
        func=""
        for i in a:
            if i in b:
                func=i
                flag=1
        if flag==0:
            speak("No aggregate function chosen")
        else:
            if(func =='average'):
                func="avg"
            elif(func =='total'):
                func="sum"
            else:
                func=func[:3]    #max/min
            speak("Specify column for aggregate function")
            a_col=takeCommand()
            for a in columns:
                if(a in a_col):
                    func=func+"("+a+")"
                    s_col.append(b)
                    s=s+func
                    break

        # Where condition to be specified by user because of the complexity of this clause
        speak("Do you have a where condition")
        r=takeCommand()
        if('yes' in r):
            speak("Please specify conditions")
            w=input("Condition(s): ")
            qry= 'select '+s+' from '+tb+' where '+w
        else:
            qry= 'select '+s+' from '+tb

        # Group By condition
        speak("Do you have an group by condition")
        r=takeCommand()
        if('yes' in r):
            speak("Try to be syntactically sure while using group by")
            speak("Please specify column for group by condition")
            c=takeCommand()
            for x in columns:
                if x in c:
                    qry=qry+" group by "+x
                    break

        # Order By condition
        speak("Do you have an order by condition")
        r=takeCommand()
        if('yes' in r): #
            speak("Please specify column")
            c=takeCommand()
            for x in columns:
                if x in c:
                    speak("Please specify ascending or descending")
                    o=takeCommand()
                    if('ascending' in o):
                        qry=qry+" order by "+x+" asc ;"
                    elif('descending' in o):
                        qry=qry+" order by "+x+" desc ;"
                break

        # Final query execution
        print(qry)
        speak("Executing "+qry)
        try:
            db_cursor.execute(qry)
            table_rows2 = db_cursor.fetchall()
            df2 = pd.DataFrame(table_rows2,columns=db_cursor.column_names)
            speak("Here is the Data of the "+ tb+" Table available in your database.")
            print(df2)
        except Exception as e:
            speak("Exception ocuured. Please try again from start ")
            exit(0)

    def update_table():

        # Getting the table name and its columns
        table,conn=show_tables()
        tables=[]
        for i in range(len(table)):
            tables.append(table[i][0])
        print("tables",tables)
        flag=0
        tb=""
        for i in range(5):
            tbname=takeCommand()
            if any(t in tbname for t in  tables) :
                for t in tables:
                    if(t in tbname):
                        tb=t
                print("Okay! ", tb, " table is in given list")
                speak("OKay! "+tb+" Table is in given list")
                flag=1
                break
            else:
                print("Nothing matched in given Tables list")
                speak("Nothing matched in given Tables list")
        if(flag==0):
            speak("Sorry. Exceeded number of tries. Please try restarting the program")
            exit(0)
        db_cursor = conn.cursor() 
        qry= 'desc '+tb
        db_cursor.execute(qry)
        table_rows1 = db_cursor.fetchall()
        df1=pd.DataFrame(table_rows1)
        columns=df1[df1.columns[0]].values.tolist()
        print(columns)

        # Due to complexity of the set and where conditions they taken as text input from the user
        speak("Please input set values and conditions")
        setval=input("Enter set value : ")
        w=input("Enter where condition : ")
        # Update query formation and execution 
        qry="update "+tb+" set "+setval+" where "+w
        db_cursor.execute(qry)
        speak(tb+" updated")
        db_cursor.execute("select * from "+tb)
        table_rows = db_cursor.fetchall()
        df = pd.DataFrame(table_rows,columns=db_cursor.column_names)
        speak("Updated "+ tb+" is as follows")
        print(df)

    def delete_row():

        # Getting the table name and its columns
        table,conn=show_tables()
        tables=[]
        for i in range(len(table)):
            tables.append(table[i][0])
        print("tables",tables)
        flag=0
        tb=""
        for i in range(5):
            tbname=takeCommand()
            if any(t in tbname for t in  tables) :
                for t in tables:
                    if(t in tbname):
                        tb=t
                print("Okay! ", tb, " table is in given list")
                speak("OKay! "+tb+" Table is in given list")
                flag=1
                break
            else:
                print("Nothing matched in given Tables list")
                speak("Nothing matched in given Tables list")
        if(flag==0):
            speak("Sorry. Exceeded number of tries. Please try restarting the program")
            exit(0)
        db_cursor = conn.cursor() 

        # Due to complexity of the where conditions it is taken as text input from the user
        speak("Please input conditions")
        w=input("Enter where condition : ")
        qry="delete  from "+tb+" where "+w
        db_cursor.execute(qry)
        speak("Deleted operation carried out successfully")
        db_cursor.execute("select * from "+tb)
        table_rows = db_cursor.fetchall()
        df = pd.DataFrame(table_rows,columns=db_cursor.column_names)
        speak("Updated "+ tb+" is as follows")
        print(df)

    # if else conditions to call necessary functions
    if 'show data bases' in query:
        show_dbs()
    if 'select database' in query:
        db_selected()
    if  "show tables" in query:
        show_tables()
    if 'show table data' in query:
        select_data()
    if 'update table' in query:
        update_table()
    if 'delete rows' in query:
        delete_row()
    if 'speak query' in query:
        qry=takeCommand()
        try:
            db_cursor = sce.cursor()    
            db_cursor.execute(qry)
            table_rows = db_cursor.fetchall()
            df = pd.DataFrame(table_rows)
            speak("Here is the output of your query : ")
            print(df)
        except Exception as e:
            speak("Some error with spoken query")
            speak(e)
    if 'write query' in query:
        qry=input("Enter query: ")
        try:
            db_cursor = sce.cursor()    
            db_cursor.execute(qry)
            table_rows = db_cursor.fetchall()
            df = pd.DataFrame(table_rows)
            speak("Here is the output of your query : ")
            print(df)
        except Exception as e:
            speak("Some error with written query")

    return query 


# Getting transcribed text from speech 
def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from microphone.
    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was successful
    "error": `None` if no error occured, otherwise a string containing an error message if the API could not be reached or speech was unrecognizable
    "transcription": `None` if speech could not be transcribed, otherwise a string containing the transcribed text
    """
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source,timeout=8,phrase_time_limit = 5)
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

# Some basic printed text
instructions = ("I am your Database Interaction Voice Assistant:\n")
commands=(
    " --- Show Databases \n"
    " --- Select Database \n"
    " --- Show Tables \n"
    " --- Show Table Data \n"
    " --- Update Table \n"
    " --- Delete Table \n"
    " --- Write Query \n"
#   " --- Speak Query (Only Suitable for easy to speak queries to ensure corresct formation of query)"
    " --- Say abort or end or terminate to exit \n"
    )
print(instructions)
print(commands)
greet()
speak(instructions)
sce=db_connect()
speak("You can carry out the given instructions")
time.sleep(1)
dtbname=""

# Beginning of the actual program
if __name__ == "__main__": 
    clear = lambda: os.system('cls')
    # This Function will clean any command before execution of this python file
    clear()          
    recorded=['connect to database']
    queries=[ 'show data bases', "select database", "show tables", "show table data", 
             "update table","delete rows","speak query","write query"]
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Carry out one of the listed queries until user quits or commits an error
    while True:
        while True: # Indefinite loop until user's speech is recognized
            speak("Please Speak. I'm Listening ....")
            print("Speak. I'm Listening .... ")
            guess = recognize_speech_from_mic(recognizer, microphone)
            # print(guess)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            speak("Sorry. I didn't catch that. What did you say?")
            print("I didn't catch that. What did you say?\n")

        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break
        print("You said: {}".format(guess["transcription"]))
        if guess["transcription"] is not None:
            guess_is_correct = any(s in guess["transcription"].lower() for s in queries)
            if any(s in guess["transcription"].lower() for s in ('abort', 'end', 'terminate')):
                speak( " Thanks for Using. Have a Good day !")
                print( " Thanks for Using. Have a Good day !")
                break
        if guess_is_correct:
            txt=query_engine(guess["transcription"].lower())
            op=" Task Achieved successfuly !"
            print(op)
            speak(op)
        else:
            print("Sorry, I can't perform what you have said . Please try again! ")
            speak("Sorry, I can't perform what you have said . Please try again!")

# joins, trigger, sequence, view, index are a few topics that require larger and sometimes nested lines of query
# Hence, they are not implemented yet 