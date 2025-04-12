from flask import Flask, render_template, request
import json
import subprocess
import os
import sys

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def our_sites():
    bloked_site = []

    if request.method == "POST":
        our_sites_data = request.form.get("our_sites", "")
        lines = our_sites_data.splitlines()

        # Зберігаємо список у JSON
        with open("our_sites.json", "w", encoding="utf-8") as f:
            json.dump(lines, f, indent=2, ensure_ascii=False)

        try:
            result = subprocess.run(
                [sys.executable, os.path.join(os.getcwd(), "parsing.py")],
                check=True,
                capture_output=True,
                text=True
            )

            # Після виконання parsing.py зчитуємо result.json
            if os.path.exists("result.json"):
                with open("result.json", "r", encoding="utf-8") as f:
                    bloked_site = json.load(f)

            return render_template(
                "compresion_blocked_sites.html",
                our_sites=our_sites_data,
                message=result.stdout,
                bloked_site=bloked_site
            )

        except subprocess.CalledProcessError as e:
            return render_template(
                "index.html",
                our_sites=our_sites_data,
                message=f"Помилка під час парсингу:\n{e.stderr}",
                bloked_site=[]
            )

    return render_template("compresion_blocked_sites.html", our_sites="", bloked_site=[])

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # або будь-який інший вільний порт

