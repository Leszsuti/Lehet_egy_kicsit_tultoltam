class Valaki:
    def __init__(self,neptun_kod="", neptun_jelszo="", h_azonosito="", h_jelszo="", github_felhasznalonev="", github_token="", email=""):
        self.neptun_kod = neptun_kod
        self.neptun_jelszo = neptun_jelszo
        self.h_azonosito = h_azonosito
        self.h_jelszo = h_jelszo
        self.github_felhasznalonev=github_felhasznalonev
        self.github_token=github_token
        self.email=email
        self.mentett= {}

    def __str__(self):
        return self.neptun_kod + "\n" + self.neptun_jelszo + "\n" + self.h_azonosito + "\n" + self.h_jelszo + "\n" + self.github_felhasznalonev + "\n" + self.github_token + "\n" + self.email + "\n"

    def read_txt(self):
        try:
            with open("valaki.txt","r") as f:
                lista = f.readlines()
                print("lista: ", lista)
                self.neptun_kod = lista[0].strip()
                self.neptun_jelszo = lista[1].strip()
                self.h_azonosito = lista[2].strip()
                self.h_jelszo = lista[3].strip()
                self.github_felhasznalonev = lista[4].strip()
                self.github_token = lista[5].strip()
                self.email=lista[6].strip()
        except Exception as e:
            print("valaki.read_txt_exception")
            self.neptun_kod = ""
            self.neptun_jelszo = ""
            self.h_azonosito = ""
            self.h_jelszo = ""
            self.github_felhasznalonev = ""
            self.github_token = ""
            self.email = ""

    def ment_adat(self, nev:str, ertek):
        self.mentett[nev] = ertek
    def get_adat(self, nev:str):
        if self.mentett.get(nev) is None:
            return ""
        return self.mentett[nev]

    def minden_adat_meg_van_adva(self):
        if self.neptun_kod is None or self.neptun_jelszo is None or self.h_azonosito is None or self.h_jelszo is None or self.github_felhasznalonev is None or self.github_token is None or self.email is None:
            return False
        if self.neptun_kod == "" or self.neptun_jelszo == "" or self.h_azonosito == "" or self.h_jelszo == "" or self.github_felhasznalonev == "" or self.github_token == "" or self.email == "":
            return False
        return True