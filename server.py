from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'flask_app'
mysql = MySQL(app)

def get_cursor():
	return mysql.connection.cursor()

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		userDetails = request.form
		name = userDetails["name"]
		email = userDetails["email"]
		
		cursor = get_cursor()


		cursor.execute("insert into users(name, email) values(\'{}\', \'{}\')".format(name, email))

		mysql.connection.commit()
		cursor.close()

		return redirect("/users")
	else:
		return render_template("index.html")

@app.route("/users")
def get_users():
	cursor = get_cursor()
	querryResult = cursor.execute("select * from users")

	if querryResult > 0:
			detalii = cursor.fetchall()
			return render_template("users.html", detalii=detalii)
	else:
		return "uhm???"


if __name__ == "__main__":
	app.run(debug=True)