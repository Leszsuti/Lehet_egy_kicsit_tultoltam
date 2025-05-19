import os
from typing import Optional
from github import Github


class File:
    def __init__(self, gyoker: Optional['Mappa'], nev:str="noname", utvonal:str="root", github=False):
        self.gyoker = gyoker
        self.nev = nev
        self.utvonal = utvonal
        self.github = github

    def get_nev(self):
        return self.nev
    def get_utvonal(self):
        return self.utvonal
    def get_gyoker(self):
        return self.gyoker


class Mappa:
    def __init__(self, gyoker: Optional['Mappa'], nev:str="noname", utvonal:str="root", github=False):
        self.gyoker = gyoker
        self.nev = nev
        self.utvonal = utvonal
        self.mappak : list['Mappa'] = []
        self.fileok :list['File'] = []
        self.github = github

    def add_file(self, file:['File']):
        self.fileok.append(file)

    def add_mappa(self, mappa:['Mappa']):
        self.mappak.append(mappa)

    def get_gyoker(self):
        return self.gyoker

    def get_fileok(self):
        return self.fileok

    def get_mappak(self):
        return self.mappak

    def get_nev(self):
        return self.nev

    def get_utvonal(self):
        return self.utvonal

    def get_mappa(self, nev:str):
        for mappa in self.mappak:
            if mappa.nev == nev:
                return mappa
        return None

    def get_file(self, nev:str):
        for file in self.fileok:
            if file.nev == nev:
                return file
        return None

    def get_mappa_file(self, nev:str):
        for mappa in self.mappak:
            if mappa.nev == nev:
                return mappa
        for file in self.fileok:
            if file.nev == nev:
                return file
        return None

    def felepit(self):
        try:
            if self.github:
                return

            self.mappak = []
            self.fileok = []
            mappa=self.get_utvonal()
            mappak = [f for f in os.listdir(mappa) if os.path.isdir(os.path.join(mappa, f))]
            #print(mappak)
            for m in mappak:
                self.add_mappa(Mappa(gyoker=self, nev=m, utvonal=self.get_utvonal() + "\\" + m))

            fileok = [f for f in os.listdir(mappa) if os.path.isfile(os.path.join(mappa, f))]
            #print(fileok)
            for f in fileok:
                self.add_file(File(gyoker=self, nev=f, utvonal=self.get_utvonal() + "\\" + f))

            # print(self.get_nev())
            for m in self.mappak:
                # if m.get_nev() == ".git":
                #     continue
                m.felepit()
                # print(m.get_nev() + " | " + m.get_utvonal() + " | " + m.get_gyoker().get_nev() + " (mappa)")
            # for f in self.fileok:
            #     print(f.get_nev() + " | " + f.get_utvonal() + " | " + f.get_gyoker().get_nev() + " (file)")
        except Exception as e:
            print("nincs ilyen mappa")

    def listaz_all(self, melyseg=0, kimenet=None):
        if melyseg == 0:
            print(self.utvonal)
            kimenet= [self.utvonal]
        for m in self.mappak:
            print(melyseg*"  " + "" + m.get_nev())
            kimenet.append(melyseg*"  " + "" + m.get_nev())
            m.listaz_all(melyseg=melyseg+1, kimenet=kimenet)
        for f in self.fileok:
            print(melyseg*"  " + "" + f.get_nev())
            kimenet.append(melyseg*"  " + "" + f.get_nev())
        return kimenet

    def listaz(self):
        kimenet=[]
        #print("def: listaz")
        for m in self.mappak:
            #print(m.get_nev())
            kimenet.append(m.get_nev())
        for f in self.fileok:
            #print(f.get_nev())
            kimenet.append(f.get_nev())
        return kimenet

    #----------------GITHUB---------------------------------------

    def beolvas_github(self, token:str, repository:str, utvonal:str=""):
        self.mappak=[]
        self.fileok=[]
        self.utvonal = utvonal
        g=Github(token)
        print("g=Github(token)")
        repo = g.get_repo(repository)
        print("repo=Github(repository)")
        contents = repo.get_contents(utvonal)
        print("contents=Github(repository)")
        for content in contents:
            if content.type == "dir":
                mappa=Mappa(gyoker=self,nev=content.name,utvonal=self.get_utvonal() + "/" + content.name, github=True)
                self.mappak.append(mappa)
                mappa.beolvas_github(token=token,repository=repository,utvonal=self.get_utvonal() + "/" + content.name)
            else:
                self.fileok.append(File(gyoker=self,nev=content.name,utvonal=self.get_utvonal() + "/" + content.name, github=True))





class Filekezelo:
    def __init__(self, gyoker:Mappa, nev:str="noname_filekezelo"):
        self.gyoker = gyoker
        self.nev = nev
        self.jelenlegi=gyoker
        gyoker.felepit()

    def get_jelenlegi(self):
        return self.jelenlegi
    def get_nev(self):
        return self.nev
    def get_gyoker(self):
        return self.gyoker

    def utvonal_feldolgozo(self, utvonal:str):
        lista=utvonal.split("/")
        jelenlegi=self.gyoker
        index=0
        while index < len(lista):
            #print(jelenlegi.get_utvonal())
            if jelenlegi is None:
                return None
            utolso=jelenlegi.get_mappa_file(lista[index])
            jelenlegi=utolso
            index+=1
        self.jelenlegi=jelenlegi
        return jelenlegi

    def jelenlegi_gyokere(self):
        if self.jelenlegi == self.gyoker:
            return self.gyoker
        self.jelenlegi=self.jelenlegi.get_gyoker()
        return self.jelenlegi

    def jelenlegi_gyereke(self, nev:str):
        self.jelenlegi=self.jelenlegi.get_mappa_file(nev)
        return self.jelenlegi










