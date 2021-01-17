import requests
from lxml import html

class page(object):
    
    def __init__(self, li, source, manager):
        self.manager = manager
        self.source = source
        self.li = li
        self.li_a = li.xpath("./a")[0]
        self.link = self.li_a.attrib["href"]
        
        page_link = self.source + self.link
        print("Getting " + page_link)
        resp = requests.get(page_link)
        resp.raise_for_status()
        
        self.content_full = html.fromstring(resp.content.decode("utf-8"))
        self.page_content = self.content_full.xpath("//div[@class='page-inner']")[0]
        self.index = manager.get_page_index(self.link)
        
        for child in li.xpath(".//ul/li"):
            child.attrib["hidden"] = ""
        
        self.set_unique_links()
        self.identify_children()
        self.fix_inner_children()
        
        
    def identify_children(self):
        children_list = self.li.xpath("./ul/li")
        self.outer_children = []
        self.inner_children = []
        for child_id,child in enumerate(children_list):
            child_page = child.xpath("./a/@href")[0]
            if ".html#" in child_page:
                self.inner_children.append( [child_id,child] )
            else:
                self.outer_children.append(child)
        assert self.inner_children == [] or self.outer_children == []
        
        
    
    def set_unique_links(self):
            all_ids = self.page_content.xpath("//*[@id]")
            for id in all_ids:
                id.set("id" ,  "{}-{}".format(id.attrib["id"], self.index)) 
            
            all_as = self.page_content.xpath("//a")
            for a in all_as:
                a.set("data-index", "{}".format(self.index))
            
            sect = self.page_content.xpath("./section")[0]
            
            sect.set("id", "page-{}".format(self.index))
            self.li_a.set("href", "#page-{}".format(self.index))
            
            self.li.set("data-link-index", "p{}".format(self.index))
            self.page_content.set("data-link-index", "p{}".format(self.index))
    
    
    def fix_inner_children(self):
        
        if self.inner_children == []:
            return
        
        for child_index,child in self.inner_children:
            
            sub_children = [child] + child.xpath(".//ul/li")
            
            for sub_index, sub_child in enumerate(sub_children):
                sub_child_page = sub_child.xpath("./a/@href")[0]
                sub_child_page_fix = self.manager.convert_link(sub_child_page, self.index).replace("#", "")
                
                div = self.page_content.xpath("//div[@id='{}']".format(sub_child_page_fix))[0]
                
                sub_child.set("data-link-index", "p{}-{}-{}".format(self.index, child_index, sub_index))
                div.set("data-link-index", "p{}-{}-{}".format(self.index, child_index, sub_index))
                
    def get_children_list(self):
        return self.outer_children


