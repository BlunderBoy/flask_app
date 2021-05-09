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

def isValid(value):
	return value != ""

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		
		# afisare
		if "Afisare studenti" in request.form:
			return redirect("/studenti")

		if "Afisare clase" in request.form:
			return redirect("/clase")

		if "Afisare profesori" in request.form:
			return redirect("/profesori")

		# adaugari
		if "Adauga studenti" in request.form:
			return redirect("/aduga_student_manual")

		if "Adauga clase" in request.form:
			return redirect("/adauga_clasa_manual")

		if "Adauga profesori" in request.form:
			return redirect("/adaugare_profesor_manual")

	return render_template("index.html")

@app.route("/studenti")
def studenti():
	cursor = get_cursor()
	
	rezultate = cursor.execute("select * from studenti")

	if rezultate > 0:
		studenti = cursor.fetchall()
		return render_template("studenti.html", studenti=studenti)
	else:
		return "Nu sunt studenti in baza de date"

@app.route("/aduga_student_manual", methods=["GET", "POST"])
def adauga_student_manual():
	if request.method == "GET":
		return render_template("adauga_student_manual.html")
	
	if request.method == "POST":
		id_student = request.form["id"]
		id_clasa = request.form["id_clasa"]
		nume = request.form["nume"].capitalize()
		prenume = request.form["prenume"].capitalize()
		email = request.form["email"]
		nr_telefon = request.form["nr_telefon"]
		anul_inrolarii = request.form["anul_inrolarii"]
		data_nasterii = request.form["data_nasterii"]
		medie = request.form["medie"]

		if not isValid(id_student) \
		or not isValid(id_clasa)\
		or not isValid(nume)\
		or not isValid(prenume)\
		or not isValid(email)\
		or not isValid(nr_telefon)\
		or not isValid(anul_inrolarii)\
		or not isValid(medie):
			return "Wrong data format"
 
		cursor = get_cursor()

		cursor.execute(
			"insert into studenti(id, nume, prenume, id_clasa, email, nr_telefon, anul_inrolarii, data_nasterii, medie) \
				 values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \
					str_to_date(\'{}\', \'%d/%m/%y\'),\
					str_to_date(\'{}\', \'%d/%m/%y\'), \'{}\');"
				 .format(id_student, nume, prenume, id_clasa, email, nr_telefon, anul_inrolarii, data_nasterii, medie)
		)

		mysql.connection.commit()
		cursor.close()

		return redirect("/studenti")

@app.route("/profesori")
def profesori():
	cursor = get_cursor()
	
	rezultate = cursor.execute("select * from profesori")

	if rezultate > 0:
		profesori = cursor.fetchall()
		return render_template("profesori.html", profesori=profesori)
	else:
		return "Nu sunt profi in baza de date"

@app.route("/adaugare_profesor_manual", methods=["GET", "POST"])
def adaugare_manuala_profesori():

	if request.method == "GET":
		return render_template("adauga_profesor_manual.html")
	
	if request.method == "POST":
		id_profesor = request.form["id"]
		materie = request.form["materie"]
		nume = request.form["nume"].capitalize()
		prenume = request.form["prenume"].capitalize()
		salariu = request.form["salariu"]
		anul_inrolarii = request.form["an_inrolare"]
		grad = request.form["grad"]

		if not isValid(id_profesor) \
		or not isValid(materie)\
		or not isValid(nume)\
		or not isValid(prenume)\
		or not isValid(anul_inrolarii)\
		or not isValid(salariu)\
		or not isValid(grad):
			return "Wrong data format"
 
		cursor = get_cursor()

		cursor.execute(
			"insert into profesori(id_profesor, materie, nume, prenume, salariu, anul_inrolarii, grad) \
				 values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\',\
					str_to_date(\'{}\', \'%d/%m/%y\'), \'{}\');"
				 .format(id_profesor, materie, nume, prenume, salariu, anul_inrolarii, grad)
		)

		mysql.connection.commit()
		cursor.close()

		return redirect("/profesori")

@app.route("/clase")
def clase():
	cursor = get_cursor()
	
	rezultate = cursor.execute("select * from clase")

	if rezultate > 0:
		clase = cursor.fetchall()
		return render_template("clase.html", clase=clase)
	else:
		return "Nu sunt clase in baza de date"

@app.route("/adauga_clasa_manual", methods=["GET", "POST"])
def adaugare_manuala_clasa():
	if request.method == "GET":
		return render_template("adauga_clasa_manual.html")
	
	if request.method == "POST":
		id_clasa = request.form["id"]
		nume = request.form["nume"]
		id_diriginte = request.form["id_diriginte"]
		profil = request.form["profil"]

		if not isValid(id_clasa) \
		or not isValid(id_diriginte)\
		or not isValid(nume)\
		or not isValid(profil):
			return "Wrong data format"
 
		cursor = get_cursor()

		cursor.execute(
			"insert into clase(id_clasa, nume, id_diriginte, profil) values (\'{}\', \'{}\', \'{}\', \'{}\');"
				 .format(id_clasa, nume, id_diriginte, profil)
		)

		mysql.connection.commit()
		cursor.close()

		return redirect("/clase")

if __name__ == "__main__":
	app.run(debug=True)