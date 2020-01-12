import subprocess, urllib.request, re, time
from datetime import datetime

while(True):
    is_up = urllib.request.urlopen("http://www.rbc.com").getcode()

    host = "www.rbc.com"
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    ping = subprocess.Popen(["ping", host, "-n", "1"], stdout = subprocess.PIPE,stderr = subprocess.PIPE, shell=True)

    pattern = r"Average = (\d+\S+)"
    ping = re.findall(pattern, ping.communicate()[0].decode())[0]

    filename = 'log.txt'
    with open(filename, 'a') as out:
        out.write(str(is_up) + ' ' + ping + ' ' + time_stamp + '\n')
    
    time.sleep(300)