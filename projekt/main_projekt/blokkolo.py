
from .mappaszerkezet import *
class Blokkolo:
    def __init__(self, mappa:Mappa, nev:str="noname_blokkolo"):
        self.mappa = mappa
        self.nev = nev
        mappa.felepit()
        self.foblokk=self.blokkolo()

    def blokkolo(self):
        blokk=Blokk(self.mappa, [],"0")
        return blokk.blokkolo()

    def change_aktiv(self, id:str):
        lista=id.split("/")
        _id=lista[0] + "/"
        lista=lista[1:]
        foblokk=self.foblokk
        blokk=foblokk
        for i in lista:
            _id+=i
            blokk=foblokk.get_blokk(_id=_id)
            if blokk is None:
                print("def change_aktiv HIBA " + _id)
                return
            foblokk=blokk
            _id+="/"
        blokk.change_aktiv()

    def to_string(self):
        return self.foblokk.to_string()

    def html(self):
        return self.foblokk.html()





class Blokk:
    def __init__(self, mappa:Mappa, blokk_lista:list['Blokk'], id:str= "0"):
        self.mappa = mappa
        self.blokk_lista = blokk_lista
        self.id = id
        self.aktiv=False

    def blokkolo(self):
        index=0
        for m in self.mappa.get_mappak():
            blokk=Blokk(mappa=m, blokk_lista=[], id=self.id + "/" + str(index))
            self.blokk_lista.append(blokk)
            index+=1
        for b in self.blokk_lista:
            b.blokkolo()
        return self

    def get_blokk(self, _id:str):
        for b in self.blokk_lista:
            if b.id == _id:
                return b

    def to_string(self, ki=None, melyseg=0):
        if melyseg==0:
            ki=[]
        ki.append(melyseg*"  " + self.id)
        if self.aktiv:
            for b in self.blokk_lista:
                b.to_string(ki=ki, melyseg=melyseg+1)
        return ki

    def change_aktiv(self):
        self.aktiv = not self.aktiv
        print("change_aktiv " + self.id)

    def html(self, ki=None, melyseg=0):
        if melyseg==0:
            ki=[]
        ki.append(Trio(nev=self.mappa.get_nev(),fileok=self.mappa.get_fileok(),id=self.id, melyseg=melyseg, isfile=False))
        if self.aktiv:
            for b in self.blokk_lista:
                b.html(ki=ki, melyseg=melyseg+1)
            for f in self.mappa.get_fileok():
                ki.append(Trio(nev=f.get_nev(),fileok=[],id=self.id,melyseg=melyseg+1,isfile=True))
        return ki


class Trio:
    def __init__(self,nev:str , fileok:list['File'], id:str="0", melyseg:int=0, isfile=False):
        self.nev = nev
        self.fileok = fileok
        self.id = id
        self.melyseg = melyseg
        self.isfile = isfile

    def get_nev(self):
        logo="📄"
        if not self.isfile:
            logo="📁"
        return logo + self.nev
    def get_space(self):
        return self.melyseg * "    "
    def get_fileok(self):
        kimenet=""
        for f in self.fileok:
            kimenet+="\n" + (self.melyseg+1) * "    " + f.get_nev()
        return kimenet
    def get_id(self):
        return self.id
    def is_file(self):
        return self.isfile


# mappa=Mappa(gyoker=None,nev="root",utvonal=r"K:\ide")
# blokkolo=Blokkolo(mappa=mappa,nev="lulu_blokkolo")
# blokkolo.change_aktiv("0/0")
# blokkolo.change_aktiv("0/0/1")
# blokkolo.change_aktiv("0/0/2")
# blokkolo.change_aktiv("0/0/0/2")
# blokkolo.change_aktiv("0/0/2/0")
# ki=blokkolo.html()
# for i in ki:
#      print(i.get_space + i.get_nev() + " " + i.get_id())