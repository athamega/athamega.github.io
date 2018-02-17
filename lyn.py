import random
import bitly
from BeautifulSoup import BeautifulSoup
import stepic


l = 'yitsheyzeus'
k = 'R_6e7993c0fe4d442aa736b64bfabb9dd3'
api = bitly.Api(login=l,apikey=k)

import sys
#import pyimgur
import urllib
import os

#im = pyimgur.Imgur('570be81fd8caac9') #56560fe7af848e745f50ac311d1fdf1c11275126
#im = pyimgur.Imgur('c0c828f140906aa') #4cdfd6f604ab7255792148f5aa9a229732b4b0a1
#im = pyimgur.Imgur('c0c828f140906aa') #4cdfd6f604ab7255792148f5aa9a229732b4b0a1
#im = pyimgur.Imgur('b4debe6ca234468') #4cdfd6f604ab7255792148f5aa9a229732b4b0a1
linkdump=1
imgdo=1
nolinks=0
nobitly=0
if linkdump:
	ldf = open('/home/adam/ldf.txt','a')
hm = {}
#keepmasked = ['matchbox20.','www.lamc','/lamc.la','reallyhim.com']
keepmasked = ['absooluwiolkfdsngkfjgnwefew',]
of = sys.argv[1]

text = open(of,'r').read()

soup = BeautifulSoup(text)
links = soup.findAll('a')
imgs = soup.findAll('img')

def bysolve(link):
  try:
   return bysolve2(link)
  except:
   print sys.argv[0]
   return link

def bysolve2(link):
  if 'bit.ly' in link:
    link = api.expand(link)
    return(bysolve(link))
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


if not nolinks:
 for link in links:
  ##check for bit.ly
#    print  link['href']
    key = link.get('href')
    link['href'] = bysolve(link.get('href'))
    inter = link['href']
    fme=0
    if inter is  None: fme=1 
#    link['href'] = bymask(link.get('href'))
    link['href'] = link.get('href')
    hm[key]=link['href']
    if fme==0 and key==hm[key] and fme==0:
      #remove  safe-redirect-url and "span id" from google crap
      if "safe-red" in link:
	print "safered",link
      rid=''.join(random.choice('0123456789ABCDEF') for i in range(16))
      if '?' in inter:
#	link['href']=bymask(inter+"&"+rid)
	hm[key]=link['href']
      else: 
#	link['href']=bymask(inter+"?"+rid)
	hm[key]=link['href']
    if key is None: fme=1
    if fme==0:  key=key.strip()
    if key=="": key="http://suez.fromthemachine.org"
    print key,inter,hm[key], link.text,
    l = 'None'
    if not link['href']:
      l = 'None'
    else:
      l = link['href']
    if not key: key=''
    if linkdump:
      #prit
      ldf.write(sys.argv[1]+','+key+','+l+'\n')
    else:
      if fme==0 and key in link.text and fme==0: link.string.replace(key,link['href'])	
      if fme==0 and "bit.ly" in link.text and fme==0: link.string=link['href']	
    print link
#im = pyimgur.Imgur('b4debe6ca234468')
#im = pyimgur.Imgur('384314be7f1d573')
#secretda55935876fc9647ee4f0835c6eb183d27719aad
from PIL import Image
#if not linkdump for img in imgs: 
if 0:
 if imgdo==1 and "imgur" not in img.get('src'):
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
  	nf.write(str(soup))

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

