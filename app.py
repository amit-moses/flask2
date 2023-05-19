from flask import Flask, render_template, request, redirect, session


app = Flask(__name__)
app.secret_key = b'_5#y2L"F45664543KLQ8z\n\xec]/'

STUDENTS = [
    {"name":"Ran", "phone": "050-4445555"},
    {"name":"Or", "phone": "053-9995555"},
    {"name":"Binyamin", "phone": "052-43345555"}]

@app.route("/", methods=["GET","POST"])
def index():
   if session.get("logged_in_user"):
        return redirect("/students")
   user = request.form.get("username")
   password = request.form.get("password")
   if user == "ran" and password == "123":
       session['logged_in_user'] = user
       session['color_picked'] = request.form.get("color")
       return redirect("/students")
   return render_template("index.html")

@app.route("/students")
def students():    
   
   if not session.get("logged_in_user"):
        return redirect("/")
    # check if logged in. if not redirect("/")
   return render_template("students.html", students = STUDENTS, logged_in_user=session.get("logged_in_user"))

@app.route("/logout")
def logout():
    # session.clear()
    session['logged_in_user'] = ''
    return redirect("/")

@app.route("/students/search")
def search():
    if not session.get("logged_in_user"):
        return redirect("/")
    args_tp = request.args
    if len(args_tp) == 0:
        return redirect("/students")
    else:
        search_n = args_tp.get("search_name").lower()
        search_p = args_tp.get("search_phone").lower()
        if len(search_n) == 0 and len(search_p) == 0:
            return redirect("/students")
        filtered = filter(lambda st: search_n in st['name'].lower() and search_p in st["phone"].lower(), STUDENTS)
        # new_list = [student for student in STUDENTS if search in student]   
        return render_template("students.html", students = filtered, logged_in_user=session.get("logged_in_user"), ser_n=search_n, ser_p=search_p)

if __name__ == '__main__':
   app.run(debug=True, port=9000)