from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Veritabanı bağlantısını sağlayan yardımcı fonksiyon
def get_db_connection():
    conn = sqlite3.connect('v11.gts.sqlite3.db')
    conn.row_factory = sqlite3.Row
    return conn

# İstenen id'ye göre alanları döndüren rota
@app.route('/api/madde_anlam/<int:madde_id>', methods=['GET'])
def get_madde_anlam_by_id(madde_id):
    conn = get_db_connection()
    
    # madde tablosundan veri çekme
    madde_item = conn.execute('SELECT * FROM madde WHERE madde_id = ?', (madde_id,)).fetchone()
    
    # anlam tablosundan veri çekme
    anlam_item = conn.execute('SELECT * FROM anlam WHERE madde_id = ?', (madde_id,)).fetchone()
    
    conn.close()
    
    if madde_item and anlam_item:
        response = {
            "madde_id": madde_item['madde_id'],
            "madde": madde_item['madde'],
            "anlam": anlam_item['anlam']
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)