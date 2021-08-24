import xmltodict
import json
from datetime import datetime



def parse_XML(xml_file): 
    """ 
        Parser un fichier xml en un objet json
        Pour l'envoyer ensuite dans elasticsearch
    """
    with open(xml_file, 'r') as myfile:
        obj = xmltodict.parse(myfile.read())
    print(json.dumps(obj))

def fomat_date(data):
    datetimeobject = data.strptime(oldformat,'%Y%m%d%H%M%S')
    return  datetimeobject.strftime('%Y-%m-%d-%H-%M')


def main():
    with open('HOST18_pmresult_1911619733_5_202106080845_202106080850.xml', '+r') as myfile:
        obj = xmltodict.parse(myfile.read())
        print(json.dumps(obj, indent=4))
        print("----------")


if __name__ == '__main__':
    main()


if __name__ == 'main':
    main()
        