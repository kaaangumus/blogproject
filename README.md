# NF Blog - Modern Flask Blog Application

NF Blog, siber güvenlik uzmanları, geliştiriciler ve teknoloji tutkunları için tasarlanmış, modern ve güvenli bir **Python/Flask** blog uygulamasıdır. Proje, amatör veya başlangıç seviyesindeki bir Flask altyapısının sektör standartlarında **SQLAlchemy**, **Bcrypt** ve **Flask-Login** gibi modern pratiklerle tamamen yeniden yazılmış ve profesyonel hale getirilmiş halidir.

## 🚀 Özellikler

- **Modern ORM (SQLAlchemy):** Veritabanı işlemleri için ham SQL sorguları yerine güvenilir Flask-SQLAlchemy kullanıldı.
- **Gelişmiş Güvenlik:** 
  - Şifreler düz metin yerine **Flask-Bcrypt** ile güvenli bir şekilde hashlenerek saklanmaktadır.
  - Formlarda **Flask-WTF** kullanılarak CSRF (Cross-Site Request Forgery) koruması sağlanmıştır.
- **Güvenli Oturum Yönetimi:** Flask-Login ile profesyonel session yönetimi ve `@login_required` rota koruması eklendi.
- **Admin Paneli:** Yazıları ekleme, düzenleme, silme, profil yönetimi, **kategori oluşturma** ve **genel site ayarları** (başlık, SEO açıklamaları) tamamen dinamik hale getirildi.
- **CKEditor Entegrasyonu:** Yazı ve Hakkımda sayfaları için güncel ve güvenli **CKEditor 4.25.1-LTS** entegrasyonu.
- **Otomatik Kurulum:** Uygulama ilk kez çalıştırıldığında gerekli veritabanı tablolarını, varsayılan kategorileri ve admin kullanıcısını (`admin` / `admin123`) otomatik olarak oluşturur.

## 🛠️ Kurulum ve Çalıştırma

Proje XAMPP (MySQL) veya SQLite ile çalışacak şekilde yapılandırılmıştır.

### 1. Gereksinimleri Yükleyin
Proje dizininde terminal açın ve gerekli Python kütüphanelerini kurun:
```bash
pip install -r requirements.txt
```

### 2. Veritabanı Yapılandırması (.env)
Proje kök dizinindeki `.env` dosyasını kendi veritabanı bilgilerinize göre düzenleyebilirsiniz (Varsayılan ayarlar XAMPP MySQL içindir):
```env
SECRET_KEY=kendi_guvenli_anahtarin
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=blogproject
```
*(Not: MySQL kullanmıyorsanız SQLAlchemy URI'sini SQLite olarak `config.py` içerisinden değiştirebilirsiniz.)*

### 3. Uygulamayı Başlatın
Uygulamayı çalıştırdığınızda eksik tablolar otomatik oluşturulacaktır:
```bash
python main.py
```

### 4. Giriş Yapın
- **Blog Arayüzü:** `http://127.0.0.1:5000`
- **Yönetim Paneli:** `http://127.0.0.1:5000/login`
- **Varsayılan Giriş Bilgileri:**
  - Kullanıcı Adı: `admin`
  - Şifre: `admin123`

## 📁 Proje Yapısı

- `main.py` - Flask uygulaması, rotalar (routes) ve core backend mantığı.
- `models.py` - SQLAlchemy veritabanı tabloları (User, Post, About, Category, Setting).
- `forms.py` - Flask-WTF formları ve validasyonlar.
- `config.py` - Uygulama ve veritabanı konfigürasyonu.
- `test_app.py` - Endpoint'leri kontrol eden temel otomatik test scripti.
- `templates/` - Güvenli Jinja2 şablonları (CSRF dahil).
- `static/` - Resimler, CSS stilleri ve JS scriptleri.

## 🤝 Katkıda Bulunma

Hata bildirimleri (issues) veya geliştirme istekleri (pull requests) her zaman memnuniyetle karşılanır. Geliştirme ortamınızın güncel kütüphanelere (`requirements.txt`) ve `.env` ayarlarına sahip olduğundan emin olun.

---
*Bu proje Rubar Gümüş (ve GitHub üzerinden destek sağlayanlar) tarafından geliştirilmiştir.*
