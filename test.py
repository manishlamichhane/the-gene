from individual import Male, Female
from nature import Nature
import unittest


class TestNatureMethods(unittest.TestCase):

    def test_breedability(self):
        # great great grand parents
        gggp_m = Male(name="gggp_m")
        gggp_f = Female(name="gggp_f")

        # great grand parents
        ggp_m = Male(parents=(gggp_m, gggp_f), name="ggp_m")
        ggp_f = Female(name="ggp_f")

        # great grand uncle
        ggu = Male(parents=(gggp_m, gggp_f), name="ggu")
        gga = Female(name="gga")

        # first cousin twice removed
        fctr = Male(parents=(ggu, gga), name="fctr")

        # grand parents
        gp_m = Male(parents=(ggp_m, ggp_f), name="gp_m")
        gp_f = Female(name="gp_f")

        # great uncle/aunt
        gu = Male(parents=(ggp_m, ggp_f), name="gu")
        ga = Female(name="ga")

        # first cousin once removed
        fcor = Male(parents=(gu, ga), name="fcor")

        # parents
        p_m = Male(parents=(gp_m, gp_f), name="p_m")
        p_f = Female(name="p_f")

        # uncle/aunts
        u1_m = Male(parents=(gp_m, gp_f), name="u1_m")
        u1_f = Female(name="u1_f")

        a1_f = Female(parents=(gp_m, gp_f), name="a1_f")
        a1_m = Male(name="a1_m")

        # first cousins
        fc1_m = Male(parents=(u1_m, u1_f), name="fc1_m")
        fc1_f = Female(name="fc1_f")

        fc2_f = Female(parents=(a1_m, a1_f), name="fc2_f")

        # me ☺️
        me = Male(parents=(p_m, p_f), name="me")
        wife = Female(name="wife")

        brother = Male(parents=(p_m, p_f), name="brother")
        sil = Female(name="sil")

        # my children 😭
        c1_m = Male(parents=(me, wife), name="c1_m")
        c1_f = Female(name="c1_f")

        c2_m = Male(parents=(me, wife), name="c2_m")
        c2_f = Female(name="c2_f")

        # grand children
        gc1_m = Male(parents=(c1_m, c1_f), name="gc1_m")
        gc1_f = Female(name="gc1_f")

        gc2_m = Male(parents=(c2_m, c2_f), name="gc2_m")
        gc2_f = Female(name="gc2_f")

        # great grand children
        ggc1_m = Male(parents=(gc1_m, gc1_f), name="ggc1_m")
        ggc1_f = Female(name="ggc1_f")

        ggc2_m = Male(parents=(gc2_m, gc2_f), name="ggc2_m")
        ggc2_f = Female(name="ggc2_f")

        # great great grand children
        gggc1_m = Male(parents=(ggc1_m, ggc1_f), name="gggc1_m")
        gggc1_f = Female(name="gggc1_f")

        # my brother's

        # niece/nephew
        niece_f = Female(parents=(brother, sil), name="niece_f")
        niece_m = Male(name="niece_m")

        # grand niece/nephew
        grand_niece_f = Female(parents=(niece_m, niece_f), name="grand_niece_f")
        grand_niece_m = Male(name="grand_niece_m")

        # great grand niece/nephew
        ggnephew_m = Male(parents=(grand_niece_m, grand_niece_f), name="ggnephew_m")

        self.assertFalse(Nature.breedable(me, brother))
        self.assertFalse(Nature.breedable(me, niece_f))
        self.assertFalse(Nature.breedable(me, c1_m))
        self.assertFalse(Nature.breedable(me, c1_f))
        self.assertFalse(Nature.breedable(p_m, u1_m))
        self.assertFalse(Nature.breedable(ggp_m, p_m))
        self.assertFalse(Nature.breedable(p_m, ggp_m))
        self.assertFalse(Nature.breedable(p_m, fc1_m))
        self.assertTrue(Nature.breedable(p_f, fc1_m))
        self.assertFalse(Nature.breedable(c1_m, brother))
        self.assertTrue(Nature.breedable(c1_m, niece_f))
        self.assertFalse(Nature.breedable(brother, grand_niece_f))
        self.assertFalse(Nature.breedable(ggp_m, fc1_m))



if __name__ == '__main__':
    unittest.main()
