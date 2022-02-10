import psutil
import re
import time
import os

#func. take process id and return heap value
def getHeap(pid):
	allocatedHeap = open("/proc/"+str(currentID)+"/maps")
	currentAdd=0
	flag =0
	for line in allocatedHeap.readlines():
		if line.find('[heap]') > 0 or flag == 1:
			flag=1
		if (line.find('[') > 0 or line.find('/') > 0 )  and not (line.find('[heap]') > 0) :
			flag =0
			continue
		temp = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r])', line)
		initialAdd = int(temp.group(1), 16)
		finalAdd = int(temp.group(2), 16)
		currentAdd+= (finalAdd-initialAdd) /(1024*1024)
	return currentAdd

pids={}

while(1) :
	for proc in psutil.process_iter():
		try:
			currentID = proc.pid  #get the id of process
			if currentID not in pids :  
				pids[currentID] = [getHeap(currentID),0,0]
			else :
				pids[currentID][1] = pids[currentID][0]# put old value in pids[currentID][1]
				pids[currentID][0] = getHeap(currentID)#get current value and save it in pids[currentID][0]

			currentState= pids[currentID][0]
			finalState = pids[currentID][1]
			if abs(currentState - finalState) > 200 :
				pids[currentID][2]+=1#couting no of times that process make allocate and dealocate
			
			if pids[currentID][2] >= 4 :  #Detect behavior after 4 times 
				print("Abnormal program detected")
				print("The Program is blocked")
				print(proc.name)# get Process ID,name and status which we BLock
				os.kill(currentID, 9)#Block process
			
			
		except (PermissionError , psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
			pass

	time.sleep(10)
