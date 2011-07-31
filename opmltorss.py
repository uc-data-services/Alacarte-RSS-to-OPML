from xml.etree.ElementTree import Element, SubElement, Comment, tostring, ElementTree
from xml.etree import ElementTree
from xml.dom import minidom
import datetime
import urllib2
import re 

generated_on = str(datetime.datetime.now())

# Configure one attribute with set()
root = Element('opml')
root.set('version', '1.0')

root.append(Comment('Generated by Tim Dennis'))

head = SubElement(root, 'head')
title = SubElement(head, 'title')
title.text = 'UC Berekeley Guides'
dc = SubElement(head, 'dateCreated')
dc.text = generated_on
dm = SubElement(head, 'dateModified')
dm.text = generated_on

body = SubElement(root, 'body')

def write_xml(elem):
    """Write out a pretty print xml doc to file.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    with open('ucb-guides-feeds.xml', mode='w') as a_file:
        a_file.write(reparsed.toprettyxml(indent=" "))
       
feed_base_url = 'http://lib.berkeley.edu/alacarte/srg/feed/'
guide_base_url = 'http://lib.berkeley.edu/alacarte/subject-guide/'
response = urllib2.urlopen('http://lib.berkeley.edu/alacarte/subject-guides')
html = response.read()
subject_urls = set(re.findall('/subject-guide/(.*?)".*?>(.*?)</a>', html))
current_group = SubElement(body, 'outline', {'text':'Subject Guides'})
for url, title in subject_urls:
    podcast = SubElement(current_group, 'outline',
                             {'text': title,
                              'xmlUrl':feed_base_url+url,
                              'htmlUrl':feed_base_url+url,
                              })
      
