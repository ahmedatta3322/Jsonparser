from abc import ABCMeta ,abstractmethod
import sys , json , xmltodict , csv
import xml.etree.ElementTree as ET
#define the main abstraction class
##################################
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
#############################
#############################
#############################
class XmlParser(IConvert):
    #define the inputs and jsonexport 
    def __init__(self,file):
        self.file = file
        self.jsoncontent = {}
    #import the data and parse it to dict
    def importdata(self):
        xmlcontent = open(self.file).read()
        self.jsoncontent = xmltodict.parse(xmlcontent) 
    #convert the dict to json
    def convert(self):
        self.importdata()
        self.jsoncontent['file_name'] = str('xml/' + self.file)
        #convert main fields to small case
        self.jsoncontent['transaction'] ,self.jsoncontent['transaction']["customer"] ,self.jsoncontent['transaction']["date"] , self.jsoncontent['Transaction']['Customer']['id'] = self.jsoncontent['Transaction'] , self.jsoncontent['Transaction']['Customer'] ,self.jsoncontent['Transaction']["Date"],self.jsoncontent['Transaction']['Customer']['@id']
        #convert unites to vehicles list 
        self.jsoncontent['transaction']["vehicles"] = []
        for key,value in self.jsoncontent['transaction']['Customer']['Units'].items():  
            if(isinstance(value,dict)):
                value['id'] ,value['make'] ,value['vinNumber'] = value['@id'] , value['Make'] ,value['VinNumber']
                del value['@id'] , value['VinNumber'] , value['Make']
                self.jsoncontent['transaction']["vehicles"].append(dict(value))
            #Deal with list of vehicles
            elif(isinstance(value,list)):
                for element in value:
                    element['id'] ,element['make'] ,element['vinNumber'] = element['@id'] , element['Make'] ,element['VinNumber']
                    del element['@id'] , element['VinNumber'] , element['Make']
                    self.jsoncontent['transaction']["vehicles"].append(dict(element))
        del self.jsoncontent['Transaction'] , self.jsoncontent['transaction']['Customer']['Units'] , self.jsoncontent['transaction']['Customer'] ,self.jsoncontent['transaction']["Date"],self.jsoncontent['transaction']['customer']['@id']
    #Export converted json
    def exportdata(self):
        self.convert()
        out_file = open("parsing_result/sample.json", "w")
        res = json.dump(self.jsoncontent,out_file)      
#define the CSV parsing class      
# #############################
# #############################
# ############################# 
class CsvParser(IConvert):
    def __init__(self,cfile,vfile):
        #define the inputs , vfile for vehicles , cfile for customers , jsonexport
        self.cfile = cfile
        self.vfile = vfile
        self.jsonexport = {}
        self.customer = {}
        self.vehicles = []
        self.date = ''
        self.transactions = []
    def importdata(self):
        self.jsonexport['file_name'] = str('csv/' + self.cfile + 'csv/' + self.vfile)
        #self.jsonexport['transactions'] = self.transactions
    def convert(self):
        self.importdata()
        with open(self.cfile) as custcontent:
            cust_reader = csv.reader(custcontent, delimiter = ',')
            cust_reader.__next__()
            #headers = next(cust_reader)
            for row in cust_reader:
                self.customer = {'id': row[0], 'name':row[1],'address':row[2],'phone':row[3]}
                self.transactions.append({'vehicles':self.vehicles,'customer':self.customer,'date':row[4]})
        with open(self.vfile) as vehicontent:
            vehi_reader = csv.reader(vehicontent, delimiter = ',')
            vehi_reader.__next__()
            arr = []
            for el in vehi_reader:
                arr.append(el)
            for transaction in self.transactions:
                data = []
                for row in arr:
                    if (transaction["customer"]['id'] == row[3]):
                        data.append({'id':row[0],'make':row[1],'vinNumber':row[2]})
                transaction['vehicles'] = data
        self.jsonexport['transactions'] = self.transactions
    def exportdata(self):
        self.convert()
        out_file = open("parsing_result/sample.json", "w")
        res = json.dump(self.jsonexport,out_file)
#define the main creator of the Json "factory" 
#############################
#############################
#############################
class JsonCreator:
    @staticmethod
    def convert_to_json(thetype):
        if thetype == 'xml':
            #pass the files from the cml
            return XmlParser("input_data/xml/" + sys.argv[2]).exportdata()
        elif thetype == 'csv':
            #pass the files from the cml
            return CsvParser("input_data/csv/" + sys.argv[2],"input_data/csv/" + sys.argv[3]).exportdata()
        else :
            return None
if __name__ == "__main__":
    Parseresult = JsonCreator.convert_to_json(sys.argv[1])
