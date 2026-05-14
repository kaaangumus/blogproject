#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""NF Blog - Automated Test Script"""
import requests

BASE = "http://127.0.0.1:5000"
s = requests.Session()

print("=" * 50)
print("NF Blog Otomatik Test")
print("=" * 50)

# Test 1: Ana sayfa
r = s.get(f"{BASE}/")
status = "OK" if r.status_code == 200 else "FAIL"
has_content = "NF BLOG" in r.text
print(f"[{status}] GET /         -> {r.status_code} | NF BLOG gorunu: {has_content}")

# Test 2: Login sayfası GET
r = s.get(f"{BASE}/login")
status = "OK" if r.status_code == 200 else "FAIL"
has_form = "csrf_token" in r.text
print(f"[{status}] GET /login    -> {r.status_code} | CSRF token: {has_form}")

# Test 3: CSRF token al ve login yap
import re
csrf_match = re.search(r'name="csrf_token"[^>]+value="([^"]+)"', r.text)
if csrf_match:
    csrf = csrf_match.group(1)
    
    # Test 4: Yanlış şifre
    data = {"username": "admin", "password": "yanlis_sifre", "csrf_token": csrf}
    r2 = s.post(f"{BASE}/login", data=data)
    status = "OK" if r2.status_code == 200 else "FAIL"
    has_error = "Kullanici adi" in r2.text or "yanlış" in r2.text.lower() or "login" in r2.url.lower()
    print(f"[{status}] POST /login (yanlis sifre) -> {r2.status_code} | Hata mesaji: {has_error}")

    # Test 5: Doğru giriş
    r3_get = s.get(f"{BASE}/login")  # Taze CSRF token al
    csrf2 = re.search(r'name="csrf_token"[^>]+value="([^"]+)"', r3_get.text).group(1)
    data2 = {"username": "admin", "password": "admin123", "csrf_token": csrf2}
    r3 = s.post(f"{BASE}/login", data=data2, allow_redirects=True)
    status = "OK" if r3.status_code == 200 else "FAIL"
    is_panel = "NF Panel" in r3.text or "Yazi Yonetimi" in r3.text or "navbar" in r3.text
    print(f"[{status}] POST /login (dogru) -> {r3.status_code} | Panel erisme: {is_panel}")
    
    if is_panel:
        # Test 6: Admin panel GET
        r4 = s.get(f"{BASE}/panel/home")
        status = "OK" if r4.status_code == 200 else "FAIL"
        print(f"[{status}] GET /panel/home -> {r4.status_code}")

        # Test 7: Profil sayfası
        r5 = s.get(f"{BASE}/panel/profile/")
        status = "OK" if r5.status_code == 200 else "FAIL"
        print(f"[{status}] GET /panel/profile/ -> {r5.status_code}")

        # Test 8: About sayfası public
        r6 = s.get(f"{BASE}/about")
        status = "OK" if r6.status_code in [200, 302] else "FAIL"
        print(f"[{status}] GET /about -> {r6.status_code}")

        # Test 9: 404 sayfası
        r7 = s.get(f"{BASE}/bu-sayfa-yok")
        status = "OK" if r7.status_code == 404 else "FAIL"
        print(f"[{status}] GET /bu-sayfa-yok -> {r7.status_code} (404 bekleniyor)")

        # Test 10: Logout
        r8 = s.get(f"{BASE}/logout", allow_redirects=True)
        status = "OK" if r8.status_code == 200 else "FAIL"
        print(f"[{status}] GET /logout -> {r8.status_code}")
        
        # Test 11: Panel erişimi login sonrası bloklu mu?
        r9 = s.get(f"{BASE}/panel/home", allow_redirects=True)
        is_redirect_to_login = "login" in r9.url or "Giris" in r9.text or "NF Panel" not in r9.text
        status = "OK" if is_redirect_to_login else "FAIL"
        print(f"[{status}] GET /panel/home (logout sonrasi) -> {r9.status_code} | Login'e yonlendirme: {is_redirect_to_login}")

else:
    print("[FAIL] CSRF token alinamadi!")

print("=" * 50)
print("Test tamamlandi.")
