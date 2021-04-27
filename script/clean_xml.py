from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import json
import pandas as pd
import xml.etree.ElementTree as ET
import re
import pprint



def match_xml(file):
    # build regex that matches xml element
    # xml_element = start_tag <anything> end_tag
    #             | self_close_tag
    xml_element = '(?xs) {start_tag} (?(self_close) |.*? {end_tag})'

    # start_tag = '<' name  *attr '>'
    # self_close_tag = '<' name *attr '/>'
    ws = r'[ \t\r\n]*'  # whitespace
    start_tag = '< (?P<name>{name}) {ws} (?:{attr} {ws})* (?P<self_close> / )? >'
    end_tag = '</ (?P=name) >'
    name = '[a-zA-Z]+'  # note: expand if necessary but the stricter the better
    attr = '{name} {ws} = {ws} "[^"]*"'  # match attribute
                                        #  - fragile against missing '"'
                                        #  - no “'” support
    assert '{{' not in xml_element
    while '{' in xml_element: # unwrap definitions
        xml_element = xml_element.format(**vars())

    # extract xml from stdin
    with open(file, 'r') as f:
        all_text = f.read()
    for m in re.finditer(xml_element, all_text):
        print("start: {span[0]}, end: {span[1]}, xml: {begin}{xml}{end}".format(
                span=m.span(), xml=m.group(), begin="{{{", end="}}}"))
        with open('/home/mustaph/Documents/projet_QSM/data/test.xml', 'a+') as te:
            te.write(str(m.span()))

def replce_xml(filepath):
    with  open(filepath, 'r+') as file:
        data = file.read()
        data = re.sub('(&lt;)', '<',data)
        data = re.sub('(&gt;)', '>',data)
    with open(filepath, 'w+') as file:
        file.write(data)
    #match_xml(filepath)        
        

def split_line(filepath):
    data = ''
    with open(filepath, 'r+') as file:
        lines = file.readline()
        outside_tags = []
        for line in lines:
            data += ''+isXml_tag(line)
    with open('/home/mustaph/Documents/projet_QSM/data/test.xml', 'a+') as te:
            te.write(data)
                
                #outside_tags.append(line.split(' '))
    #return outside_tags
       
    
def isXml_tag(lines):
    ws = r'[ \t\r\n]*'
    start_tag = '< (?P<name>{name}) {ws} (?:{attr} {ws})* (?P<self_close> / )? >'
    end_tag = '</ (?P=name) >'
    name = '[a-zA-Z]+'  
    attr = '{name} {ws} = {ws} "[^"]*"'
    xml_element = '(?xs) {start_tag} (?(self_close) |.*? {end_tag})'
    data = ''
    assert '{{' not in xml_element
    while '{' in xml_element: # unwrap definitions
        xml_element = xml_element.format(**vars())
    for m in re.finditer(xml_element, lines):
        data = m.group()
    return data
def main():
    match_xml('../data/uipMsg.log.2021-04-09-48')
    #print(listev)

if __name__ == '__main__':
    main()