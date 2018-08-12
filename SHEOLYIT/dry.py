
import random
import bitly
from BeautifulSoup import BeautifulSoup
import stepic


l = 'yitsheyzeus'
k = 'R_6e7993c0fe4d442aa736b64bfabb9dd3'
api = bitly.Api(login=l,apikey=k)

import sys
import pyimgur
import urllib
import os

#im = pyimgur.Imgur('570be81fd8caac9') #56560fe7af848e745f50ac311d1fdf1c11275126
#im = pyimgur.Imgur('c0c828f140906aa') #4cdfd6f604ab7255792148f5aa9a229732b4b0a1
#im = pyimgur.Imgur('c0c828f140906aa') #4cdfd6f604ab7255792148f5aa9a229732b4b0a1
#im = pyimgur.Imgur('b4debe6ca234468') #4cdfd6f604ab7255792148f5aa9a229732b4b0a1

##im = pyimgur.Imgur('b4debe6ca234468','f5b2c5cde7aabaa9d1083b1c3b668ba67427338f') #f5b2c5cde7aabaa9d1083b1c3b668ba67427338f	
#yitim = pyimgur.Imgur('220fb4a37cfab8a','f1d4fcce3a0aceebf1c7aab81b2008853340db0b')
#im = pyimgur.Imgur('c0c828f140906aa','e95813c2e152e6ec1b688635b4b131279dfaa5db')
im = pyimgur.Imgur('eac405e4fc0208a','2409cc0694ecb6bd755eede32c90dc6fad4d075f')
imgdo=0
nolinks=0
nobitly=0

lsof = []

cmdl = sys.argv[1]

#for dirname, dirnames, filenames in os.walk('/root/atham/'):
for filenames in os.listdir('/root/atham/'):
  if filenames[-4:] == "html":
   lsof.append(filenames)
lsof.remove('index.html')
#print lsof

def presolv(cmdl):
#  if cmdl.contains('html') and cmdl.contains('?'):
  try:
    if cmdl[1:1]==".": return cmdl
  except:
    return cmdl
  if "html" in cmdl and "?" in cmdl:
    if not 'x/c' in cmdl and not 'search' in cmdl and not 'youtube' in cmdl:
     cmdl = cmdl[:cmdl.index('?')]
  for item in lsof:
    try:
      file = cmdl[cmdl.index('.'):]
    except:
      print 'PRESOLV ERROR',cmdl
      return cmdl
    try:
      filwdir = file[file.index('/')+1:]
    except:
      print 'PRESOLV ERROR',file,cmdl
      return cmdl
    #print item[:4],filwdir[:4]
    if item[:4]==filwdir[:4]:
     #yearmatch
     #www.lamc.la/2017/07/is-it-westworld-or-cloverfield-ln.html
     #2017-07-10-is-it-westworld-or-cloverfield-ln.html
     #print item[11:],filwdir[8:]
     if item[11:]==filwdir[8:]:
       #filenamematch
       print 'match',item[11:],filwdir[8:]
       return './'+item
#    print item,filwdir
    if item==filwdir:
       return './'+item
  return cmdl
 

#print presolv(cmdl)

hm = {}
#keepmasked = ['matchbox20.','www.lamc','/lamc.la','reallyhim.com']
keepmasked = ['noneatall','zeromasked']

of = sys.argv[1]

text = open(of,'r').read()

soup = BeautifulSoup(text)
links = soup.findAll('a')
imgs = soup.findAll('img')

def bysolve(link):
  try:
   if link[1:1]=='.': return link
   return bysolve2(link)
  except:
   print sys.argv[0]
   return link

def bysolve2(link):
#  if 'bit.ly' in link:
#    link = api.expand(link)
#    return(bysolve(link))
  try:
    bso = urllib.urlopen(link)
  except:
    print sys.argv[0]
    return link
  kmflag=0
  for km in keepmasked:
        if km in bso.geturl():
          kmflag=1
  if kmflag==1: 
    return link
  if 'https://www.google.com/url?q=' in bso.geturl():
#urllib2.unquote(s).decode('utf8')
    print bso.geturl()[29:],'HAHA'
#    return bysolve(urllib2.unquote(bso.geturl()[29:]).decode('utf8'))
    return bysolve(bso.geturl()[29:])
  if '/x/c?' in bso.geturl():
    #print "X/C?"
    url = 'http://gmass.co'+bso.geturl()[bso.geturl().index('/x/c'):]
    url = url.replace('%3D','=')
    url = url.replace('%26','&')
    print url
    return bysolve(url)
  if 'click.php' in bso.geturl():
    print "click.php"
    return bysolve(bso.geturl())
  return bso.geturl()

def bymask(link):
   if "bitbucket.org" in link: link=link.replace('bitbucket.org','bitbucket.io')
   if "bygod.pcriot" in link: link=link.replace('bygod.pcriot.com','m.lamc.la')
   if nobitly: return link
   try:
    x= api.shorten(link)
   except:
    try:
      x = hm[link]
      print "recoverd from hash:" + link+"/"+x
    except:    
      x = link

    #print link + " : bymask error"
   return x

if nolinks: print "NO LINKS!!!"

if not nolinks:
 for link in links:
  ##check for bit.ly
#    print  link['href']
    key = link.get('href')
    print key
    link['href'] = bysolve(link.get('href'))
    inter = link['href']
    fme=0
    if inter is  None: fme=1 
#    link['href'] = bymask(link.get('href'))
    link['href'] = presolv(link.get('href'))
    hm[key]=link['href']
    print link['href'],"ymir"
    if fme==0 and key==hm[key] and fme==0:
      #remove  safe-redirect-url and "span id" from google crap
      if "safe-red" in link:
	print "safered",link
      rid=''.join(random.choice('0123456789ABCDEF') for i in range(16))
      if '?' in inter:
	#link['href']=bymask(inter+"&"+rid)
	hm[key]=link['href']
      else: 
	#link['href']=bymask(inter+"?"+rid)
	hm[key]=link['href']
    if key is None: fme=1
    if fme==0:  key=key.strip()
    if key=="": key="http://lamc.la"
    if not link is None:
     if not link.basestring is None:
     #print key,inter,hm[key], link.encode('utf-8') #link.text,
      try:
        if fme==0 and key in link.encode('utf-8') and fme==0: link.basestring.replace(key,link['href'])	
        if fme==0 and "bit.ly" in link.encode('utf-8') and fme==0: link.basestring=link['href']	
        print link
      except:
	print "ERROR",link
#im = pyimgur.Imgur('b4debe6ca234468')
#im = pyimgur.Imgur('384314be7f1d573')
#secretda55935876fc9647ee4f0835c6eb183d27719aad
from PIL import Image
for img in imgs: 
 if imgdo==1 and "doltimgur" not in img.get('src'):
  #x = image.retrieve(img.get('src'),'tempimg')
  #print x
  rid=''.join(random.choice('0123456789ABCDEF') for i in range(30000))
  try:
    if "http" in img.get('src'):
      image = urllib.URLopener()
      image.retrieve(img.get('src'),'temp')
      ts = Image.open('temp')
    else: ts = Image.open(img.get('src'))
    ts.save('temp2.png')
    s = stepic.Steganographer(ts)
    try:
      im2.putalpha(1)
      im2=s.encode(rid)
    except:
      print "passing on image convert of "+img.get('src')
      im2=ts
    im2.save('temp.png')
    i = im.upload_image('temp.png')      
  except:
    print "Unexpected error:", sys.exc_info()[0], str(sys.exc_info())
    print "IMGUR ERROR WAITING 20 MIN"
    print str(img) 
    if len(sys.argv)<3:
   	outfile = of
    else: 
  	outfile = sys.argv[2]

    nf = open(outfile,'w')
    try:
  	nf.write(soup.prettify())
    except:
  	print "some error with prettify"
  	nf.write(soup.encode('utf-8'))

    nf.close()
    exit

    
  print i.link
  img['src']=i.link

if len(sys.argv)<3:
  outfile = of
else: 
  outfile = sys.argv[2]

nf = open(outfile,'w')
#try:
#  nf.write(soup.prettify())
#except:
#  print "some error with prettify"
nf.write(str(soup))

nf.close()

