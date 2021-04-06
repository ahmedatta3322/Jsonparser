from abc import ABCMeta ,abstractmethod
#define the main abstraction class
class IConvert(metaclass=ABCMeta):
    @abstractmethod
    def convert():
        return "abstract"
    
#define the XML parsing class
class XmlParser(IConvert):
    def __init__(self):
        print('xml')
        pass
    def convert(self):
        pass
#define the CSV parsing class       
class CsvParser(IConvert):
    def __init__(self):
        print('csv')
        pass
    def convert(self):
        pass
#define the main creator of the Json "factory" 
class JsonCreator:
    @staticmethod
    def convert_to_json(thetype):
        if thetype == 'xml':
            return XmlParser()
        elif thetype == 'csv':
            return CsvParser()
        else :
            return None
Parseresult = JsonCreator.convert_to_json(input())