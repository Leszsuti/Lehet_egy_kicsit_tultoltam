import threading
import time
import webbrowser

from flask import Flask, render_template, request
from valaki import Valaki
from main_projekt import connect_ssh
import neptunorarend
from main_projekt.github_view import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)
valaki = Valaki()
table=[]
@app.route('/main_view/',methods=['GET','POST'])
def index():
    global valaki
    uzenet = ""
    if request.method == 'POST':
        gomb=request.form['gomb']
        if gomb == 'mentes':
            valaki.neptun_kod=request.form['neptun_kod']
            valaki.neptun_jelszo=request.form['neptun_jelszo']
            valaki.h_azonosito=request.form['h_azonosito']
            valaki.h_jelszo=request.form['h_jelszo']
            valaki.github_felhasznalonev=request.form['github_felhasznalonev']
            valaki.github_token=request.form['github_token']
            valaki.email=request.form['email']
            print(valaki)
            # if valaki.minden_adat_meg_van_adva():
            with open("valaki.txt","w") as f:
                f.write(str(valaki))
            uzenet = "Sikeres mentés"
            # else:
            # uzenet = "Ahhoz, hogy el legyen mentve, minden mezőt ki kell tölteni."
        if gomb == 'legutobbi':
            valaki.read_txt()
            print(valaki)

        if gomb == 'ssh':
            if valaki.h_azonosito is not None and valaki.h_azonosito != "":
                connect_ssh.connect(valaki)
            else:
                uzenet="h-s azonosító kitöltése szükséges"
        if gomb == 'orarend':
            if valaki.neptun_kod is not None and valaki.neptun_kod != "" and valaki.neptun_jelszo is not None and valaki.neptun_jelszo != "":
                global table
                neptunorarend.magic(valaki)
                table = neptunorarend.tabla
                neptunorarend.ablak()
            else:
                uzenet="Neptun kód és jelszó kitöltése szükséges"
        if gomb == 'github':
            if valaki.github_token is not None and valaki.github_token != "" and valaki.github_felhasznalonev is not None and valaki.github_felhasznalonev != "" and valaki.email is not None and valaki.email != "":
                webbrowser.open("http://127.0.0.1:5000/github/")
            else:
                uzenet = "GitHub felhasználónév, email és token kitöltése szükséges"

    return render_template("main_view.html", valaki=valaki, uzenet=uzenet)


@app.route("/orarend/")
def orarendd():
    return render_template("orarend.html", tabla=table)


def indit_server():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    print("STARTED")
    threading.Thread(target=indit_server).start()
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000/main_view/")

