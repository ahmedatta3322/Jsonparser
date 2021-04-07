from abc import ABCMeta ,abstractmethod
import sys , json , xmltodict , csv
import xml.etree.ElementTree as ET
#define the main abstraction class
class IConvert(metaclass=ABCMeta):
    @abstractmethod
    def importdata():
        pass
    @abstractmethod
    def convert():
        pass
    @abstractmethod
    def exportdata():
        pass
    
#define the XML parsing class
class XmlParser(IConvert):
    def __init__(self,file):
        #define the inputs
        self.file = file
#import the data and parse it to dict
    def importdata(self):
        xmlcontent = open(self.file).read()
        jsoncontent = xmltodict.parse(xmlcontent) 
        return jsoncontent
#convert the dict to json
    def convert(self):
        jsoncontent = self.importdata()
        jsoncontent['file_name'] = str('xml/' + self.file)
#convert main fields to small case
        jsoncontent['transaction'] ,jsoncontent['transaction']["customer"] ,jsoncontent['transaction']["date"] , jsoncontent['Transaction']['Customer']['id'] = jsoncontent['Transaction'] , jsoncontent['Transaction']['Customer'] ,jsoncontent['Transaction']["Date"],jsoncontent['Transaction']['Customer']['@id']
#convert unites to vehicles list 
        jsoncontent['transaction']["vehicles"] = []
        for key,value in jsoncontent['transaction']['Customer']['Units'].items():  
            if(isinstance(value,dict)):
                value['id'] ,value['make'] ,value['vinNumber'] = value['@id'] , value['Make'] ,value['VinNumber']
                del value['@id'] , value['VinNumber'] , value['Make']
                jsoncontent['transaction']["vehicles"].append(dict(value))
            #Deal with list of vehicles
            elif(isinstance(value,list)):
                for element in value:
                    element['id'] ,element['make'] ,element['vinNumber'] = element['@id'] , element['Make'] ,element['VinNumber']
                    del element['@id'] , element['VinNumber'] , element['Make']
                    jsoncontent['transaction']["vehicles"].append(dict(element))
        del jsoncontent['Transaction'] , jsoncontent['transaction']['Customer']['Units'] , jsoncontent['transaction']['Customer'] ,jsoncontent['transaction']["Date"],jsoncontent['transaction']['customer']['@id']
        return jsoncontent
#Export converted json
    def exportdata(self):
        jsoncontent = self.convert()
        out_file = open("parsing_result/sample.json", "w")
        res = json.dump(jsoncontent,out_file)
          
#define the CSV parsing class       
class CsvParser(IConvert):
    def __init__(self,vfile,cfile):
        #define the inputs , vfile for vehicles , cfile for customers
        self.cfile = cfile
        self.vfile = vfile
    def importdata(self):
        with open(cfile) as csvcontent:
            csv_reader = csv.reader(csvcontent, delimiter = ',')
            for row in csv_reader:
                print(row)
        
    def convert(self):
        pass
    def exportdata(self):
        jsoncontent = self.convert()
        out_file = open("parsing_result/sample.json", "w")
        res = json.dump(jsoncontent,out_file)
#define the main creator of the Json "factory" 
class JsonCreator:
    @staticmethod
    def convert_to_json(thetype):
        if thetype == 'xml':
            #pass the files from the cml
            return XmlParser("input_data/xml/" + sys.argv[2]).exportdata()
        elif thetype == 'csv':
            #pass the files from the cml
            return CsvParser("input_data/csv/" + sys.argv[2],sys.argv[3]).convert
        else :
            return None
if __name__ == "__main__":
    Parseresult = JsonCreator.convert_to_json(sys.argv[1])
