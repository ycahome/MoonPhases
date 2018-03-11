# turn moon right way up for images kindly provided for domoticz plugin
# see  http://www.domoticz.com/forum/viewtopic.php?f=65&t=21993
# ross lazarus me fecit march 10 2018
# added updated icons.txt
# rlazarus@rosshp:/tmp/mp$ cat MoonPhases1NM/icons.txt
# MoonPhases1NM;MoonPhases1NM;NewMoon MoonPhases

import os
prefix = 'SH'
ourd = os.getcwd()
flist = os.listdir('.')
flist = [x for x in flist if x[0] == 'M']
for f in flist:
    os.chdir(ourd)
    dname = f.split('.')[0]
    try:
        os.mkdir(dname)
    except:
        print dname, 'already exists'
    os.chdir(dname)
    try:
       os.system('unzip -o ../%s' % dname)
    except:
       print f, 'zip contents already exist'
    pnames = os.listdir('.')
    pnames = [x for x in pnames if x.endswith('.png') and not x[:3] == 'SH_']
    for pname in pnames:
        newname = '%s_%s' % (prefix,pname)
        os.system('convert -rotate "180" ./%s ./%s' % (pname,newname))
        print 'rotated',pname,'to',newname
    ico = open('icons.txt','r').readlines()
    lnew = [x for x in ico.split(';')]
    lnew[0] = '%s_%s' % (prefix,lnew[0])
    lnew[1] = lnew[0] # same..
    newico = ';'.join(lnew)
    ico = open('icons.txt','w')
    ico.write(newico)
    ico.close()
    os.system('zip ../%s_%s %s_%s*.png icons.txt' % (prefix,dname,prefix,dname))
    print 'Added SH images to',dname

