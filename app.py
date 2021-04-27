from script import cdr_scp
#from  script import clean_xml
import re
import xml.etree as ET
import pandas as pd
from os import listdir
import argparse
import logging as lg


def parse_arguments():
    arguments = argparse.ArgumentParser()
    arguments.add_argument("-f","--file", help="""si vous voulez
                            importer un fichier ou un repertoir. cette option est obligatoire""")
   
    arguments.add_argument("-s","--sep", help="""Preciser le caractere separateur. 
                            S'il n'est pas indiquer le moteur python le detectera automatiquement""")
    arguments.add_argument('-i', '--index', help="""Preciser les clonnes a prendre exemple [1,2,3...]""")

    arguments.add_argument('-e', '--headers', help="""Preciser le nom des colonnes[service, calling number ...]""")
    
    arguments.add_argument('--skiprows', help="""Cette option est pour indiquer les ligne a ignorer
                            Si le(s) fichier(s) contient une entete il faut mettre cette option a 0""")
    arguments.add_argument('-fe','--file_extension', help="""Preciser l'extension des fichiers
                            Pour lire tout les fichiers d'un repertoire(l'extension par defaut est .o)""")
    return arguments.parse_args()


def main():
    args = parse_arguments()
    try:
        file = args.file
        print(file)
        if file == None:
            raise Warning ('Vous devez indiquer un fichier ou un repertoire')
    except Warning as e:
        lg.warning(e)
    else:
        if args.sep:
            if args.skiprows:
                if not args.index or not args.headers:
                    cdr_scp.create_dataframe(args.file, args.sep, int(args.skiprows))
                else:
                    df = cdr_scp.create_dataframe(file, args.sep, int(args.skiprows))
                    cdr_scp.sub_dataframe(df,args.index, args.headers, int(args.skiprows))
            else:
                if not args.index or not args.headers:
                    cdr_scp.create_dataframe(args.file, args.sep,args)
                else:
                    df = cdr_scp.create_dataframe(file, args.sep)
                    cdr_scp.sub_dataframe(df,args.index, args.headers)
        else :
            if args.skiprows:
                if not args.index or not args.headers:
                    print(type(args.skiprows))
                    cdr_scp.create_dataframe(args.file,skiprows=int(args.skiprows))
                else:
                    cdr_scp.create_dataframe(args.file)
            else:
                if not args.index or not args.headers:
                    cdr_scp.create_dataframe(args.file)
                else:
                    raise Warning("Ne pas creer le dataframe le separateur n'est pas preciser")

    finally:
        print("################# Succesfful ########################")







    #file = r'./data/in205141_G_12_226873_20210412.o'
    #path = ''
    #parser = ET.XMLParser(recover=True)
    #tree = ET.parse('./data/test.xml', parser=parser)

    #for name in tree.iter('name'):
     #   print(tree.tag, name.text)
    #data = cdr_scp.create_dataframe(file)
    #clean_xml.replce_xml(file)
    #clean_xml.match_xml(file)
    #clean_xml.delate_header('./data/test.xml')
    #clean_xml.iter_node('./data/test.txt')
if __name__ == '__main__':
    main()
    