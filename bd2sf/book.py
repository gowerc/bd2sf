import re
import requests
from .page import page
from .manager import linkManager
from lxml import html
import base64
import os


class book(object):
    """Abstract book class
    
    Primary class used to encapsulate all functionality for converting a bookbown
    website into a single html file. 
    
    Args:
        source (str): Website for a bookdown site (e.g. 'https://r4ds.had.co.nz/')
        
    Returns:
        desc
        
    Raises:
        IOError: desc
    """
    
    def __init__(self, source):

        self.source = source
        
        resp = requests.get(source)
        base_full = resp.content.decode("utf-8")
        
        base = html.fromstring(base_full)
        head = base.xpath("//div[@class='page-inner']")[0]
        
        for child in head.xpath("./*"):
            head.remove(child)
        
        self.book = base
        self.book_content = head
        
        # some IDs are re-occour across multiple pages.  We thus register each distinct page
        # To create a unique index value. This will be used later to adjust the IDs to ensure that the
        # complete book still contains unique IDs
        self.manager = linkManager()
        for page in set(["index.html"] + self.book.xpath("//ul/li[contains(@class,'chapter')]/a/@href")):
            self.manager.register_page(page)
    
    
    def build_book(self, embed_images = True, embed_styles = True, remove_scripts = True, add_navbar_js = True):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        
        chapter_list = self.get_chapter_list()
        
        for li in chapter_list:
            page = self.get_page(li)
            self.add_page_to(page.page_content, self.book_content)
        
        self.update_links()
        
        if embed_styles:
            self.embed_styles()
        
        if remove_scripts:
            self.remove_scripts()
        
        if embed_images:
            self.embed_images()
        
        if add_navbar_js:
            self.add_navbar_js()
        
        self.remove_html_widgets()
        self.remove_next_page_button()
    
    
    def write(self,out):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        with open( out, "wb") as fi:
            fi.write(html.tostring(self.book))
    
    
    def add_navbar_js(self):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        this_dir, this_filename = os.path.split(__file__)
        file_path = os.path.join(this_dir, "js", "navbar.js")
        
        with open(file_path, "r") as fi:
            navbar = fi.read()
        
        new_script = html.Element("script")
        new_script.text = navbar
        self.book.xpath("//head")[0].insert(1, new_script)
        
        ## Add jquery library
        new_script = html.Element("script")
        new_script.attrib["src"] = "https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"
        self.book.xpath("//head")[0].insert(1, new_script)
    
    
    def remove_next_page_button(self):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        self.book.xpath("//a[contains(@class, 'navigation-next')]")[0].clear()
    
    
    
    def remove_html_widgets(self):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        ### Currently unsure how to support html-widgets so as a simple solution
        ### I am just removing them
        for i in self.book.xpath("//div[contains(@class, 'html-widget')]"):
            print("Unsupported widget removed")
            i.clear()
    
    
    
    def add_page_to( self, content, dest):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        index = len(dest.xpath("./*"))
        dest.insert(index + 1, content)
    
    
    def get_chapter_list(self):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        chapters = self.book.cssselect("ul[class = 'summary'] > li.chapter")
        # Some books have a "welcome" or "preface" chapter in the navbar which is the index page
        # If this is not included (i.e. no links back to the index page in the navbar) then include one
        if not chapters[0].xpath("./a/@href")[0] == "index.html":
            chapters = self.add_index_page(chapters)
        return chapters
     
    
    def get_page(self, li):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        page_ob = page(li, self.source, self.manager)
        for child_li in page_ob.get_children_list():
            child_page = self.get_page(child_li)
            self.add_page_to(child_page.page_content, page_ob.page_content)
        return page_ob
    
    
    def get_remote_content(self, path):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        if path.startswith("http"):
            page_path = path
        elif path.startswith("www"):
            page_path = "https://" + path
        else:
            page_path = self.source + path
            
        print("Getting " + page_path)
        
        try:
            resp = requests.get(page_path)
        except:
            print("Unable to get " + page_path)
            return None
        
        if resp.status_code == 200:
            return resp.content
        else:
            print("Unable to get " + page_path + " Response = " + str(resp.status_code))
            return None
    
    
    def add_index_page(self, chapters):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        e_a = html.Element("a")
        e_li = html.Element("li")
        e_a.attrib["href"] = "index.html"
        e_li.insert(1,e_a)
        chapters = [e_li] + chapters
        return chapters
    
    
    
    def embed_images(self):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        for img in self.book.xpath("//img[ not(starts-with(@src, 'data:')) and @src!= '']"):
            img_src =  img.attrib["src"]
            img_raw = self.get_remote_content(img_src)
            if img_raw != None:
                img_64 = base64.b64encode(img_raw)
                file_info = os.path.splitext(img_src)
                ext = file_info[1].replace(".", "")
                ext = re.sub("\?.*$", "" , ext)
                
                if ext == "svg":
                    svg = html.fromstring(img_raw.decode("utf-8"))
                    img.clear()
                    img.tag = "svg"
                    img[:] = [svg]
                else:
                    img.set("src",  "data:image/{};base64,{}".format(ext, img_64.decode("utf-8")))
                    
    
    def embed_styles(self):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        for style in self.book.xpath("//link[@rel='stylesheet']"):
            style_raw = self.get_remote_content(style.attrib["href"])
            if style_raw != None:
                style_content = style_raw.decode("utf-8")
                new_style = html.Element("style")
                new_style.attrib["type"] = "text/css"
                new_style.text = style_content 
                style.xpath("//head")[0].insert(0, new_style)
                style.getparent().remove(style)
    
    
    def remove_scripts(self):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        for script in self.book.xpath("//script"):
            delete_me = True
            try:
                src = script.attrib["src"]
                if src.startswith("http") | src.startswith("www."):
                    delete_me = False
            except KeyError:
                pass
            if delete_me:
                script.getparent().remove(script)
    
    
    def update_links(self):
        """short desc
        
        long desc
    
        Args:
            var (type): desc
    
        Returns:
            desc
    
        Raises:
            IOError: desc
        """
        for a in self.book.xpath("//a[@href]"):
            href = a.xpath("@href")[0]
            index_list = a.xpath("@data-index")
            
            ### If there is no data-index it is assumed link comes from initial book landing page (the index page)
            if index_list == []:
                index = self.manager.get_page_index("index.html")
            else:
                index = index_list[0]
            
            ### Fix people who are bad at links
            if href.startswith("www."):
                href = "https://" + href
                a.set("href", href)
            
            ## Correct for ambiguity (Naive assumption that this error only occours on index page)
            if href == "./":
                href = "index.html"
            
            if not href:
                return None
            
            href  = self.manager.convert_link(href, index)
            a.set("href", href)

