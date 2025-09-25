# app.py
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "onlineshop"

@app.route("/", methods=["GET", "POST"])
def index():
	username = session.get('username')
	return render_template("index.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")
		
		if username and password:
			session['username'] = username
			print(f"ログイン成功: {username}")
			return redirect(url_for("index"))
		else:
			print("ログイン失敗: ユーザー名またはパスワードが空です")
	
	return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
	if request.method == "POST":
		session.pop('username', None)
		return redirect(url_for("index"))
	return render_template("logout.html")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8080, debug=True)