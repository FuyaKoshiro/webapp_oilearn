from flask import Flask, request, session
from flask import render_template, redirect, url_for, make_response
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

import sqlite3
import os


app = Flask(__name__)
app.secret_key = 'secret_key'

login_manager = LoginManager()
login_manager.init_app(app)

#define the user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_username(self):
        conn = sqlite3.connect('common/models/database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user_name FROM users WHERE user_id = '{}'".format(self.id))
        username = cursor.fetchone()[0]
        conn.close()
        return username


@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on the user ID
    user = User(user_id)
    return user
    

@app.route("/")
def index():
    conn = sqlite3.connect('common/models/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos")
    video_objects = cursor.fetchall()
    conn.close()

    video_codes = [item[0] for item in video_objects] 
    channel_urls = [item[1] for item in video_objects]   
    video_titles = [item[3] for item in video_objects]
    video_thumbnail_urls = [item[4] for item in video_objects]

    channel_url_key = channel_urls[0]
    video_codes_to_add = []
    video_titles_to_add = []
    video_thumbnail_urls_to_add = []
    video_data_dict = {}
    video_data_dict_keys = []

    for i in range(len(video_codes)):
        if channel_url_key == channel_urls[i] and i < len(video_codes)-1:
            video_codes_to_add.append(video_codes[i])
            video_titles_to_add.append(video_titles[i])
            video_thumbnail_urls_to_add.append(video_thumbnail_urls[i])

        elif channel_url_key == channel_urls[i] and i == len(video_codes)-1:
            video_codes_to_add.append(video_codes[i])
            video_titles_to_add.append(video_titles[i])
            video_thumbnail_urls_to_add.append(video_thumbnail_urls[i])
            video_data_dict[channel_url_key] = [video_codes_to_add, video_titles_to_add, video_thumbnail_urls_to_add]
            video_data_dict_keys.append(channel_url_key)

        else:
            video_data_dict[channel_url_key] = [video_codes_to_add, video_titles_to_add, video_thumbnail_urls_to_add]
            video_data_dict_keys.append(channel_url_key)
            channel_url_key = channel_urls[i]
            video_codes_to_add = []
            video_titles_to_add = []
            video_thumbnail_urls_to_add = []
            video_codes_to_add.append(video_codes[i])
            video_titles_to_add.append(video_titles[i])
            video_thumbnail_urls_to_add.append(video_thumbnail_urls[i])

    length = len(video_data_dict_keys)

    print(video_data_dict)

    #change the items in home.html corresponding to users' login status
    user_is_logged_in = current_user.is_authenticated

    return render_template(
        "home.html",
        video_data_dict = video_data_dict,
        video_data_dict_keys=video_data_dict_keys,
        video_codes = video_codes,
        video_titles = video_titles,  
        video_thumbnail_urls = video_thumbnail_urls,
        user_is_logged_in = user_is_logged_in,
        length=length
        )
    

# Define the login route and view function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verify login credentials and load user from database
        user = None

        #Check if users' input matches to the one from a database
        email_input = request.form.get("email")
        password_input = request.form.get("password")

        conn = sqlite3.connect('common/models/database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, user_name, user_password FROM users WHERE user_email = '{}'".format(email_input))
        response = cursor.fetchone()
        user_id_db = response[0]
        user_name_db = response[1]
        password_db = response[2]

        if password_db == password_input:
            print("succeed to log-in")
            user = User(id=user_id_db)
            login_user(user=user)
            return redirect(url_for("index"))
        
        else:
            print("failed to log-in")
            return redirect(url_for("login"))

    # Render the login template
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract user data from form and create new user object
        name_input = request.form['username']
        email_input = request.form['email']
        password_input = request.form['password']
        confirm_password = request.form['confirm_password']

        if password_input != confirm_password:
            # Passwords don't match, show error message
            error = 'Passwords do not match.'
            return render_template('signup.html', error=error, )

        # Insert the new user data into the database
        conn = sqlite3.connect('common/models/database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (user_name, user_email, user_password) VALUES ("{}", "{}", "{}")'.format(name_input, email_input, password_input))
        conn.commit()
        conn.close()

        # Log the user in and redirect to the home page
        # Replace with your own user loading logic to get the user object from the database
        user = None 
        
        conn = sqlite3.connect('common/models/database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, user_name FROM users WHERE user_email = '{}'".format(email_input))
        user_id = cursor.fetchone()[0]

        user = User(user_id)
        login_user(user)
        return redirect(url_for("index", user=user))

    # Render the signup template
    return render_template('signup.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/content/<video_code>/", methods=["GET", "POST"])
def content(video_code):

    user_is_logged_in = current_user.is_authenticated

    if user_is_logged_in:
        user_id = current_user.id
        user_id = int(user_id)
        user_id = "test_user_id_{:02d}".format(user_id)
    else:
        user_id = None

    if request.method == "POST":
        print(request.form)
        print(type(request.form))

        #add an item into a database
        if "add" in request.form:
            phrase_id_to_add = request.form["add"]

            #get values to insert into a mypage
            conn = sqlite3.connect("common/models/database.db")
            cursor = conn.cursor()
            cursor.execute(""" 
                SELECT vv.phrase, vv.meaning, v.channel_url
                FROM video_{} vv 
                INNER JOIN videos v ON vv.video_code = v.video_code
                WHERE vv.phrase_id = "{}"
                """.format(video_code, phrase_id_to_add))
            response = cursor.fetchone()
            conn.close()
            phrase = response[0]
            meaning = response[1]
            video_channel_url = response[2]
            
            #Insert the phrase to mypage
            conn = sqlite3.connect("common/models/database.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mypage_{} (
                video_code, user_id, video_channel_url, phrase, meaning, phrase_id
                ) VALUES ("{}", "{}", "{}", "{}", "{}", "{}")
                """.format(user_id, video_code, user_id, video_channel_url, phrase, meaning, phrase_id_to_add))
            conn.commit()
            conn.close()
            return redirect(url_for("content", video_code=video_code))

        #remove a row from mypage corresponding to the phrase_id
        if "remove" in request.form:
            phrase_id_to_remove = request.form["remove"]

            conn = sqlite3.connect("common/models/database.db")
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM mypage_{}
                WHERE phrase_id = "{}"
                """.format(user_id, phrase_id_to_remove))
            conn.commit()
            conn.close()
            return redirect(url_for("content", video_code=video_code))

    #if there is not post request, display contents
    #firstly, get phrases_id from mypage to change the button from "add" to "remove" in "content.html"
    #if user is not logged in, phrase_id_from_mypage is "None"
    if user_is_logged_in:
        conn = sqlite3.connect('common/models/database.db')
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT phrase_id
                    FROM mypage_{}
                    WHERE video_code = "{}"
                    """.format(user_id, video_code))
        response = cursor.fetchall()
        conn.close()
        phrase_id_from_mypage = [item[0] for item in response]
    
    else:
        phrase_id_from_mypage = None
            
    #secondaly, get required values from database
    conn = sqlite3.connect('common/models/database.db')
    cursor = conn.cursor()
    cursor.execute("""
                SELECT v.channel_url, v.video_url, v.video_title, v.video_thumbnail_url, vv.phrase, vv.meaning, vv.phrase_id
                FROM videos v INNER JOIN video_{} vv
                ON v.video_code = vv.video_code
                """.format(video_code))
    response = cursor.fetchall()
    conn.close()

    channel_url = response[0][0]
    video_url = response[0][1]
    video_title = response[0][2]
    video_thumbnail_path = response[0][3]
    phrases = [response[i][4] for i in range(len(response))]
    meanings = [response[i][5] for i in range(len(response))]
    phrase_ids = [response[i][6] for i in range(len(response))]
    length = len(phrases)

    return render_template(
        "content.html",
        video_code=video_code,
        user_is_logged_in=user_is_logged_in,
        channel_url=channel_url,
        video_url=video_url,
        video_title=video_title,
        video_thumbnail_path=video_thumbnail_path,
        phrases=phrases,
        meanings=meanings,
        phrase_ids=phrase_ids,
        phrase_id_from_mypage=phrase_id_from_mypage,
        length=length)


@app.route("/mypage/", methods=["GET", "POST"])
@login_required
def mypage():

    user_is_logged_in = current_user.is_authenticated

    user_id = current_user.id
    user_id = int(user_id)
    user_id = "test_user_id_{:02d}".format(user_id)
    mypage = "mypage_" + user_id

    #if user send a "remove" post request, remove the phrase_id from the mypage database
    if request.method=="POST":
        phrase_id_to_remove = request.form["remove"]
        conn = sqlite3.connect("common/models/database.db")
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM {}
        WHERE phrase_id = "{}"
        """.format(mypage, phrase_id_to_remove))
        conn.commit()
        conn.close()
        return redirect(url_for("mypage"))

    #display contents from mypage (database)
    conn = sqlite3.connect("common/models/database.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT m.video_channel_url, m.phrase, m.meaning, m.phrase_id, v.video_url, v.video_title
    FROM {} m 
    INNER JOIN videos v ON m.video_code = v.video_code
    """.format(mypage))
    response = cursor.fetchall()
    conn.close()

    response_is_empty = True

    if len(response) != 0:
        response_is_empty = False
    
    print(f"response_is_empty: {response_is_empty}")
    
    print(response)
    channel_urls = [item[0] for item in response]
    phrases = [item[1] for item in response]
    meanings = [item[2] for item in response]
    phrase_ids = [item[3] for item in response]
    video_urls = [item[4] for item in response]
    video_titles = [item[5] for item in response]

    length = len(phrase_ids)

    return render_template("mypage.html",
                           response_is_empty=response_is_empty,
                            channel_urls=channel_urls,
                            phrases=phrases,
                            meanings=meanings,
                            phrase_ids=phrase_ids,
                            video_urls=video_urls,
                            video_titles=video_titles,
                            length=length,
                            user_is_logged_in=user_is_logged_in)


@app.route("/login_request", methods=["GET", "POST"])
def login_request():
    if request.method == 'POST':
        # Verify login credentials and load user from database
        user = None

        #Check if users' input matches to the one from a database
        email_input = request.form.get("email")
        password_input = request.form.get("password")

        conn = sqlite3.connect('common/models/database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, user_name, user_password FROM users WHERE user_email = '{}'".format(email_input))
        response = cursor.fetchone()
        user_id_db = response[0]
        user_name_db = response[1]
        password_db = response[2]

        if password_db == password_input:
            print("succeed to log-in")
            user = User(id=user_id_db)
            login_user(user=user)
            return redirect(url_for("index"))
        
        else:
            print("failed to log-in")
            return redirect(url_for("login"))
        
    return render_template("login_request.html")


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login_request'))


if __name__ == '__main__':
    app.debug = True
    PORT = os.environ.get('PORT','5000')
    app.run()