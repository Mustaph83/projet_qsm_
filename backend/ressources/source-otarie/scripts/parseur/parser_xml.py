import xmltodict
import json



def parse_XML(xml_file): 
    """ 
        Parser un fichier xml en un objet json
        Pour l'envoyer ensuite dans elasticsearch
    """
    with open('data.xml', 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
    print(json.dumps(obj))


def main():
    parse_XML(r'.\HOST18_pmresult_117490525_5_202106080050_202106080055.xml')
        