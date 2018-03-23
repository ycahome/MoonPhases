# turn moon right way up for images kindly provided for domoticz plugin
# see  http://www.domoticz.com/forum/viewtopic.php?f=65&t=21993
# ross lazarus me fecit march 10 2018
# added updated icons.txt
# rlazarus@rosshp:/tmp/mp$ cat MoonPhases1NM/icons.txt
# MoonPhases1NM;MoonPhases1NM;NewMoon MoonPhases

import os
suffix = 'SH'
ourd = os.getcwd()
flist = os.listdir('.')
flist = [x for x in flist if x[0] == 'M' and x[-4:] == '.zip']
for f in flist:
    os.chdir(ourd)
    dname = f.split('.')[0]
    try:
        os.mkdir(dname)
    except:
        print dname, 'already exists'
    os.chdir(dname)
    try:
       os.system('unzip -o ../%s' % f)
    except:
       print f, 'zip contents already exist'
    pnames = os.listdir('.')
    pnames = [x for x in pnames if x.endswith('.png') and not 'SH' in x]
    for pname in pnames:
        p = pname.split('.')[0]
        rest = p[10:] # eg MoonPhases4WG48_Off
        newname = 'MoonPhases%s%s%s.png' % (rest[:3],suffix,rest[3:])
        os.system('convert -rotate "200" ./%s ./%s' % (pname,newname))
        print 'rotated',pname,'to',newname
    ico = open('icons.txt','r').read()
    lnew = [x for x in ico.split(';')]
    lnew[0] = '%s%s' % (lnew[0],suffix)
    lnew[1] = lnew[0] # same..
    newico = ';'.join(lnew)
    ico = open('icons.txt','w')
    ico.write(newico)
    ico.close()
    os.system('zip ../%s%s %s%s*.png icons.txt' % (dname,suffix,dname,suffix))
    print 'Added SH images to',dname

