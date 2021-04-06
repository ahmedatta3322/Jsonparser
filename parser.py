from abc import ABCMeta ,abstractmethod
import sys
#define the main abstraction class
class IConvert(metaclass=ABCMeta):
    @abstractmethod
    def convert():
        pass
#define the XML parsing class
class XmlParser(IConvert):
    def __init__(self,file):
        #define the inputs
        self.file = file
    def convert(self):
        pass
#define the CSV parsing class       
class CsvParser(IConvert):
    def __init__(self,vfile,cfile):
        #define the inputs , vfile for vehicles , cfile for customers
        self.cfile = cfile
        self.vfile = vfile
    def convert(self):
        pass
#define the main creator of the Json "factory" 
class JsonCreator:
    @staticmethod
    def convert_to_json(thetype):
        if thetype == 'xml':
            #pass the files from the cml
            return XmlParser(sys.argv[2])
        elif thetype == 'csv':
            #pass the files from the cml
            return CsvParser(sys.argv[2],sys.argv[3])
        else :
            return None
if __name__ == "__main__":
    Parseresult = JsonCreator.convert_to_json(sys.argv[1])
