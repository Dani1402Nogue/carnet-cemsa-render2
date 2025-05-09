from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def form():
    return render_template("form.html")

@app.route("/descargar", methods=["POST"])
def descargar():
    dni = request.form["dni"]
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    try:
        driver.get("https://www.manejocemsa.com.ar/Ingreso.php")
        time.sleep(2)
        empresa = driver.find_element(By.NAME, "empresa")
        for option in empresa.find_elements(By.TAG_NAME, 'option'):
            if "PECOM ARGENTINA" in option.text:
                option.click()
                break
        driver.find_element(By.NAME, "clave").send_keys("PECOMARGENTINA")
        driver.find_element(By.NAME, "btningresar").click()
        time.sleep(2)

        result = f"Login exitoso. DNI recibido: {dni}"

    except Exception as e:
        result = f"Error: {str(e)}"

    driver.quit()
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)