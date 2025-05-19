import os
import subprocess
from flask import render_template, Blueprint, request
from valaki import Valaki
from github import Github, GithubException
from mappaszerkezet import Mappa,Filekezelo
from main_projekt.blokkolo import Blokkolo

blueprint = Blueprint('github', __name__, url_prefix='/github/')
print("github_view indul: ")
valaki = Valaki()
valaki.read_txt()
print(valaki)
token=valaki.github_token
uzenet:str=""

blokkolo_pre=Blokkolo(Mappa(gyoker=None))
lista_sajat=blokkolo_pre.html()
lista_github=blokkolo_pre.html()
blokkolo:Blokkolo=blokkolo_pre
blokkolo_github:Blokkolo=blokkolo_pre
@blueprint.route('',methods=['GET','POST'])
def github():
    global valaki, uzenet, token, blokkolo, blokkolo_github, lista_sajat, lista_github
    valaki.read_txt()
    print(valaki)
    token = valaki.github_token
    uzenet="Értesítések: "

    if request.method == 'POST':
        gomb = request.form.get('gomb')

        if gomb == 'letrehoz':
            create_repo(request.form['repo_name'])
            valaki.ment_adat(nev="repo_name", ertek=request.form['repo_name'])
            print(f"letrehozva {request.form['repo_name']}")

        if gomb == 'torles':
            delete_repo(request.form['repo_name_delete'])
            print(f"törölve {request.form['repo_name_delete']}")

        if gomb == 'push':
            file_push(path=request.form['push_honnan'],commit_message=request.form['push_message'],repo=request.form['push_repo_name'])
            valaki.ment_adat("push_honnan",request.form['push_honnan'])
            valaki.ment_adat("push_message",request.form['push_message'])
            valaki.ment_adat("push_repo_name",request.form['push_repo_name'])
            print(f"pusholva {request.form['push_repo_name']}")

        if gomb == 'clone':
            clone_repo(path=request.form['clone_path'], url=request.form['clone_url'])
            valaki.ment_adat("clone_path",request.form['clone_path'])
            valaki.ment_adat("clone_url",request.form['clone_url'])
            print(f"cloneolva {request.form['clone_url']}")

        if gomb == 'pull':
            pull_repo(path=request.form['pull_hova'])
            valaki.ment_adat("pull_hova",request.form['pull_hova'])
            print(f"pullolva {request.form['pull_hova']}")

        if gomb == 'gomb_gyoker':
            print("gyomb_gyoker_github")
            try:
                utvonal=request.form['text_gyoker']
                gyoker=Mappa(gyoker=None,nev=utvonal, utvonal=utvonal)
                blokkolo=Blokkolo(mappa=gyoker,nev="gyoker_blokkolo")
                lista_sajat=blokkolo.html()
                valaki.ment_adat("text_gyoker",request.form['text_gyoker'])
            except Exception as e:
                uzenet+=e.__str__()

        if gomb == 'gomb_gyoker_github':
            repo_neve=request.form['repo_neve']
            if repo_neve.__contains__(valaki.github_felhasznalonev):
                pass
            else:
                repo_neve=valaki.github_felhasznalonev + "/" + repo_neve
            print("gyomb_gyoker_github")
            print(repo_neve)
            print(token)
            gyoker=Mappa(gyoker=None,nev=repo_neve, utvonal='github',github=True)
            try:
                gyoker.beolvas_github(token=token,repository=repo_neve)
            except GithubException as e:
                print("github rapo " + e.__str__())
                uzenet += "Nincs ilyen repo"
            gyoker.listaz_all()
            blokkolo_github=Blokkolo(mappa=gyoker,nev="gyoker_blokkolo")
            lista_github=blokkolo_github.html()
            valaki.ment_adat("repo_neve",request.form['repo_neve'])

        aktiv_gomb=request.form.get('change_aktiv')
        if aktiv_gomb is not None:
            blokkolo.change_aktiv(aktiv_gomb)
            lista_sajat=blokkolo.html()

        aktiv_gomb = request.form.get('change_aktiv_github')
        if aktiv_gomb is not None:
            blokkolo_github.change_aktiv(aktiv_gomb)
            lista_github = blokkolo_github.html()







    return render_template('github_view.html', valaki=valaki, uzenet=uzenet, lista=osszes_repo(), mappa=jelenlegi_mappa(), lista_sajat=lista_sajat, lista_github=lista_github)


def create_repo(repo_name:str):
    global token, uzenet

    account = Github(token)
    user = account.get_user()
    print(user)
    try:
        repo = user.create_repo(repo_name, description="leiras",auto_init=True)

        repos = user.get_repos()
        for repo_ in repos:
            print(repo_.name)
        uzenet += f"Repo létrehozva: {request.form['repo_name']}"
        return repo
    except Exception as e:
        print("mar letezik ilyen repo")
        uzenet += "Sikertelen létrehozás"
        # repos = user.get_repos()
        # for repo_ in repos:
        #     print(repo_.name)
        return None

def delete_repo(repo_name:str):
    global token, uzenet
    account = Github(token)
    user = account.get_user()
    try:
        repo = user.get_repo(repo_name)
        repo.delete()
        uzenet += f"Repo törölve: {request.form['repo_name_delete']}"
        print(f"torolve{repo.name}")
    except Exception as e:
        print("nincs ilyen repo")
        uzenet += "Sikertelen törlés"

def file_push(path:str,commit_message:str,repo:str):
    global token, valaki, uzenet
    jelenlegi=jelenlegi_mappa()
    try:
        os.chdir(path)
        hova=""
        if repo.__contains__(valaki.github_felhasznalonev):
            hova=f"https://{token}@github.com/{repo}.git"
        else:
            hova=f"https://{token}@github.com/{valaki.github_felhasznalonev}/{repo}.git"

        def futtass_parancs(parancs: list, leiras: str):
            global uzenet
            eredmeny = subprocess.run(parancs, capture_output=True, text=True)
            if eredmeny.returncode == 0:
                uzenet += f"\n✅ {leiras} sikeres."
            else:
                uzenet += f"\n❌ {leiras} sikertelen:\n{eredmeny.stderr.strip()}"
            return eredmeny

        futtass_parancs(["git", "config", "--global", "user.name", valaki.github_felhasznalonev],"Felhasználónév beállítása")
        futtass_parancs(["git", "config", "--global", "user.email", valaki.email], "Email beállítása")
        futtass_parancs(["git", "remote", "remove", "origin"], "Origin eltávolítása")
        futtass_parancs(["git", "init"], "Repo inicializálása")
        futtass_parancs(["git", "add", "."], "Fájlok hozzáadása")

        commit_result = futtass_parancs(["git", "commit", "-m", commit_message], "Commit")
        if commit_result.returncode != 0:
            uzenet += "\n Lehet, hogy nem történt változás, amit commitolni lehetne."

        futtass_parancs(["git", "branch", "-M", "main"], "Branch átnevezése")
        futtass_parancs(["git", "remote", "add", "origin", hova], "Origin hozzáadása")
        futtass_parancs(["git", "push", "-uf", "origin", "main"], "Push")

        try:
            uzenet += f"\n Repo ({request.form.get('push_repo_name', 'ismeretlen')}) pusholva a {request.form.get('push_honnan', 'ismeretlen')} útvonalról (message: {request.form.get('push_message', 'nincs üzenet')})"
        except:
            uzenet += "\n hiba"


    except Exception as e:
        uzenet += e.__str__()
    finally:
        os.chdir(jelenlegi)

def clone_repo(path:str,url:str):
    global uzenet
    jelenlegi=jelenlegi_mappa()
    try:
        os.chdir(path)
        subprocess.run(["git", "clone", url], check=True)
        uzenet += f"Repo ({request.form['clone_url']}) cloneolva ide: {request.form['clone_path']}"
    except Exception as e:
        print("rossz url")
        uzenet+="Sikertelen clone"
    os.chdir(jelenlegi)

def pull_repo(path:str):
    global uzenet
    jelenlegi=jelenlegi_mappa()
    try:
        os.chdir(path)
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        uzenet += f"Pullolva ide: {request.form['pull_hova']}"
    except Exception as e:
        uzenet += "Sikertelen pull"
    os.chdir(jelenlegi)

def osszes_repo():
    global token
    lista = []
    try:

        account = Github(token)
        user = account.get_user()
        repos = user.get_repos()
        for repo in repos:
            lista.append(repo.name)
    except Exception as e:
        lista.append("Hibás github token!!!")
    return lista

def jelenlegi_mappa():
    return os.getcwd()

def mappa_megjelenites(gyoker_utvonal:str):
    print("mappa_megjelenites...")
    gyoker=Mappa(gyoker=None,nev=gyoker_utvonal,utvonal=gyoker_utvonal)
    filekezelo=Filekezelo(gyoker=gyoker,nev=gyoker_utvonal)
    return filekezelo



# #create_repo("uj repo")
# print("--------------------")
# #file_push(path=r"K:\gites_szar",commit_message="fdbjidfgiub  udf",repo="uj-repo")
# print("--------------------")
# # delete_repo(repo_name="teszt_repo")
# print("--------------------")
# #clone_repo(path=r"K:\ide",url="https://github.com/Leszsuti/uj-repo")
# print("--------------------")
# #pull_repo(path=r"K:\ide\uj-repo")








