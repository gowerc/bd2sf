


import unittest
from bd2sf import manager

class TestLinkManager(unittest.TestCase):
    
    def setUp(self):
        man = manager.linkManager()
        man.register_page("preface-to-second-edition.html")
        man.register_page("ch-introduction.html")
        man.register_page("sec-simplesolutions.html")
        man.register_page("references.html")
        man.register_page("sec-linearnormal.html")
        man.register_page("sec-problem.html")
        man.register_page("index.html")
        man.register_page("ex-sec-simplesolutions.html")
        man.register_page("ex-ch-simplesolutions.html")
        self.man = man
    
    def test_navbarlinks(self):
        self.assertEqual( self.man.convert_link("preface-to-second-edition.html", 100) , "#preface-to-second-edition-1")
        self.assertEqual( self.man.convert_link("ch-introduction.html", 100), "#ch:introduction-2")
        self.assertEqual( self.man.convert_link("sec-simplesolutions.html", 100), "#sec:simplesolutions-3")
        self.assertEqual( self.man.convert_link("ex-sec-simplesolutions.html", 100), "#ex:sec:simplesolutions-8")
        self.assertEqual( self.man.convert_link("ex-ch-simplesolutions.html", 100), "#ex:ch:simplesolutions-9")
        
        
    def test_reference(self):
        self.assertEqual( self.man.convert_link("references.html#ref-VANBUUREN2011B", 100), "#ref-VANBUUREN2011B-4")
        self.assertEqual( self.man.convert_link("references.html#ref-LITTLE2002", 100), "#ref-LITTLE2002-4")

    def test_crossreferences(self):
        self.assertEqual( self.man.convert_link("sec-linearnormal.html#sec:linearnormale", 100), "#sec:linearnormale-5")
        self.assertEqual( self.man.convert_link("sec-problem.html#fig:plotair9", 100), "#fig:plotair9-6")
        self.assertEqual( self.man.convert_link("sec-linearnormal.html#ex-sec-linearnormale", 100), "#ex:sec:linearnormale-5")
        self.assertEqual( self.man.convert_link("sec-linearnormal.html#ex-ch-linearnormale", 100), "#ex:ch:linearnormale-5")
        self.assertEqual( self.man.convert_link("ex-ch-simplesolutions.html#ex-ch-linearnormale", 100), "#ex:ch:linearnormale-9")
        
    def test_internalreferences(self):
        self.assertEqual( self.man.convert_link("#sec:linearnormale", 100), "#sec:linearnormale-100")
        self.assertEqual( self.man.convert_link("#fig:plotair9", 100), "#fig:plotair9-100")
        
    def test_externallinks(self):
        self.assertEqual( self.man.convert_link("www.tno.nl/en/", 100), "https://www.tno.nl/en/")
        self.assertEqual( self.man.convert_link("https://www.tno.nl/en/", 100), "https://www.tno.nl/en/")
        self.assertEqual( self.man.convert_link("https://cran.r-project.org/web/packages/mice/index.html", 100) , "https://cran.r-project.org/web/packages/mice/index.html")
        
    def test_register_length(self):
        self.assertEqual( len(self.man.register), 9)
    
    def test_duplicates_error(self):
        with self.assertRaises( KeyError ):
            self.man.register_page("index.html")
    
    def test_retrieval(self):
        self.assertEqual( self.man.get_page_index("index.html"), 7)
        self.assertEqual( self.man.get_page_index("indexxx.html"), 99999)
    
if __name__ == '__main__':
    unittest.main()




