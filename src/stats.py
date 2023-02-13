# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 10:49:23 2022

@author: reema
"""



import json
import sys 
from lxml import etree





script_name = sys.argv[0]
file = sys.argv[1]
jsonfile = sys.argv[2]




tree = etree.parse(file)
# tree = ET.parse('fsimage564.xml')
root = tree.getroot()
# numBy = tree.findall("./INodeSection/inode/blocks/numBytes")

filecount = 0
dircount = 0
for child in root:
    for inodee in child:
        for ch in inodee:
            if ch.text == 'FILE':
                filecount +=1
            if ch.text == 'DIRECTORY':
                dircount +=1

if filecount > 0:
    maxFileSize = 0
    minFileSize = -1
    for i in tree.xpath("//inode[type='FILE']/blocks/block/numBytes"):
        fileSize = int(i.text)
        if minFileSize == -1 or fileSize < minFileSize:
            minFileSize = fileSize
        if fileSize > maxFileSize:
            maxFileSize = fileSize

def get_depth(d, numlevel):
    numlevel += 1
    
    NoupcomingLevel = True
    children = d.xpath("./child")
    for child in children:
        nextLevel = d.xpath("../directory[parent='" + child.text + "']")
        if len(nextLevel) > 0:
            NoupcomingLevel = False
            return get_depth(nextLevel[0], numlevel)
    
    # Add 1 more depth level when the deepest level has no children containing children
    if len(children) > 0 and NoupcomingLevel:
        numlevel += 1
    
    return numlevel
maxDepth = 0
for i in tree.xpath("//INodeDirectorySection/directory"):
    depth = get_depth(i, 0)
    if depth > maxDepth:
        maxDepth = depth
        
        
        
d = {"number of files": filecount,"number of directories":dircount,"maximum depth of directory tree":maxDepth} 
if filecount > 0:
    d["file size"] = { "max": maxFileSize, "min": minFileSize }

                  
jo = json.dumps(d)
with open(jsonfile, "w") as outfile:
    outfile.write(jo)
# Writing to sample.json
