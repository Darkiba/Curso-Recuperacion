from icmplib import multiping

def ipList():
    ipAddr = input('Ingresa la dirección ip: ')
    subMask = input('Ingresa la máscara de subred: ')
    ipAddr = ipAddr[:-1]
    if subMask == '255.255.255.0':
        ipNum = 256
    elif subMask == '255.255.0.0':
        ipNum = 512
    elif subMask == '255.0.0.0':
        ipNum = 1022
    else:
        print('Ingrese una máscara de subred válida')

    ipNodes = []
    for i in range(1, 255):
        ipNodes.append(ipAddr + "{0}".format(i))

    return ipNodes

if __name__ == '__main__':

    listIP = ipList()
    hosts = multiping(listIP, count=2, interval=0.5, timeout=1)

    hosts_alive = []
    hosts_dead = []

    for host in hosts:
        if host.is_alive:
            hosts_alive.append(host.address)

        else:
            hosts_dead.append(host.address)

    f = open("Discovery.txt", "w+")

    for item in hosts_alive:
        f.write("%s\n" % item)

    f.close()



