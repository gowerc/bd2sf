# bd2sf

BookDown to SingleFile 


## Introduction

The purpose of this project is to convert bookdown sites into a single portable html file to enable easier 
referencing and lookup during local use.

Note that bookdown does offer a singlefile creation mode using: `bookdown::render_book("index.Rmd", "bookdown::pdf_book2")`. 
However this means you need access to the full source code and source data which isn't always available. If it is however
this approach is likely to be easier and less prone to errors than using this script. 


## Dependencies 

Python 3.7+  
requests  
lxml  

## Usage

```
from bd2sf import book 
book1 = book.book("https://r4ds.had.co.nz/")
book1.build_book()
book1.write("./books/r4ds.html")
```
