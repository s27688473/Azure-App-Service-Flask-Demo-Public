from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# 從 App Service 環境變數取得連線字串
conn = psycopg2.connect(os.environ['POSTGRES_CONN'])


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")

        if name:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (name) VALUES (%s)", (name,))
            conn.commit()
            cur.close()

    # 查詢資料
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    cur.close()

    return render_template("index.html", rows=rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
