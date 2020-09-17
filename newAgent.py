from agent import agent

import snmpQuery
import re

def getAgentSysName(agentInfo):
    try:
        SYSTEM_NAME = '1.3.6.1.2.1.1.5.0'
        responseValues = snmpQuery.snmpGet(
                agentInfo.snmpVersion,
                agentInfo.community,
                agentInfo.address,
                agentInfo.port,
                [SYSTEM_NAME]
            )
        return responseValues[SYSTEM_NAME]
    except:
        print('No hay conexion con el agente.')
    return None

def getAddress():
    while True:
        address = input('Direccion IP del agente: ')
        address = address.strip()
        if not address:
            print('Ingresa una direccion.')
            continue
        return address

def getPort():
    pattern = re.compile('^\d+$')
    while True:
        port = input('Puerto: ').strip()
        if not port:
            print('Ingresa un puerto.')
            continue
        if not pattern.match(port):
            print('Ingresa un puerto valido.')
            continue
        return int(port)

def getCommunity():
    pattern = re.compile('^\w+$', re.ASCII)
    while True:
        community = input('Comunidad: ').strip()
        if not community:
            print('Ingresa la comunidad.')
            continue
        if not pattern.match(community):
            print('Ingresa una comunidad valida.')
            continue
        return community

def getVersion():
    pattern = re.compile('^\d$')
    while True:
        version = input('Version SNMP: ')
        version = version.strip()
        if not version:
            print('Ingresa una version SNMP.')
            continue
        if not pattern.match(version):
            print('Ingresa una version valida.')
            continue
        version = int(version) - 1
        if version < 0 or 1 < version:
            print('Ingresa version valida.')
            continue
        return version

def newAgent():
    address = getAddress()
    port = getPort()
    community = getCommunity()
    version = getVersion()

    agentInfo = agent(address, port, community, version)
    agentName = getAgentSysName(agentInfo)

    if agentName == None:
        print('No hay conexion con el agente: ', agentInfo)
    else:
        print('Agente: ', agentName)

    return agentInfo

def newAgentv2(addr):
    address = addr
    port = 161
    community = 'grupo4cv5'
    version = 1

    agentInfo = agent(address, port, community, version)
    agentName = getAgentSysName(agentInfo)

    if agentName == None:
        print('No hay conexion con el agente: ', agentInfo)
    else:
        print('Agente: ', agentName)

    return agentInfo
