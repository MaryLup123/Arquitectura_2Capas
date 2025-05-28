from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Crear la base de datos si no existe
def init_db():
    if not os.path.exists('productos.db'):
        conn = sqlite3.connect('productos.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    total = len(productos)
    conn.close()
    return render_template('index.html', productos=productos, total=total)


@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    conn = sqlite3.connect('productos.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
    conn.commit()
    conn.close()
    return redirect('/')



if __name__ == '__main__':
    init_db()
   

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

