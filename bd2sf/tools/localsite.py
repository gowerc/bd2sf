import requests
import os
import errno
from lxml import html
import re


class site(object):
    
    def __init__(self, site, outdir):
        
        self.site = site
        self.outdir = outdir
        
        request_url = site 
        print("Getting {}".format(request_url))
        resp = requests.get(request_url)
        resp.raise_for_status()
        
        self.site_html = html.fromstring(resp.content.decode("utf-8"))
        
        links = self.site_html.xpath("//a/@href")
        links.append("index.html")
        
        pages =  list(set([ self.correct_link(i) for  i in links if not (i.startswith("http") or i == "./")]))
        self.pages = [ page(i, self.site, self.outdir) for i in pages]
    
    def correct_link(self, link):
        link = re.sub("\#.*$", "", link)
        return link
    
    def write(self, filename, bits):
        filename = self.outdir + "/" + filename
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
            
        with open(filename, "wb") as f:
            f.write(bits)



class page(site):
    def __init__(self, page, site, outdir):
        self.page = page
        self.site = site
        self.outdir = outdir
        
        request_url = site + "/" + page
        print("Getting {}".format(request_url))
        resp = requests.get(request_url)
        resp.raise_for_status()
        
        self.page_html = html.fromstring(resp.content.decode("utf-8"))
        
        if page == "index.html":
            self.get_css()
            self.get_scripts()
        
        self.fix_img()
        self.write( page,  html.tostring(self.page_html))
        
        
    def get_scripts(self):
        scripts = self.page_html.xpath("//script/@src")
        for i in scripts:
            if not (i.startswith("http") or i == ""):
                request_url = self.site + "/" + i
                print("Getting {}".format(request_url))
                resp = requests.get(request_url)
                self.write(i, resp.content)
    
    def get_css(self):
        css = self.page_html.xpath("//link[@rel='stylesheet']/@href")
        for i in css:
            if not (i.startswith("http") or i == ""):
                request_url = self.site + "/" + i
                print("Getting {}".format(request_url))
                resp = requests.get(request_url)
                self.write(i, resp.content)
    
    def fix_img(self):
        imgs = self.page_html.xpath("//img")
        for i in imgs:
            src = i.attrib["src"]
            if not (src.startswith("http") or src == ""):
                i.set("src", "{}/{}".format(self.site , src))










