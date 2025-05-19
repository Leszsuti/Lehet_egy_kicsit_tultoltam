import os
import shutil
import unittest
from main_projekt.blokkolo import Blokkolo
from main_projekt.mappaszerkezet import Mappa


class TestBlokkolo(unittest.TestCase):
    def setUp(self):
        try:
            os.mkdir("mappa")
            os.chdir("mappa")
            for i in range(4):
                os.mkdir("mappa"+str(i))
            os.chdir("mappa0")
            for i in range(2):
                with open(f"file{i}.txt", "w") as f:
                    f.write(f"{i} szoveg")
            os.chdir("..")
            os.chdir("mappa2")
            for i in range(3):
                with open(f"file{i}.txt", "w") as f:
                    f.write(f"{i} szoveg")
            os.chdir("..")
            with open(f"file{0}.txt", "w") as f:
                f.write(f"{0} szoveg")
            os.chdir("..")
        except FileExistsError:
            pass
    def tearDown(self):
        pass
        #shutil.rmtree("mappa")

    def test_blokkolo(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        blokkolo = Blokkolo(mappa)
        blokkolo.change_aktiv("0")
        self.assertEqual(blokkolo.to_string(),['0', '  0/0', '  0/1', '  0/2', '  0/3'])
    def test_blokkolo_html(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        blokkolo = Blokkolo(mappa)
        blokkolo.change_aktiv("0")
        blokkolo.change_aktiv("0/2")
        lista=blokkolo.html()
        t=[]
        for i in lista:
            t.append(i.get_nev())
        self.assertEqual(t,[
         '📁mappa',
         '📁mappa0',
         '📁mappa1',
         '📁mappa2',
         '📄file0.txt',
         '📄file1.txt',
         '📄file2.txt',
         '📁mappa3',
         '📄file0.txt'])

    def test_change_aktiv(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        blokkolo = Blokkolo(mappa)
        blokkolo.change_aktiv("0")
        blokkolo.change_aktiv("0/2")
        to_str_1 = blokkolo.to_string()
        blokkolo.change_aktiv("0")
        to_str_2 = blokkolo.to_string()
        self.assertTrue(len(to_str_2) < len(to_str_1))

    def test_get_blokk(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        blokkolo = Blokkolo(mappa)
        blokkolo.change_aktiv("0")
        blokkolo.change_aktiv("0/0")
        blokk = blokkolo.foblokk.get_blokk("0/0")
        self.assertIsNotNone(blokk)
        self.assertEqual(blokk.id, "0/0")

    def test_trio_repr(self):
        from main_projekt.blokkolo import Trio
        trio = Trio(nev="test", fileok=[], id="1", melyseg=2, isfile=False)
        self.assertEqual(trio.get_nev(), "📁test")
        self.assertEqual(trio.get_space(), "        ")
        self.assertEqual(trio.get_id(), "1")
        self.assertFalse(trio.is_file())

if __name__ == "__main__":
    unittest.main()