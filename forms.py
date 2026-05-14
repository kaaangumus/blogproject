from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, URL, Length, Optional, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired(message='Kullanıcı adı gerekli')])
    password = PasswordField('Parola', validators=[DataRequired(message='Parola gerekli')])
    submit   = SubmitField('Giriş Yap')


class PostForm(FlaskForm):
    title   = StringField('Başlık', validators=[DataRequired(), Length(min=2, max=200)])
    content = TextAreaField('İçerik', validators=[DataRequired()])
    resim   = FileField('Kapak Resmi', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Sadece resim dosyaları!')])
    cat     = SelectField('Kategori', choices=[])
    submit  = SubmitField('Kaydet')


class ProfileForm(FlaskForm):
    username = StringField('Kullanıcı Adı', validators=[DataRequired()])
    email    = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Yeni Parola (boş bırakılabilir)', validators=[Optional()])
    ozet     = TextAreaField('Hakkımda', validators=[Optional()])
    tw       = StringField('Twitter URL', validators=[Optional(), URL()])
    li       = StringField('LinkedIn URL', validators=[Optional(), URL()])
    gh       = StringField('GitHub URL', validators=[Optional(), URL()])
    st       = StringField('Stack Overflow URL', validators=[Optional(), URL()])
    pp       = FileField('Profil Fotoğrafı', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png'], 'Sadece resim!')])
    submit   = SubmitField('Güncelle')


class AboutForm(FlaskForm):
    hk      = StringField('Başlık', validators=[DataRequired()])
    hkm     = TextAreaField('İçerik', validators=[DataRequired()])
    cat     = SelectField('Kategori', choices=[
        ('', 'Seç'),
        ('Teknoloji', 'Teknoloji'),
        ('Programlama', 'Programlama'),
        ('Siber Güvenlik', 'Siber Güvenlik'),
        ('Genel', 'Genel'),
    ])
    submit  = SubmitField('Güncelle')
