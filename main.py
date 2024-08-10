from flask import Flask,render_template,url_for,request,redirect,session,logging
from flask_mysqldb import MySQL
from wtforms import Form,StringField,PasswordField,TextAreaField,SelectField,validators, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, URL
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
import os
import uuid



app = Flask(__name__)
app.secret_key = "super secret key"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "veritabanı"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

  

mysql = MySQL(app)

class Login(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

class Editor(Form):
    title = StringField("Başlık")
    content = TextAreaField("İçerik")
    resim = FileField("Resim", validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    cat = SelectField('Kategori', choices=[("",""),('Teknoloji', 'Teknoloji'), ('Programlama', 'Programlama'), ('Siber Güvenlik', 'Siber Güvenlik')])

class Profile(Form):
    uname = StringField("Kullanıcı Adı")
    email = StringField("E-Mail")
    passwd = PasswordField("Parola")
    ozet = TextAreaField("Özet Hakkımızda")
    tw = StringField("Twitter", validators=[URL()])
    li = StringField("Linkdin", validators=[URL()])
    gh = StringField("GitHub", validators=[URL()])
    st = StringField("Stackoverflow", validators=[URL()])



@app.route("/")
def home():    
    cursor = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    sorgu = "Select * from users"
    sorgu2 = "Select * from posts"
    result = cursor.execute(sorgu)
    result2 = cursor2.execute(sorgu2)
    if result > 0 and result2 > 0 :
        posted = cursor2.fetchall()
        ana = cursor.fetchone()
        return render_template("/main/index.html",ana = ana,posted=posted)
    else:
        return render_template("/onfix.html")

@app.route("/panel/posts/<string:id>")
def details(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * from posts where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        deta = cursor.fetchone()
        return render_template("/admin/panel/details.html",deta=deta)
    else :
        return render_template("/admin/panel/details.html")
    
@app.route("/about")
def about():
    cursor = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    sorgu = "Select * from users"
    sorgu2 = "Select * from about"
    result = cursor.execute(sorgu)
    result2 = cursor2.execute(sorgu2)
    if result > 0 and result2 > 0:
        post2 = cursor2.fetchone()
        post = cursor.fetchone()
        return render_template("/admin/panel/about.html",post=post,post2=post2)
    else :
        return redirect(url_for("home"))

@app.route("/adit")
def adit():
    if request.method == "GET":
        cursor  = mysql.connection.cursor()
        sorgu = "Select * from about"
        result = cursor.execute(sorgu)
        if result == 0 :
            return redirect(url_for("admin"))
        else: 
            posts = cursor.fetchone()
            form = Editor()
            form.title.data = posts["hk"]
            form.content.data = posts["hkm"]
            form.cat.data = posts["cat"]
            return render_template("admin/panel/update.html",form = form)
    else :
        form = Editor(request.form)
        NewT = form.title.data 
        NewC = form.content.data
        NewK = form.cat.data
        NewF = request.files["resim"]
        if NewF.filename == '':
            sorgu2 = "Update posts  Set title = %s , content = %s , cat = %s  where id = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu2,(NewT,NewC,NewK,id))
            mysql.connection.commit()
            return redirect(url_for("admin"))
        else:
            resim = str(uuid.uuid4()) + os.path.splitext(NewF.filename)[1]
            NewF.save(os.path.join(app.root_path, "static/assets/images", resim))
            sorgu2 = "Update posts  Set title = %s , content = %s , cat = %s , resim = %s where id = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu2,(NewT,NewC,NewK,resim,id))
            mysql.connection.commit()
            return redirect(url_for("admin"))


@app.route("/post/<string:id>")
def gonderi(id):
    cursor = mysql.connection.cursor()
    cursor2 = mysql.connection.cursor()
    sorgu = "Select * from posts where id = %s"
    sorgu2 = "Select * from users"
    result = cursor.execute(sorgu,(id,))
    result2 = cursor2.execute(sorgu2)
    if result > 0 and result2 > 0:
        post2 = cursor2.fetchone()
        post = cursor.fetchone()
        return render_template("/main/post.html",post=post,post2=post2)
    else :
        return redirect(url_for("home"))

@app.route("/panel/home")
def admin():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from posts where id "
    result = cursor.execute(sorgu)
    if result > 0 :
        posts = cursor.fetchall()
        return render_template("admin/panel/index.html",posts = posts)
    else:
        return render_template("admin/main.html")



@app.route("/panel/edit/<string:id>" , methods=["POST","GET"])
def edit(id):
    if request.method == "GET":
        cursor  = mysql.connection.cursor()
        sorgu = "Select * from posts where id  = %s "
        result = cursor.execute(sorgu,(id,))
        if result == 0 :
            return redirect(url_for("admin"))
        else: 
            posts = cursor.fetchone()
            form = Editor()
            form.title.data = posts["title"]
            form.content.data = posts["content"]
            form.cat.data = posts["cat"]
            return render_template("admin/panel/update.html",form = form)
    else :
        form = Editor(request.form)
        NewT = form.title.data 
        NewC = form.content.data
        NewK = form.cat.data
        NewF = request.files["resim"]
        if NewF.filename == '':
            sorgu2 = "Update posts  Set title = %s , content = %s , cat = %s  where id = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu2,(NewT,NewC,NewK,id))
            mysql.connection.commit()
            return redirect(url_for("admin"))
        else:
            resim = str(uuid.uuid4()) + os.path.splitext(NewF.filename)[1]
            NewF.save(os.path.join(app.root_path, "static/assets/images", resim))
            sorgu2 = "Update posts  Set title = %s , content = %s , cat = %s , resim = %s where id = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu2,(NewT,NewC,NewK,resim,id))
            mysql.connection.commit()
            return redirect(url_for("admin"))



@app.route("/panel/ekle/", methods=["GET","POST"])
def ekle():
    cursor  = mysql.connection.cursor()
    if request.method == "POST":
        YeniT = request.form['baslik']
        YeniC= request.form['icerik']
        YeniK = request.form['kategori']
        NewF = request.files["resim"]
        if NewF.filename == '':
            sorgu2 = "INSERT INTO posts  Set title = %s , content = %s , cat = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu2,(YeniT,YeniC,YeniK))
            mysql.connection.commit()
            return redirect(url_for("admin"))
        else:
            resim = str(uuid.uuid4()) + os.path.splitext(NewF.filename)[1]
            NewF.save(os.path.join(app.root_path, "static/assets/images", resim))
            sorgu2 = "INSERT INTO posts  Set title = %s , content = %s , cat = %s , resim = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu2,(YeniT,YeniC,YeniK,resim))
            mysql.connection.commit()
            return redirect(url_for("admin"))
            
    else:
        return "<script>alert('Eklenemedi');window.location.href = '/panel/home';</script>"


@app.route("/panel/profile/delete/")
def pdelete():
    id = session["username"]
    cursor = mysql.connection.cursor()
    sorgu = "SELECT rank FROM users WHERE username = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        rank = cursor.fetchone()
        if rank != "admin":
            no = "admin"
            return render_template("/admin/panel/pdelete.html",no=no)
        else:
            return render_template("/admin/panel/pdelete.html",rank=rank)
    else :
        return render_template("/admin/panel/profile.html")
    

@app.route("/panel/profile/", methods=["GET", "POST"])
def phome():
    if request.method == "GET":
        curs1 = mysql.connection.cursor()
        sorgu = "SELECT * FROM users WHERE username = %s"
        result = curs1.execute(sorgu, (session["username"],))
        if result == 0:
            return redirect(url_for("admin"))
        else:
            posts = curs1.fetchone()
            form = Profile()
            form.uname.data = posts["username"]
            form.email.data = posts["email"]
            form.passwd.data = posts["password"]
            form.ozet.data = posts["ozet"]
            form.tw.data = posts["tw"]
            form.li.data = posts["li"]
            form.gh.data = posts["gh"]
            form.st.data = posts["st"]
            return render_template("/admin/panel/profile.html", form=form)
    else:
        form = Profile(request.form)
        NewT = form.uname.data
        NewC = form.email.data
        NewK = form.passwd.data
        NewF = request.files["resim"]
        resim = str(uuid.uuid4()) + os.path.splitext(NewF.filename)[1]
        NewF.save(os.path.join(app.root_path, "static/assets/images", resim))
        Func1 = form.ozet.data
        Func2 = form.tw.data
        Func3 = form.li.data
        Func4 = form.gh.data
        Func5 = form.st.data
        if NewF.filename == '':
        # Resim yüklenmediği için sadece diğer alanları güncelle
            if NewK == "":
                sorgu2 = "UPDATE users SET username = %s, email = %s, ozet = %s, tw = %s, li = %s, gh = %s, st = %s WHERE username = %s"
                curs3 = mysql.connection.cursor()
                curs3.execute(sorgu2, (NewT, NewC, Func1, Func2, Func3, Func4, Func5, session["username"]))
                mysql.connection.commit()
                session["username"] = form.uname.data
                return redirect(url_for("phome"))
            else:
                sorgu2 = "UPDATE users SET username = %s, email = %s, password = %s, ozet = %s, tw = %s, li = %s, gh = %s, st = %s WHERE username = %s"
                curs2 = mysql.connection.cursor()
                curs2.execute(sorgu2, (NewT, NewC, NewK, Func1, Func2, Func3, Func4, Func5, session["username"]))
                mysql.connection.commit()
                session["username"] = form.uname.data
                return redirect(url_for("phome"))
        else:
            resim = str(uuid.uuid4()) + os.path.splitext(NewF.filename)[1]
            NewF.save(os.path.join(app.root_path, "static/assets/images", resim))
            sorgu2 = "UPDATE users SET username = %s, email = %s, password = %s, ozet = %s, tw = %s, li = %s, gh = %s, st = %s, pp = %s WHERE username = %s"
            curs2 = mysql.connection.cursor()
            curs2.execute(sorgu2, (NewT, NewC, NewK, Func1, Func2, Func3, Func4, Func5, resim, session["username"]))
            mysql.connection.commit()
            session["username"] = form.uname.data
            return redirect(url_for("phome"))

@app.route("/panel/profile/<string:id>")
def profile(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * from users where id = %s "
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        users = cursor.fetchone()
        return render_template("/admin/panel/profile.html",users=users)
    else :
        return render_template("/admin/panel/profile.html")

@app.route("/panel/ayarlar")
def ayar():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from ayar"
    result = cursor.execute(sorgu)
    if result > 0:
        ayar = cursor.fetchone()
        return render_template("/admin/panel/ayar.html",ayar=ayar)
    else: 
        return render_template("/admin/panel/ayar.html")
@app.route("/login", methods=["GET","POST"])
def login():
    form = Login(request.form)
    if request.method == "POST":
        session["logged_in"] = False
        username = form.username.data
        password = form.password.data
        cursor = mysql.connection.cursor()
        sorgu = "Select * from users where username = %s "
        result = cursor.execute(sorgu,(username,))
        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if real_password == password:
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("admin"))
            else:
                pass
        else:
            pass 
    return render_template("/admin/index.html",form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("notfound.html"),404

@app.route("/delete/<string:id>")
def delete(id):
    try:
        if session["logged_in"] == True :
            cursor = mysql.connection.cursor()
            sorgu = "Select * from posts where id = %s"
            result = cursor.execute(sorgu,(id,))
            if result > 0 :
                sorgu2 = "Delete from posts where id = %s "
                cursor.execute(sorgu2,(id,))
                mysql.connection.commit()
                return redirect(url_for("admin"))
            else: 
                return redirect(url_for("home"))
    
        else:
            return render_template("notfound.html")
    except:
        return render_template("notfound.html")


if __name__ == "__main__":
    app.run(debug=True)
