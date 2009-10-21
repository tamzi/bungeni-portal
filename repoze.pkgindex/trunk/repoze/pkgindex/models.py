import os

import operator

from zope.interface import implements
from zope.interface import Interface, Attribute
from sets import Set
from string import digits



class IDirectory(Interface):
    items = Attribute(
        """Return directory listing as (name, obj).""")

class Package(object):
    def __init__(self,path):
        self.path = path

class Directory(object):
    """Package directory listing.
    
    For each file - package name, version number and location are
    extracted. Sub-directories are traversed.
    """

    implements(IDirectory)

    __parent__ = __name__ = None
    
    def __init__(self, path):
        self.path = os.path.abspath(os.path.normpath(path))
        
    def items(self):
        parentitems = []
        items = []
        for filename in os.listdir(self.path):
            fname, ext = os.path.splitext(filename)
            if ext in ('.jar', '.egg', '.gz', '.tgz', '.zip'):
                pkg_name = fname.rsplit('-', 1)[0]
                if '.' in pkg_name:
                    for c in pkg_name:
                        if c in digits: 
                            pkg_name = pkg_name.rsplit('-', 1)[0]
                if pkg_name not in parentitems:
                    parentitems.append((pkg_name))
                    item = Versions(self.path, pkg_name)
                    name = pkg_name
            elif os.path.isdir(os.path.join(self.path, fname)):
                item = Directory(os.path.join(self.path, fname))
                name = fname
            else:
                continue
            items.append((name, item))
            item.__name__ = name
            item.__parent__ = self
        items = list(Set(items))       
        return sorted(items, key=operator.itemgetter(0))

    def __getitem__(self, key):
        return dict(self.items())[key]

class Versions(Directory):
    """File name and version listing

    Is called by a directory listing.
    """
    implements(IDirectory)

    def __init__(self, path, pkg_name):
        self.path = path
        self.pkg_name = pkg_name

    def items(self):
        items = []
        for filename in os.listdir(self.path):
            if filename.startswith(self.pkg_name +'-'):
                path = os.path.join(self.path, filename)
                item = Package(path)
                item.__name__ = filename
                item.__parent__ = self
                items.append((filename, item))      
        return sorted(items, key=operator.itemgetter(0))
