import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, render_template, request, session, redirect
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("/index.html")


@app.route("/login")
def login():
    if db.execute("SELECT * FROM admins WHERE login=:login AND password=:password",
    {"login": session.get("login"), "password": session.get("password")}).rowcount > 0:
        return redirect("/admin", code=302)
    else:
        return render_template("/index.html", message="Авторизуйтесь", login="True")
@app.route("/login-error")
def login_error():
    return render_template("/index.html", message="Ошибка авторизации", login="True")


@app.route("/admin", methods=["POST", "GET"])
def admin():
    if session.get("login") is None:
        session["login"] = ""
        return redirect("/login", code=302)
    if request.method == "POST":
        session["login"] = request.form.get("login")
        session["password"] = request.form.get("password")

    if (db.execute("SELECT * FROM admins WHERE login=:login AND password=:password",
    {"login": session["login"], "password": session["password"]}).rowcount > 0):
        
        informatic__students = db.execute("SELECT * FROM students WHERE profession_id = (SELECT id FROM professions WHERE name = :name)",
                                    {"name": "Информатика"}).fetchall()
        robots__students = db.execute("SELECT * FROM students WHERE profession_id = (SELECT id FROM professions WHERE name = :name)",
                                    {"name": "Робототехника"}).fetchall()
        nano__students = db.execute("SELECT * FROM students WHERE profession_id = (SELECT id FROM professions WHERE name = :name)",
                                    {"name": "Нанотехнологии"}).fetchall()
        bio__students = db.execute("SELECT * FROM students WHERE profession_id = (SELECT id FROM professions WHERE name = :name)",
                                    {"name": "Биоинженерия"}).fetchall()
        physics__students = db.execute("SELECT * FROM students WHERE profession_id = (SELECT id FROM professions WHERE name = :name)",
                                    {"name": "Физика"}).fetchall()
        
        return render_template("/admin.html", informatic__students = informatic__students,
                                robots__students = robots__students,
                                nano__students = nano__students,
                                bio__students = bio__students,
                                physics__students = physics__students
                                )
    else:
        return redirect("/login-error", code=302)


@app.route("/admin-registration", methods=["POST", "GET"])
def adminRegistration():
    if request.method == "POST":
        if (db.execute("SELECT * FROM admins WHERE login=:login AND password=:password",
        {"login": session.get("login"), "password": session.get("password")}).rowcount > 0):
            Newlogin = request.form.get("login")
            Newpassword = request.form.get("password")
            Newmail = request.form.get("mail")
            try:
                db.execute("INSERT INTO admins (login, mail, password)\
                VALUES (:login, :mail, :password)",
                {"login": str(Newlogin), 
                "mail": str(Newmail),
                "password": str(Newpassword)
                }) 
                db.commit()
            except Exception:
                print("Ошибка при регистрации")
                return redirect("/admin-registration-fail", code=302)
            print(f"Добавлен пользователь с логином {Newlogin} и почтой {Newpassword}")
            return render_template("/admin.html", 
                message={
                    "header":"Пользователь зарегистрирован",
                    "submit":"Еще один",
                    "cancel":"Выход"}, regestration="True")       
    if request.method == "GET":
        return render_template("/admin.html", 
            message={
                "header":"Регистрация пользователя",
                "submit":"Подтвердить",
                "cancel":"Отмена"}, regestration="True")      
    else:
        return render_template("/index.html", message="Авторизуйтесь", login="True")


@app.route('/process-data', methods=['POST', 'GET'])
def doit():
    id = int(request.form['id'])
    if request.method == "POST":
        print("Удален студент")
        print(db.execute("SELECT * FROM students WHERE id=:id",
        {"id":id}).fetchall())
        db.execute("DELETE FROM students WHERE id=:id",
        {"id":id})
        db.commit()
        return redirect("/admin", code=302)
    else:
        return redirect("/admin", code=302)


@app.route("/admin-registration-fail", methods=["POST", "GET"])
def registration_fail():
    return render_template("/admin.html",
        message={
            "header":"Пользователь уже существует",
            "submit":"Еще попытка",
            "cancel":"Выход"}, regestration="True")


@app.route("/admin-logout", methods=["POST", "GET"])
def admin__logout():
    session["login"] = ""
    session["password"] = ""
    return redirect("/", code=302)


@app.route("/send-data", methods=["POST", "GET"])
def admin__send():
    if request.method=="POST":
        mail = request.form.get("mail")
        fio = request.form.get("fio")
        age = request.form.get("age")
        phone = request.form.get("phone")
        citizen = request.form.get("citizen")
        fromWhere = request.form.get("fromWhere")
        profession = request.form.get("profession")
        payment = request.form.get("payment")
        good = True
        if len(str(fio).split(" "))<2 or int(age)>30 or int(age)<16:
            good = False

        try:
            db.execute("INSERT INTO students (mail, fio, age, phone,\
                citizen, knowFrom, profession_id, payment, good) \
                VALUES (:mail, :fio, :age, :phone, :citizen, :knowFrom, :profession_id, :payment, :good)",
                {"mail": mail, "fio": fio, "age": age, "phone": phone, "citizen":citizen, 
                "knowFrom":fromWhere, "profession_id":profession, "payment":payment, "good":good}) 
            db.commit()
            return render_template("/index.html", data="sent", message="Ваша анкета принята!")
        except Exception:
            print("Ошибка при регистрации анкеты")
            return render_template("/index.html", data="sent", message="Ошибка при отправке")
    else:
        return redirect("/", code=302)