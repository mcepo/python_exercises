## getting process list and sorting it by process id and parent process id
## and writing results into files
import subprocess
import psutil
import pprint


##### getting process list and writing it to a file #####
processFile = open('processFile.lst', 'w')

for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['ppid', 'pid', 'name', 'username', 'create_time', 'exe' ])
    except:
        pass
    else:
        processFile.write('\t'.join(map(str,[pinfo['ppid'], pinfo['pid'], pinfo['name'], pinfo['username'], pinfo['create_time'], pinfo['exe']])))
        processFile.write('\n')


processFile.close()


#### reading process from file and sorting it ######
processFile = open('processFile.lst', 'r')

processList = []

for line in processFile.readlines():
    line = line[:len(line)-2]
    processList.append(line.split('\t'))

processFile.close()

#sortedProcessList = sorted(processList, key=lambda x: int(x[0])*10000 + int(x[1]))
sortedProcessList = sorted(processList, key=lambda x: (int(x[0]),int(x[1]) ))

processFile = open('sortedProcessFile.lst', 'w')

for pinfo in sortedProcessList:
     processFile.write('\t'.join(pinfo))
     processFile.write('\n')

processFile.close()


##### reading process list from file and outputing it ####
processFile = open('sortedProcessFile.lst', 'r')

for line in processFile.readlines():
    line = line[:len(line)-2]
    print(line)

processFile.close()






