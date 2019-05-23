# !/usr/bin/python
import sys
import psutil
import os

#### first try if there is a before file ####

baseline = False

try:
    open('dump.before', 'r')
except:
    fileDump = open('dump.before', 'w')
else:
    baseline = True
    fileDump = open('dump.after', 'w')

#### processes #####

processList = []

for proc in psutil.process_iter():
    try:
        processList.append(proc.as_dict(attrs=['ppid', 'pid', 'name', 'username', 'create_time', 'exe' ]))
    except:
        pass

sortedProcessList = sorted(processList, key=lambda x: (x['ppid'],x['pid']) )

for pinfo in sortedProcessList:
    fileDump.write('\t'.join(map(str,[pinfo['ppid'], pinfo['pid'], pinfo['name'], pinfo['username'], pinfo['create_time'], pinfo['exe']])))
    fileDump.write('\n')

### network connections ###

netConnections = os.popen('netstat -aut').read().split('\n')

for line in netConnections:
    fileDump.write(line)
    fileDump.write('\n')


### cron jobs ####

korisnik = os.popen('sudo crontab -u pythontools -l').read()
korijen = os.popen('sudo crontab -l').read()
etcjob = os.popen('sudo cat /etc/crontab').read()
satni = os.popen('sudo ls /etc/cron.hourly/ -l').read()
tjedni = os.popen('sudo ls /etc/cron.weekly/ -l').read()
mjesecni = os.popen('sudo ls /etc/cron.weekly/ -l').read()

if korisnik == "":
    fileDump.write("EMPTY\n")
else:
    fileDump.write(korisnik + "\n")
if korijen == "":
    fileDump.write("EMPTY\n")
else:
    fileDump.write(korijen + "\n")
if satni == "total 0\n":
    fileDump.write("EMPTY\n")
else:
    fileDump.write(satni + "\n")
if tjedni == "total 0\n":
    fileDump.write("EMPTY\n")
else:
    fileDump.write(tjedni + "\n")
if mjesecni == "total 0\n":
    fileDump.write("EMPTY\n")
else:
    fileDump.write(mjesecni + "\n")
fileDump.write(etcjob + "\n")

#### os version #####

fileDump.write("\n-------OS Version--------\n")
uname = os.popen('uname -a')
for x in uname:
    fileDump.write(x)


### users and passwords ####

passwd = os.popen('sudo cat /etc/passwd').read()
shadow = os.popen('sudo cat /etc/shadow').read()

lista = os.popen('awk -F\':\' \'{ print $1}\' /etc/passwd').read()
user=lista.split()
fileDump.write("\n-------groups--------\n")
for x in user:
    groups = os.popen('sudo groups '+x).read()
    fileDump.write(groups)

fileDump.write("\n-------passwd--------\n")
fileDump.write(passwd)
fileDump.write("\n-------shadow--------\n")
fileDump.write(shadow)

#### mounts ####

mnt = os.popen('sudo df -h').read()
fileDump.write("\n-------Mounts--------\n")
fileDump.write(mnt)

mnt = os.popen('sudo cat /proc/mounts').read()
fileDump.write("\n-------Mounts /proc/mounts--------\n")
fileDump.write(mnt)

### applications ####

instaps = os.popen('dpkg -l').read()
fileDump.write(instaps)


#### permissions on key directories ####

loc = '/etc '
loc1 = '/sys '
loc2 = '/root '

output = os.popen('sudo ls -la ' + loc + loc1 + loc2).read()

lineArr = []
logArr = []

for line in output.split('\n'):
    if not line.startswith('total') and not line.startswith('/'):
        if not line.strip():
            continue
        else:
            lineArr = line.split()    
            logArr.append(lineArr) 

logArr.sort(key=lambda x: (x[-1]))

for i in logArr:
    for j in i:
        fileDump.write(str(j) + "\t")
    fileDump.write("\n")

#### logs ####

ab=0

if baseline:
    tekst=" BEFORE"
    
else:
    tekst=" AFTER"


logs=["/var/log/auth.log","/var/log/syslog","/var/log/faillog","/var/log/lastlog","/var/log/dpkg.log","/var/log/kern.log"]


for log1 in logs:
     try:
         log=open(log1).read()

         zag=log1+tekst+"\n"

         fileDump.write(zag+log+"\n")
     except:
         pass

### if there is an before file compare processes with it ###
if baseline:
    os.popen('diff dump.before dump.after > dump.diff')

print('Done !')

fileDump.close()