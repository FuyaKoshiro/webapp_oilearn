from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/")
def display_home():
    return "home.html"

@app.route("/signup/")
def display_signup():
    return "signup.html"

@app.route("/login/")
def display_login():
    return "login.html"

@app.route("/content/<video_id>")
def display_content(video_id):
    return f"content/video_id.html, video_id: {video_id}"

@app.route("/mypage/<user_Id>")
def display_mypage(user_id):
    return f"mypage/user_Id.html, user_id: {user_id}"

@app.route("/login/request")
def display_login_request():
    return "login/request.html"


if __name__ == '__main__':
    app.run()