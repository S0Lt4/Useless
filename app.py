from flask import Flask, render_template, request, send_from_directory
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# --- VERİTABANI KURULUMU ---
def veritabanini_hazirla():
    conn = sqlite3.connect("veritabanı.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sakalar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            arkadas_adi TEXT,
            ip_adresi TEXT,
            cihaz_bilgisi TEXT,
            tarih_saat TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def ana_sayfa():
    kim = request.args.get('kim', 'Bilinmeyen')
    
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
        
    cihaz = request.user_agent.string if request.user_agent else "Bilinmiyor"
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect("veritabanı.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sakalar (arkadas_adi, ip_adresi, cihaz_bilgisi, tarih_saat) VALUES (?, ?, ?, ?)", 
        (kim, ip, cihaz, simdi)
    )
    conn.commit()
    conn.close()
    
    return render_template("main.html")

# --- VİDEOYU GÜVENLİ SERVİS ETME FONKSİYONU ---
# Bu rota, tarayıcının static klasöründeki videoyu takılmadan çekmesini sağlar
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == '__main__':
    veritabanini_hazirla()
    app.run(debug=True)