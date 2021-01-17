import re


class linkManager(object):
    
    def __init__(self):
        self.register = {}
        self.index = 0
    
    
    def register_page(self, path):
        path = self.path_fix(path)
        
        if path in self.register:
            raise KeyError("Duplicate entries detected")
        else:
            self.register[path] = self.index + 1
            self.index = self.index + 1
    
    
    def get_page_index(self, path):
        path = self.path_fix(path)
        try:
            index = self.register[path]
        except KeyError as e:
            print( "Bad URL, internal link {} does not exist".format(path))
            index = 99999
        return index
    
    
    def convert_link(self, string, index):
        
        # Ignore www facing links
        if string.startswith("www."):
            string = "https://" + string
        
        if string.startswith("http"):
            return string
        
        if string.startswith("#"):
            if string.startswith("#page-"):
                return string 
            else:
                return "{}-{}".format(string, index)
        
        string = self.path_fix(string)
        
        if re.search("\.html\#", string):
            link = re.sub("\#.*$", "", string)
            index = self.get_page_index(link)
            return re.sub( "^.*\.html", "", string) + "-" + str(index)
        
        index = self.get_page_index(string)
        string = string + "-" + str(index)
        
        string = string.replace(".html", "")
        
        if not string.startswith("#"):
            string = "#" + string
        
        return string
    
    def path_fix(self, path):
        path = re.sub("^ex-ch-", "ex:ch:" , path)
        path = re.sub("^ex-sec-", "ex:sec:" , path)
        path = re.sub("^ch-", "ch:" , path)
        path = re.sub("^sec-", "sec:" , path)
        
        path = re.sub("\#ex-ch-", "#ex:ch:" , path)
        path = re.sub("\#ex-sec-", "#ex:sec:" , path)
        path = re.sub("\#ch-", "#ch:" , path)
        path = re.sub("\#sec-", "#sec:" , path)
        return path
    

