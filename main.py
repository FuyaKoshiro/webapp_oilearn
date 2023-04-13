from flask import Flask, request, session
from flask import render_template, redirect, url_for, make_response
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3

from controller.cookies import Cookies


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


#define the user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_username(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id = ?", (self.id,))
        username = cursor.fetchone()[0]
        conn.close()
        return username
    
@login_manager.user_loader
def load_user(user_id):
    # Load the user from the database based on the user ID
    user = User.query.get(int(user_id))
    return user
    
@app.route("/")
def index():
    conn = sqlite3.connect('common/models/database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM videos WHERE channel_url = 'test_channel_url'")
    video_objects = cursor.fetchall()
    conn.close()

    titles = []
    video_urls = []
    thumbnails = []
    video_codes = []

    for i in video_objects:
        titles.append(i[3])
        video_urls.append(i[2])
        thumbnails.append(i[4])
        video_codes.append(i[0])


    return render_template(
        "home.html",
        video_codes=video_codes,
        titles=titles, 
        video_urls=video_urls, 
        thumbnails=thumbnails,
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

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT user_id, user_email, user_password FROM users WHERE user_email = ?", (email_input,))
        response = cursor.fetchone()
        password_db = response[2]

        if password_db == password_input:
            print("succeed to log-in")

            user_id = response[0]
            user = User(id=user_id)
            login_user(user=user)
            return redirect("/login")
        
        else:
            print("failed to log-in")
            return redirect("/login")

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
            return render_template('signup.html', error=error)

        # Insert the new user data into the database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (user_name, user_email, user_password) VALUES (?, ?, ?)', (name_input, email_input, password_input))
        conn.commit()
        conn.close()

        # Log the user in and redirect to the home page
        # Replace with your own user loading logic to get the user object from the database
        user = None 
        login_user(user)
        return redirect("/")

    # Render the signup template
    return render_template('signup.html')


# @app.route("/logout/", methods=["GET", "POST"])
# def logout():

#     cookies = Cookies(cursor=cursor)
#     user_id = cookies.get_user_id()
#     user_name = cookies.get_user_name(user_id=user_id)

#     if request.method == "POST":
#         res = make_response(redirect("/"))
#         res.delete_cookie("user_name")
#         print("cookie is deleted")
#         return res

#     return render_template("logout.html", user_name=user_name)


@app.route("/content/<vcode>/")
def content(vcode):

    cookies = Cookies(cursor=cursor)
    user_id = cookies.get_user_id()
    user_name = cookies.get_user_name(user_id=user_id)

    cursor.execute("SELECT * FROM videos WHERE video_code = ?", (vcode,))
    video_objects = cursor.fetchall()

    phrases = []
    meanings = []

    url = video_objects[0][3]
    title = video_objects[0][2]

    for i in video_objects:
        phrases.append(i[5])
        meanings.append(i[6])

    print(url, title, phrases, meanings)

    return render_template(
        "content.html",
        url=url,
        title=title,
        phrases=phrases,
        meanings=meanings,
        user_name=user_name)


@app.route("/mypage/", methods=["GET", "POST"])
@login_required
def mypage():

    user_id = current_user.id
    print(f"user_id: {user_id}")

    if not user_id:
        return redirect("/login/request/")

    """
    If users submit remove button, fix the phrase_id array and update the database
    """

    if request.method=="POST":
        
        phrase_id_to_remove = request.form.get("phrase_id")

        print("phrase_id_to_remove: ", phrase_id_to_remove)
        cursor.execute("""
        DELETE FROM mypage WHERE phrase_id = ?
        """, (phrase_id_to_remove,))
        conn.commit()


    """
    Display contents based on users' record (phrase_id)
    1. Extract the data from videos
    2. Add them into the lists
    3. Extract the phrases and meanings based on users' phrase_id
    """

    user_mypage = str(user_id) + "_mypage"

    cursor.execute("""
    SELECT v.channel_url, v.video_url, v.video_title, v.video_thumbnail_path, v.phrases, v.meanings, m.phrase_id, m.datestamp
    FROM videos v INNER JOIN 
    """ + user_mypage + """
    m
    WHERE v.video_code = m.video_code    
    """)

    video_objects = cursor.fetchall()

    channel_urls = []
    video_urls = []
    video_titles = []
    video_thumbnail_paths = []
    phrases = []
    meanings = []
    phrase_ids = []
    date_stamps = []

    for video_object in video_objects:
        channel_urls.append(video_object[0])
        video_urls.append(video_object[1])
        video_titles.append(video_object[2])
        video_thumbnail_paths.append(video_object[3])
        phrases.append(video_object[4])
        meanings.append(video_object[5])
        phrase_ids.append(video_object[6])
        date_stamps.append(video_object[7])

    length = len(video_objects)

    phrases_to_display = []
    meanings_to_display = []

    for i in phrase_ids:
        phrases_to_display.append(phrases[i])
        meanings_to_display.append(meanings[i])

    # phrase_ids = []
    # dates = []
    # phrases = []
    # meanings = []
    # titles = []

    # cursor.execute("""
    # SELECT m.phrase_id, m.date, m.phrases, m.meaning, v.title
    # FROM videos v INNER JOIN mypage m 
    # WHERE v.video_code = m.video_code
    # """)
    # video_objects = cursor.fetchall()

    # for item in video_objects:

    #     phrase_ids.append(item[0])
    #     dates.append(item[1])
    #     phrases.append(item[2])
    #     meanings.append(item[3])
    #     titles.append(item[4])



    return render_template("mypage.html",
                            channel_urls=channel_urls,
                            video_urls=video_urls,
                            video_titles=video_titles,
                            video_thumbnail_paths=video_thumbnail_paths,
                            phrases_to_display=phrases_to_display,
                            meanings_to_display=meanings_to_display,
                            phrase_ids=phrase_ids,
                            date_stamps=date_stamps,
                            user_name=user_name,
                            lengh=length)



@app.route("/login/request/")
def login_request():
    return render_template("login_request.html")


if __name__ == '__main__':
    app.run()