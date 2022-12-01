import psutil
import schedule
import os
import time
from sys import *
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(files,send_to):
    files=os.path.abspath(files)
    
    from_addr = "rajputkamlesh1889@gmail.com"
    to_addr = send_to
    content = time.ctime()

    msg = MIMEMultipart()
    msg['From'] = "Kamlesh's Laptop"
    msg['To'] = to_addr
    msg['Subject'] = "Periodic Process Log"
    body = MIMEText(content,'plain')
    msg.attach(body)

    filename = files

    with open(filename,'r') as f:
        attachment = MIMEApplication(f.read(),Name = basename(filename))
        attachment['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))

    msg.attach(attachment)    

    smtp = smtplib.SMTP(host = 'smtp.gmail.com',port = 587)
    smtp.starttls()

    smtp.login("rajputkamlesh1889@gmail.com", "lmhxrcrtsklwceno")

    smtp.send_message(msg,from_addr=from_addr, to_addrs = to_addr)
    
    smtp.quit()

def ProcessDisplay(log_dir = "RunningProcesses"):
    listprocess = []

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass

    separator = "-"*80
    
    log_path = os.path.join(log_dir,"ProcessLog%s.csv"%(time.ctime()))

    f= open(log_path,"w")

    f.write(separator+"\n")
    f.write("Runing Process Logger : "+time.ctime()+"\n")
    f.write(separator+"\n")            

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs = ['pid','name','username'])
            pinfo['vms'] = proc.memory_info().vms/(1024*1024)

            listprocess.append(pinfo);

        except(psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass

    for element in listprocess:
        f.write("%s\n"%element) 

    return log_path             

def Task():
    File = ProcessDisplay()
    send_mail(File,argv[2])


def main():
    
    if(len(argv)<3):
        print("Please Refer Readme file before using the script")
        exit()

    else:
        Itime = int(argv[1])
        schedule.every(Itime).minutes.do(Task)

        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    main()    