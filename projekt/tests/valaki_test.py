import unittest
import os
from main_projekt.valaki import Valaki

class TestValaki(unittest.TestCase):

    def setUp(self):
        self.v = Valaki(
            neptun_kod="ABC123",
            neptun_jelszo="jelszo1",
            h_azonosito="user",
            h_jelszo="pw",
            github_felhasznalonev="ghuser",
            github_token="token",
            email="email@example.com"
        )

    def test_str(self):
        output = str(self.v)
        self.assertIn("ABC123", output)
        self.assertIn("jelszo1", output)
        self.assertIn("email@example.com", output)

    def test_ment_adat_es_get_adat(self):
        self.v.ment_adat("kulcs", "érték")
        self.assertEqual(self.v.get_adat("kulcs"), "érték")

    def test_get_adat_nem_letezo(self):
        self.assertEqual(self.v.get_adat("nincs"), "")

    def test_minden_adat_meg_van_adva_igaz(self):
        self.assertTrue(self.v.minden_adat_meg_van_adva())

    def test_minden_adat_meg_van_adva_hianyzik(self):
        self.v.email = ""
        self.assertFalse(self.v.minden_adat_meg_van_adva())

    def test_read_txt_sikeres(self):
        with open("valaki.txt", "w") as f:
            f.write("ABC123\njelszo1\nuser\npw\nghuser\ntoken\nemail@example.com\n")
        self.v.read_txt()
        self.assertEqual(self.v.neptun_kod, "ABC123")
        os.remove("valaki.txt")

    def test_read_txt_hibas(self):
        if os.path.exists("valaki.txt"):
            os.remove("valaki.txt")
        self.v.read_txt()
        self.assertEqual(self.v.neptun_kod, "")
        self.assertEqual(self.v.neptun_jelszo, "")
        self.assertEqual(self.v.github_token, "")

if __name__ == "__main__":
    unittest.main()