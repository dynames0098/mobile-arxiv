# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import io
import os
import sys
import time
import shutil

def arxivDownloadToServer(subjectTable):


    headd=urllib.urlopen('headd')
    headd=BeautifulSoup(headd)
    f=io.open('arxiv.html','w')
    f.write(headd.prettify())
    firstRun=1;

    j=0
    for subject in subjectTable:
        i=0
        arxivOC=BeautifulSoup(urllib.urlopen('http://arxiv.org/list/'+subject+'/recent'))

        ###COMPONENTS

        aim=arxivOC.find_all('div',attrs={'id':'dlpage'})
        aim=aim[0].dl

        titles=aim.find_all(attrs={"class":"list-title"})
        pdf=aim.find_all(attrs={"title":"Download PDF"})
        if firstRun:
            f.write(unicode(aim.previous_sibling.previous_sibling))
            firstRun=0
        f.write(unicode('<h3>'+subject+'</h3>'))
        f.write(u'<ul>')

        for tag in titles:
            tag.span.string=""
            del tag['class']
            tag.name='a'
            tag['style']="color:white;"
            pdfname=os.path.split(pdf[i]['href'])[1]+'.pdf'
            print pdfname
            #downloadPdfFromArxiv('http://arxiv.org'+pdf[i]['href'],pdfname)
            print "downloaded, sleep"
            tag['href']='http://arxiv.org'+pdf[i]['href']
            tag=tag.wrap(arxivOC.new_tag("div"))
            tag=tag.wrap(arxivOC.new_tag("h2"))
            tag=tag.wrap(arxivOC.new_tag("label"))
            tag['for']="item"+str(j)

            ii=BeautifulSoup('<i aria-hidden="true"></i>')
            ii['for']="item1"

            tag.h2.insert_before(ii)

            abs=getAbstract(os.path.split(pdf[i]['href'])[1])
            abs=abs.wrap(arxivOC.new_tag("div"))
            abs=abs.wrap(arxivOC.new_tag("li"))
            abs=abs.wrap(arxivOC.new_tag("ul"))
            abs['class']="options"
            abs=abs.wrap(arxivOC.new_tag("li"))
            abs['class']="block"
            abs.ul.insert_before(tag)

            inputButton=BeautifulSoup('<input type="checkbox" name="item" id="item'+str(j)+'" />')
            abs.label.insert_before(inputButton)


            f.write(abs.prettify())
            i+=1
            j+=1
            #time.sleep(10)
            print "wake up"
        f.write(u'</ul>')
    f.close()

def downloadPdfFromArxiv(urlpath,pdfname):
    currentLoc=sys.path[0]
    print "downloading "+urlpath+" to"+currentLoc
    if not os.path.isdir(currentLoc+'/pdf/'):
        os.mkdir(currentLoc+'/pdf/')
    urllib.urlretrieve(urlpath,currentLoc+'/pdf/'+pdfname)

def getAbstract(numOrder):
    soup=urllib.urlopen('http://arxiv.org/abs/'+numOrder)
    soup=BeautifulSoup(soup)
    abs=soup.find_all("blockquote")[0]
    del abs['class']
    abs.name='p'
    return abs

if __name__=='__main__':
    arxivDownloadToServer(['math.OC','cs.CV'])
    shutil.copyfile('arxiv.html','B:\\github\\spyder\\pdf\\static\\arxiv.html')
