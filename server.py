from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_mysqldb import MySQL
from random import choice, randrange, random
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
		
		#######
		if "Studenti cu bursa" in request.form:
			return redirect("/studenti_bursa")

		if "Studenti corigenti" in request.form:
			return redirect("/studenti_corigenti")

		if "Clasa dirigentelui" in request.form:
			return redirect("/clasa_dirigintelui")
		
		if "Sortare profesori grad" in request.form:
			return redirect("/sortare_profesori_grad")

		if "Media clasei" in request.form:
			return redirect("/media_clasei")

		if "Numar elevi" in request.form:
			return redirect("/numar_elevi")

	return render_template("index.html")
			
@app.route("/studenti_bursa")
def studenti_bursa():
	cursor = get_cursor()
	
	rezultate = cursor.execute("select nume, prenume, id_clasa, medie from studenti \
		where medie >= 8.5 order by medie desc")

	if rezultate > 0:
		studenti = cursor.fetchall()
		return render_template("studenti_bursa.html", studenti=studenti)
	else:
		return "Nu sunt studenti in baza de date"
			
@app.route("/studenti_corigenti")
def studenti_corigenti():
	cursor = get_cursor()
	
	rezultate = cursor.execute("select nume, prenume, id_clasa, medie from studenti \
		where medie < 5 order by medie desc")

	if rezultate > 0:
		studenti = cursor.fetchall()
		return render_template("studenti_corigenti.html", studenti=studenti)
	else:
		return "Nu sunt studenti in baza de date"
			
@app.route("/clasa_dirigintelui")
def clasa_dirigintelui():
	cursor = get_cursor()
	
	rezultate = cursor.execute(""" 
		select p.prenume, p.nume, p.materie, c.nume 
		from profesori p
			inner join clase c
				on p.id_profesor = c.id_diriginte;
	""")

	if rezultate > 0:
		profesori = cursor.fetchall()
		return render_template("clasa_dirigintelui.html", profesori=profesori)
	else:
		return "Nu sunt profi in baza de date"
					
@app.route("/sortare_profesori_grad")
def sortare_profesori_grad():
	cursor = get_cursor()
	
	rezultate = cursor.execute(""" 
		select prenume, nume, grad
		from profesori
		order by grad asc;
	""")

	if rezultate > 0:
		profesori = cursor.fetchall()
		return render_template("sortare_profesori_grad.html", profesori=profesori)
	else:
		return "Nu sunt profi in baza de date"
			
@app.route("/media_clasei")
def media_clasei():
	cursor = get_cursor()
	
	rezultate = cursor.execute("""
		select c.nume,
			(select round(avg(medie), 2) 
			from studenti s 
			where s.id_clasa = c.id_clasa)
		from clase c
		order by 2 desc;
	""")

	if rezultate > 0:
		clase = cursor.fetchall()
		return render_template("media_clasei.html", clase=clase)
	else:
		return "Nu sunt clase in baza de date"
			
@app.route("/numar_elevi")
def numar_elevi():
	cursor = get_cursor()
	
	rezultate = cursor.execute("""
		select c.nume,
		(
			select count(s.id_clasa) from studenti s
			where s.id_clasa = c.id_clasa
		)
		from clase c
		order by 2 desc
	""")

	if rezultate > 0:
		clase = cursor.fetchall()
		return render_template("numar_elevi.html", clase=clase)
	else:
		return "Nu sunt clase in baza de date"

def get_random_date():
	day = choice(["0","1","2"]) + choice([str(i) for i in range(1,9)])

	month = choice(["0","1"])
	if month == "0":
		month += choice([str(i) for i in range(1,9)])
	else:
		month += choice(["1","2"])

	year = "0"+choice([str(i) for i in range(5)])

	return day+"/"+month+"/"+year

def get_random_date_enroll():
	day = choice(["0","1","2"]) + choice([str(i) for i in range(1,9)])

	month = choice(["0","1"])
	if month == "0":
		month += choice([str(i) for i in range(1,9)])
	else:
		month += choice(["1","2"])

	year = choice([str(i) for i in range(18, 21)])

	return day+"/"+month+"/"+year

@app.route("/populate_students")
def populate_students():
	cursor = get_cursor()

	names = ["Alex", "Marius", "Cristi", "Irina", "Maria", "Alex", "Alexandra",
	"Lucian", "Silviu", "Razvan", "Adrian", "Luiza", "Andrei", "Diana", "Cosmin", "Mihaela",
	"Stefan", "Bogdan"]

	fam_names = ["Popescu",
	"Ionescu",
	"Popa",
	"Pop",
	"Niță",
	"Nițu",
	"Constantinescu",
	"Stan",
	"Stanciu",
	"Dumitrescu",
	"Dima",
	"Gheorghiu",
	"Ioniță",
	"Marin",
	"Tudor",
	"Dobre",
	"Barbu",
	"Nistor",
	"Florea",
	"Frățilă",
	"Dinu",
	"Dinescu",
	"Georgescu",
	"Stoica",
	"Diaconu",
	"Diaconescu",
	"Mocanu",
	"Voinea",
	"Albu",
	"Petrescu",
	"Manole",
	"Cristea",
	"Toma",
	"Stănescu",
	"Pușcașu",
	"Tomescu",
	"Sava",
	"Ciobanu",
	"Rusu",
	"Ursu",
	"Lupu",
	"Munteanu",
	"Moldoveanu",
	"Mureșan",
	"Andreescu",
	"Sava",
	"Mihăilescu",
	"Iancu",
	"Teodorescu",
	"Moisescu",
	"Călinescu",
	"Tabacu",
	"Negoiță",
	"Ifrim"]

	for i in range(4, 100):
		random_nume = choice(names)
		random_familie = choice(fam_names)
		rand_telephone = "07"+"".join([str(choice([0,1,2,3,4,5,6,7,8,9])) for _ in range(8)])
		cursor.execute(
			"insert into studenti(id, nume, prenume, id_clasa, email, nr_telefon, anul_inrolarii, data_nasterii, medie) \
				 values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \
					str_to_date(\'{}\', \'%d/%m/%y\'),\
					str_to_date(\'{}\', \'%d/%m/%y\'), \'{}\');"
				 .format(i, random_nume, random_familie, randrange(1, 6), 
				  random_nume+random_familie+str(choice([0,1,2,3,4,5,6,7,8,9]))+choice(["@yahoo.com","@gmail.com"]),
				  rand_telephone, 
				  get_random_date(), 
				  get_random_date_enroll(), 
				  round(random()*10, 1))
		)
	mysql.connection.commit()
	cursor.close()
	return redirect("/studenti")

@app.route("/populate_profesori")
def populate_profesori():
	cursor = get_cursor()
	materii = ["romana", "engleza", "franceza", "mate", "fizica", "chimie", "biologie", "cultura civica", "istorie", "religie", "geografie", "desen", "muzica", "sport", "educatie tehnologica"]
	names = ["Alex", "Marius", "Cristi", "Irina", "Maria", "Alex", "Alexandra",
	"Lucian", "Silviu", "Razvan", "Adrian", "Luiza", "Andrei", "Diana", "Cosmin", "Mihaela",
	"Stefan", "Bogdan"]

	fam_names = ["Popescu",
	"Ionescu",
	"Popa",
	"Pop",
	"Niță",
	"Nițu",
	"Constantinescu",
	"Stan",
	"Stanciu",
	"Dumitrescu",
	"Dima",
	"Gheorghiu",
	"Ioniță",
	"Marin",
	"Tudor",
	"Dobre",
	"Barbu",
	"Nistor",
	"Florea",
	"Frățilă",
	"Dinu",
	"Dinescu",
	"Georgescu",
	"Stoica",
	"Diaconu",
	"Diaconescu",
	"Mocanu",
	"Voinea",
	"Albu",
	"Petrescu",
	"Manole",
	"Cristea",
	"Toma",
	"Stănescu",
	"Pușcașu",
	"Tomescu",
	"Sava",
	"Ciobanu",
	"Rusu",
	"Ursu",
	"Lupu",
	"Munteanu",
	"Moldoveanu",
	"Mureșan",
	"Andreescu",
	"Sava",
	"Mihăilescu",
	"Iancu",
	"Teodorescu",
	"Moisescu",
	"Călinescu",
	"Tabacu",
	"Negoiță",
	"Ifrim"]
	for i in range(1, 20):
		cursor.execute(
		"insert into profesori(id_profesor, materie, nume, prenume, salariu, anul_inrolarii, grad) \
			 values (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\',\
				str_to_date(\'{}\', \'%d/%m/%y\'), \'{}\');"
			 .format(i, choice(materii).capitalize(), 
			 choice(names), 
			 choice(fam_names),
			 randrange(4000, 9000, 1000), 
			 get_random_date_enroll(), 
			 randrange(1,3))
	)

	mysql.connection.commit()
	cursor.close()

	return redirect("/profesori")

@app.route("/populate_clase")
def populate_clase():
	cursor = get_cursor()

	cursor.execute(
		"insert into clase(id_clasa, nume, id_diriginte, profil) values (\'{}\', \'{}\', \'{}\', \'{}\');"
			 .format(1, "MI1", randrange(1, 19), "Real")
	)

	cursor.execute(
		"insert into clase(id_clasa, nume, id_diriginte, profil) values (\'{}\', \'{}\', \'{}\', \'{}\');"
			 .format(2, "MI2", randrange(1, 19), "Real")
	)

	cursor.execute(
		"insert into clase(id_clasa, nume, id_diriginte, profil) values (\'{}\', \'{}\', \'{}\', \'{}\');"
			 .format(3, "SN1", randrange(1, 19), "Real")
	)

	cursor.execute(
		"insert into clase(id_clasa, nume, id_diriginte, profil) values (\'{}\', \'{}\', \'{}\', \'{}\');"
			 .format(4, "SN2", randrange(1, 19), "Real")
	)

	cursor.execute(
		"insert into clase(id_clasa, nume, id_diriginte, profil) values (\'{}\', \'{}\', \'{}\', \'{}\');"
			 .format(5, "SN3", randrange(1, 19), "Real")
	)

	mysql.connection.commit()
	cursor.close()
	return redirect("/clase")

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