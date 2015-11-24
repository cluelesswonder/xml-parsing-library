
#import lxml or install from: http://lxml.de/installation.html
try:
    from lxml import etree
    print "running with lxml.etree"
except ImportError:
    try:  # Python 2.5
        import xml.etree.cElementTree as etree
        print "running with cElementTree on Python 2.5+"
    except ImportError:
        try:  # Python 2.5
            import xml.etree.ElementTree as etree
            print "running with ElementTree on Python 2.5+"
        except ImportError:
            try:  # normal cElementTree install
                import cElementTree as etree
                print "running with cElementTree"
            except ImportError:
                try:  # normal ElementTree install
                    import elementtree.ElementTree as etree
                    print "running with ElementTree"
                except ImportError:
                    print "Failed to import ElementTree from any known place"


class configXML(object):
    """configures selected xml file with lxml module"""
    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
        self.F = open(xmlfile)
        self.tree = etree.parse(self.F)  # represents XML document in tree form
        self.root = self.tree.getroot()

    def key_check(self, key):
        """checks for existence of passed key"""
        if self.tree.find(key) is None:
            print "NULL"
            return 1
        else:
            return -1

    def getConfigValue(self, key):
        """returns existing key - value pairs or ''
        if <key /> or NULL if key doesn't exist"""
        self.key = key
        if self.key_check(key) < 1:
            for element in self.tree.getiterator(key):
                if element.text is None:
                    element.text = ""
                    print element.tag, '-', element.text
                    return
                else:
                    print element.tag, '-', element.text
                    return
                return
        else:
            return

    def setConfigValue(self, key, value=None):
        """returns NULL if key doesn't exist, returns -1
        if no value and none is written, returns 1
        if new value is written over existing value """
        self.key = key
        self.value = value
        if self.key_check(key) < 1:
            for element in self.tree.getiterator(key):
                if value:
                    element.text = value
                    self.tree.write(self.xmlfile, pretty_print=True)
                    print 1
                    return
                else:
                    element.text = None
                    self.tree.write(self.xmlfile, pretty_print=True)
                    print -1
                    return
        else:
            return

    def createConfigKey(self, key, value=None):
        """creates new <key>value</key>, returns
        NULL if already exists, positive number
        if created. Negative if fails"""
        self.key = key
        self.value = value
        if self.tree.find(key) is not None:
            print "NULL"
            return
        else:
            k = etree.SubElement(self.root, key)
            k.text = value
            self.tree.write(self.xmlfile, pretty_print=True)
            print 'Added:', key, '-', value, 'to the xml file'
            return
        return

    def removeConfigKey(self, key):
        """if key exists: removes and returns positive number, else returns
        NULL"""
        self.key = key
        if self.key_check(key) < 1:
            for unwanted in self.tree.getiterator(key):
                unwanted.getparent().remove(unwanted)
                #removed = etree.tostring(self.tree, pretty_print=True)
                self.tree.write(self.xmlfile, pretty_print=True)
                print "Written to the xml file"
        else:
            return

PATH = raw_input("Enter path to file: ")

myxmlfile = configXML(PATH)

mykey = myxmlfile.getConfigValue("installdir")
mykey = myxmlfile.getConfigValue("localftpuser")

result = myxmlfile.setConfigValue("dateformat", "yyyy-dd-mm")

created = myxmlfile.createConfigKey("installdir", "D:\_application\/")
created = myxmlfile.createConfigKey("date", "10/27/2014")

kill = myxmlfile.removeConfigKey("dropfolder")

