from pdfGenerator import pdfGenerator
from newAgent import newAgent, getAgentSysName, newAgentv2
from monitorGroup import MonitorGroup
from agent import agent
from datetime import datetime

import snmpQuery
import time
import sys
import os
import re

OPTION_MIN = 0
OPTION_MAX = 4
SLEEP_TIME = 1

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

def selectAgent(agentList, enumerateOnly=False):
    if len(agentList) == 0:
        print('No hay agentes .')
        return None

    optionMin, optionMax = 0, len(agentList)
    pattern = re.compile('^\d+$')

    print('Agentes:')
    for x in range(optionMin, optionMax):
        print('\t', x, ' ', agentList[x])
    print()

    if enumerateOnly:
        return None

    while True:
        selected = input('Ingresa el numero del agente: ')
        selected = selected.strip()
        if not selected:
            print('Por favor ingresa un numero.')
            continue
        if not pattern.match(selected):
            print('Solo puedes ingresar numeros de la lista.')
            continue
        selected = int(selected)
        if selected < optionMin or optionMax < selected:
            print('Ingresa solo numeros de la lista.')
            continue
        return agentList[selected]


def showMenu():
    print()
    print('Monitoreo SNMP, selecciona tu opcion.')
    print('0) Salir.')
    print('1) Lista de agentes.')
    print('2) Nuevo Agente.')
    print('3) Eliminar Agente.')
    print('4) Reporte.')
    print()

    pattern = re.compile('^\d$')

    while True:
        option = input('Ingresa una opcion: ').strip()
        if not option:
            continue
        if not pattern.match(option):
            print('Ingresa un numero que represente la opcion.')
            continue
        option = int(option)
        if option < OPTION_MIN or OPTION_MAX < option:
            print('Ingresa solo elementos de la lista.')
            continue
        return option


def getDatetime():
    pattern = re.compile('^\d{4}\s+\d{2}\s+\d{2}\s+\d{2}\s+\d{2}\s+\d{2}$')

    while True:
        date = input('Ingresa la fecha y hora : ')
        date = date.strip()
        if not date:
            print('Por favor ingresa una fecha y hora.')
            continue
        if not pattern.match(date):
            print('Ingresa la fecha y hora en el programa especificado.')
            continue
        try:
            tokens = list(map(lambda x: int(x), date.split()))
            date = datetime(tokens[0], tokens[1], tokens[2],
                            tokens[3], tokens[4], tokens[5])
        except ValueError:
            print('Revisa la fecha y hora.')
            continue
        epoch = datetime.fromtimestamp(0)
        if date < epoch:
            print('La fecha y hora deben ser despues de ', epoch)
            continue
        return date


def getFileName():
    pattern = re.compile('^\w+$', re.ASCII)
    while True:
        filename = input('Nombre del archivo: ')
        filename = filename.strip()
        if not filename:
            print('Nombre de archivo.')
        if not pattern.match(filename):
            print('Ingresa un nombre valido.')
        return filename


def storeAgents(agentList):
    f = open('agents.txt', 'w')
    for agent in agentList:
        f.write("{0} {1} {2} {3}\r\n".format(
            agent.address,
            agent.port,
            agent.community,
            agent.snmpVersion
        )
        )
    f.close()


def loadAgents():
    agentList = []

    if not os.path.isfile('agents.txt'):
        return agentList

    f = open('agents.txt', 'r')
    for line in f:
        line = line.strip()
        if not line:
            continue

        tokens = line.split()
        tokens[1] = int(tokens[1])
        tokens[3] = int(tokens[3])
        agent = agent(*tokens)

        name = getAgentSysName(agent)
        if not name:
            continue

        agentList.append(agent)

    f.close()

    return agentList


if __name__ == '__main__':

    monitorGroup = MonitorGroup()
    listIP = []
    f = open('Discovery.txt', 'r')
    for line in f:
        listIP.append(line)
        #print(line)

    print(listIP)
    for item in listIP:
        agentInfo = newAgentv2(item[:-1])

        if agentInfo:
            monitorGroup.addAgentMonitor(agentInfo)

    f.close()

    while True:
        time.sleep(SLEEP_TIME)
        option = showMenu()

        if option == 0:


            storeAgents(monitorGroup.agents)

            del monitorGroup
            sys.exit(0)

        elif option == 1:

            selectAgent(monitorGroup.agents, enumerateOnly=True)

        elif option == 2:

            agentInfo = newAgent()
            if agentInfo:
                monitorGroup.addAgentMonitor(agentInfo)

        elif option == 3:

            agentInfo = selectAgent(monitorGroup.agents)
            if agentInfo:
                monitorGroup.removeAgentMonitor(agentInfo)

        elif option == 4:

            agent = selectAgent(monitorGroup.agents)
            agent2 = selectAgent(monitorGroup.agents)
            if not agentInfo:
                continue

            print('Ingresa la fecha y hora de inicio:')
            startTime = int(getDatetime().timestamp())
            print('Ingresa la fecha y hora de fin:')
            endTime = int(getDatetime().timestamp())

            if startTime > endTime:
                swapTime = endTime
                endTime = startTime
                startTime = swapTime

            filename = getFileName()

            pdfMaker = pdfGenerator(agent,agent2)
            pdfMaker.makeReport(filename, startTime, endTime)

        else:
            continue
