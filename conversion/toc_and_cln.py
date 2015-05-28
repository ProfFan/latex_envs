
"""
Created on Thu Nov 18 15:34:38 2014
@author: JF
"""

import glob
import os
import sys
import time
from stat import *

    
def texheaders_filtering(input_file):
    import re
    
    st = os.stat(input_file)
    atime = st[ST_ATIME] #access time
    mtime = st[ST_MTIME] #modification time
   
    with open(input_file,'rt') as f:
        text=f.read()
    #print(text)           
    my_texfile = input_file #file.split('.html')[0] + 'b.html' 
    if sys.version_info >= (3,0,0):
        my_texfile_desc = open(my_texfile, 'wt', newline='')
    else:
        my_texfile_desc = open(my_texfile_file, 'wt')


    def remp(intext):
        #out=re.findall('\\\\[sub]?section',intext.group(0))
        out=re.findall('(\\\\[sub]?section|\\\\chapter)',intext.group(0))        

        print(out) 
        """"print(out.group(0))
        return out.group(0) """ 
        return out[-1] 
 
    #newtext=re.sub('section{Table of Contents}([\s\S]*?)\\[sub]?section{','Remplacement',text,flags=re.M)
    newtext=re.sub('\\\\section{Table of Contents}([\s\S]*?)(\\\\[sub]?section|\\\\chapter)',remp,text,flags=re.M)
    newtext=re.sub('\\\\begin{verbatim}[\s]*?<matplotlib\.[\S ]*?>[\s]*?\\\\end{verbatim}','',newtext,flags=re.M)
    newtext=re.sub('\\\\begin{verbatim}[\s]*?<IPython\.core\.display[\S ]*?>[\s]*?\\\\end{verbatim}','',newtext,flags=re.M)
    
    #bottom page with links to Index/back/next (suppress this)
#'----[\s]*?<div align=right> [Index](toc.ipynb)[\S ]*?.ipynb\)</div>'
    newtext=re.sub('\\\\begin{center}\\\\rule{3in}{0.4pt}\\\\end{center}[\s]*?\\\\href{toc.ipynb}{Index}[\S\s ]*?.ipynb}{Next}','',newtext,flags=re.M)
   
    
    # figcaption(text,label=)
    tofind="figcaption\(([\s\S]*?)\)\n([\s\S]*?)\\\\begin{center}\s*\\\\adjustimage[\s\S]*?}}{([\S]*?)}\s*\\\\end{center}"
   
    def replacement(text):
        cap=re.match("\"([\S\s]*?)\",[\S\s]*?label=\"([\S]*?)\"",text.group(1))
        
        if cap==None:
             cap=re.match("\"([\S\s]*?)\"",text.group(1))
             caption=cap.group(1)
             label=""
             rep="\n%s\n\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.6\\linewidth]{%s}\n\\caption{%s}\n\\end{figure}" % (text.group(2),text.group(3),caption)
        else:
             caption=cap.group(1)
             label=cap.group(2)  
             rep="\n%s\n\\begin{figure}[H]\n\\centering\n\\includegraphics[width=0.6\\linewidth]{%s}\n\\caption{%s}\n\\label{%s}\n\\end{figure}" % (text.group(2),text.group(3),caption,label)
        return rep
    code="Init"
   
    while (code!=None):   
        code=re.search(tofind,newtext)             
        newtext=re.sub(tofind,replacement,newtext,flags=re.M)

 

    my_texfile_desc.write(newtext)
    
    #modify the file timestamp
    my_texfile_desc.close()    
    os.utime(my_texfile,(atime,mtime))




    
verbose=True    
if __name__ == '__main__':	
    import argparse

    whatitdoes="""This program filters a LaTeX file \n
        - in order to remove the first 'table of contents section', 
    to the next section ; 
         - it replaces figcaption structures to "\\caption{\\label{}}" LaTeX constructs. 
         - Finally, it also filters out various 'spurious' outputs"""
    myself="(c) JFB 2014"
    parser = argparse.ArgumentParser(description=whatitdoes, epilog=myself)
    # mandatory argument
    parser.add_argument(
    help = 'List of files to filter (accepts regular expressions)',
    dest = 'argfiles', default = '*.tex', type = str,  nargs = '*')
    # verbosity flag
    parser.add_argument('-v','--verbose', help = 'Prints information',
    dest = 'verbose', default = False,   #action='store_true'
    action='count')

    arguments = parser.parse_args()
    verbose=arguments.verbose
    if verbose==2: print("script arg: ", arguments.argfiles)
   
    if isinstance(arguments.argfiles,list):
        tex_files=[]
        for x in arguments.argfiles:
             tex_files = tex_files+glob.glob(x)   
    else:
        tex_files = glob.glob(arguments.argfiles)
    if verbose==2: print("glog.glog expansion: ", tex_files, '\n')
    if len(tex_files ) == 0:
        raise RuntimeError('No TeX files to convert.')
          
    for file in tex_files:
        if verbose:
            print("Filtering {}".format(file))
        texheaders_filtering(file)




