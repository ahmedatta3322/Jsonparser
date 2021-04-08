# Jsonparser

Jsonparser is a python script to parse XML , CSV data to Json data 

# Install Requirments : 
```bash
pip install -r requirements.txt
```
# Orginazing your input files :
put all csv files you want to parse in input_data/csv 
or 
put all xml files you want to parse in input_data/xml 

# Usage 
for CSV 
```bash
python parser.py csv <customers file> <vehicles file>
```
for XML 
```bash
python parser.py csv <XML file>
```
# Main design pattern
this script build mainly based on factory design patterm . 
