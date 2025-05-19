
import shutil
import unittest
from main_projekt.mappaszerkezet import *

class TestMappa(unittest.TestCase):
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
        shutil.rmtree("mappa")

    def test_mappa_felepit(self):
        mappa = Mappa(gyoker=None,nev="mappa",utvonal="mappa", github=False)
        mappa.felepit()
        self.assertEqual(mappa.get_mappa("mappa2").get_file("file1.txt").get_utvonal(),"mappa\\mappa2\\file1.txt")

    def test_mappa_listaz(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        mappa.felepit()
        mappa.listaz()
        self.assertEqual(mappa.listaz(), ['mappa0', 'mappa1', 'mappa2', 'mappa3', 'file0.txt'])

    def test_mappa_listaz_all(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        mappa.felepit()
        mappa.listaz()
        self.assertEqual(mappa.listaz_all(), [
            'mappa',
             'mappa0',
             '  file0.txt',
             '  file1.txt',
             'mappa1',
             'mappa2',
             '  file0.txt',
             '  file1.txt',
             '  file2.txt',
             'mappa3',
             'file0.txt'])

    def test_filekezelo(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        filekezelo=Filekezelo(gyoker=mappa,nev="filekezelo")
        self.assertEqual(filekezelo.jelenlegi_gyereke("mappa0").get_nev(),"mappa0")
        self.assertEqual(filekezelo.jelenlegi_gyokere().get_nev(),"mappa")
    def test_filekezelo_utvonal(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        filekezelo=Filekezelo(gyoker=mappa,nev="filekezelo")
        self.assertEqual(filekezelo.utvonal_feldolgozo("mappa2/file0.txt").get_nev(),"file0.txt")

    def test_get_file(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        mappa.felepit()
        mappa2 = mappa.get_mappa("mappa2")
        file = mappa2.get_file("file1.txt")
        self.assertIsNotNone(file)
        self.assertEqual(file.get_nev(), "file1.txt")

    def test_get_mappa_file(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        mappa.felepit()
        self.assertEqual(mappa.get_mappa_file("mappa3").get_nev(), "mappa3")
        self.assertEqual(mappa.get_mappa_file("file0.txt").get_nev(), "file0.txt")

    def test_get_mappa_file_none(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        mappa.felepit()
        self.assertIsNone(mappa.get_mappa_file("nemletezo.txt"))

    def test_jelenlegi_gyokere_is_alap(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        filekezelo = Filekezelo(gyoker=mappa, nev="filekezelo")
        self.assertEqual(filekezelo.jelenlegi_gyokere().get_nev(), "mappa")

    def test_utvonal_feldolgozo_nemletezo(self):
        mappa = Mappa(gyoker=None, nev="mappa", utvonal="mappa", github=False)
        filekezelo = Filekezelo(gyoker=mappa, nev="filekezelo")
        eredmeny = filekezelo.utvonal_feldolgozo("nemletezo/file.txt")
        self.assertIsNone(eredmeny)


if __name__ == "__main__":
    unittest.main()