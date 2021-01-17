
from bd2sf import book 
from bd2sf.tools import localsite

import importlib
importlib.reload(book)
importlib.reload(localsite)


book1 = book.book("https://stefvanbuuren.name/fimd/")
book1.build_book()
book1.write("./books/fimd.html")


book2 = book.book("https://r4ds.had.co.nz/")
book2.build_book()
book2.write("./books/r4ds.html")


book3 = book.book("https://serialmentor.com/dataviz/")
book3.build_book()
book3.write("./books/dataviz.html")


book4 = book.book("https://geocompr.robinlovelace.net/")
book4.build_book()
book4.write("./books/geocomp.html")


book5 = book.book("https://bookdown.org/yihui/rmarkdown/")
book5.build_book()
book5.write("./books/markdown.html")



localsite.site("https://r4ds.had.co.nz/", "./local/r4ds")
localsite.site("https://stefvanbuuren.name/fimd/", "./local/fimd")


