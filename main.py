import os
import uuid

from flask import Flask, render_template, url_for, request, redirect, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

from config import Config
from models import db, User, Post, About, Setting
from forms import LoginForm, PostForm, ProfileForm, AboutForm

# ─────────────────────────── App & Extensions ────────────────────────────────
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt   = Bcrypt(app)
csrf     = CSRFProtect(app)
login_mgr = LoginManager(app)
login_mgr.login_view         = 'login'
login_mgr.login_message      = 'Bu sayfaya erişmek için giriş yapmalısınız.'
login_mgr.login_message_category = 'warning'


@login_mgr.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ─────────────────────────── Helpers ─────────────────────────────────────────
ALLOWED_EXT = {'jpg', 'jpeg', 'png', 'gif'}

def save_picture(file_storage):
    """Uploaded file'ı benzersiz isimle kaydet, dosya adını döndür."""
    ext = os.path.splitext(file_storage.filename)[1].lower()
    filename = uuid.uuid4().hex + ext
    path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file_storage.save(path)
    return filename


# ─────────────────────────── Public Routes ───────────────────────────────────
@app.route('/')
def home():
    ana    = User.query.first()
    posted = Post.query.order_by(Post.date.desc()).all()
    if not ana:
        return render_template('onfix.html')
    return render_template('main/index.html', ana=ana, posted=posted)


@app.route('/post/<int:post_id>')
def gonderi(post_id):
    post = Post.query.get_or_404(post_id)
    ana  = User.query.first()
    return render_template('main/post.html', post=post, post2=ana)


@app.route('/about')
def about():
    ana        = User.query.first()
    about_info = About.query.first()
    if not ana or not about_info:
        return redirect(url_for('home'))
    return render_template('main/about.html', post=ana, post2=about_info)


# ─────────────────────────── Auth Routes ─────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Hoş geldiniz!', 'success')
            nxt = request.args.get('next')
            return redirect(nxt or url_for('admin'))
        flash('Kullanıcı adı veya parola yanlış.', 'danger')
    return render_template('admin/index.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Çıkış yapıldı.', 'info')
    return redirect(url_for('home'))


# ─────────────────────────── Admin Routes ────────────────────────────────────
@app.route('/panel/home')
@login_required
def admin():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('admin/panel/index.html', posts=posts)


@app.route('/panel/ekle/', methods=['GET', 'POST'])
@login_required
def ekle():
    form = PostForm()
    if form.validate_on_submit():
        resim_fn = ''
        if form.resim.data and form.resim.data.filename:
            resim_fn = save_picture(form.resim.data)
        post = Post(
            title   = form.title.data,
            content = form.content.data,
            cat     = form.cat.data,
            resim   = resim_fn,
        )
        db.session.add(post)
        db.session.commit()
        flash('Yazı başarıyla eklendi!', 'success')
        return redirect(url_for('admin'))
    # GET veya hata → panele yönlendir (modal üzerinden)
    return redirect(url_for('admin'))


@app.route('/panel/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title   = form.title.data
        post.content = form.content.data
        post.cat     = form.cat.data
        if form.resim.data and form.resim.data.filename:
            post.resim = save_picture(form.resim.data)
        db.session.commit()
        flash('Yazı güncellendi!', 'success')
        return redirect(url_for('admin'))
    # Pre-fill
    form.title.data   = post.title
    form.content.data = post.content
    form.cat.data     = post.cat
    return render_template('admin/panel/update.html', form=form, post=post)


@app.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Yazı silindi.', 'info')
    return redirect(url_for('admin'))


@app.route('/panel/profile/', methods=['GET', 'POST'])
@login_required
def phome():
    form = ProfileForm()
    user = current_user
    if form.validate_on_submit():
        # Profil fotoğrafı
        if form.pp.data and form.pp.data.filename:
            user.pp = save_picture(form.pp.data)
        user.username = form.username.data
        user.email    = form.email.data
        if form.password.data:
            user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.ozet = form.ozet.data or ''
        user.tw   = form.tw.data   or '#'
        user.li   = form.li.data   or '#'
        user.gh   = form.gh.data   or '#'
        user.st   = form.st.data   or '#'
        db.session.commit()
        flash('Profil güncellendi!', 'success')
        return redirect(url_for('phome'))
    # GET → pre-fill
    form.username.data = user.username
    form.email.data    = user.email
    form.ozet.data     = user.ozet
    form.tw.data       = user.tw if user.tw != '#' else ''
    form.li.data       = user.li if user.li != '#' else ''
    form.gh.data       = user.gh if user.gh != '#' else ''
    form.st.data       = user.st if user.st != '#' else ''
    return render_template('admin/panel/profile.html', form=form)


@app.route('/panel/about/', methods=['GET', 'POST'])
@login_required
def panel_about():
    about_info = About.query.first()
    form = AboutForm()
    if form.validate_on_submit():
        if about_info:
            about_info.hk  = form.hk.data
            about_info.hkm = form.hkm.data
            about_info.cat = form.cat.data
        else:
            about_info = About(hk=form.hk.data, hkm=form.hkm.data, cat=form.cat.data)
            db.session.add(about_info)
        db.session.commit()
        flash('Hakkımda sayfası güncellendi!', 'success')
        return redirect(url_for('panel_about'))
    if about_info:
        form.hk.data  = about_info.hk
        form.hkm.data = about_info.hkm
        form.cat.data = about_info.cat
    return render_template('admin/panel/about_edit.html', form=form)


@app.route('/panel/details/<int:post_id>')
@login_required
def details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('admin/panel/details.html', deta=post)


# ─────────────────────────── Error Handlers ──────────────────────────────────
@app.errorhandler(404)
def page_not_found(e):
    return render_template('notfound.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('notfound.html'), 500


# ─────────────────────────── DB Init & Run ───────────────────────────────────
def init_db():
    """Veritabanı tablolarını oluştur ve yoksa admin kullanıcısı ekle."""
    db.create_all()

    if not User.query.first():
        hashed = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin  = User(
            username = 'admin',
            email    = 'admin@nfblog.com',
            password = hashed,
            rank     = 'admin',
            ozet     = 'Penetration Tester | Red Teamer',
            tw       = '#',
            li       = '#',
            gh       = 'https://github.com/kaaangumus',
            st       = '#',
        )
        db.session.add(admin)
        db.session.commit()
        print('[NF Blog] Admin kullanicisi olusturuldu -> admin / admin123')

    if not About.query.first():
        about = About(
            hk  = 'Hakkimda',
            hkm = 'Bu sayfayi duzenlemek icin panele girin.',
            cat = 'Genel',
        )
        db.session.add(about)
        db.session.commit()

    if not Setting.query.first():
        setting = Setting(
            title    = 'NF Blog',
            content  = 'Siber Guvenlik & Programlama',
            content2 = 'NF Blog',
        )
        db.session.add(setting)
        db.session.commit()

    print('[NF Blog] Veritabani hazir.')


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
