
import snmpQuery as snmp


def storageSizeOID(storageId):
    return '1.3.6.1.2.1.25.2.3.1.5.{0}'.format(storageId)


def storageUsedOID(storageId):
    return '1.3.6.1.2.1.25.2.3.1.6.{0}'.format(storageId)


def getStorageTable(snmpAgentInfo):
    return snmp.snmpWalk(
        snmpAgentInfo.snmpVersion,
        snmpAgentInfo.community,
        snmpAgentInfo.address,
        snmpAgentInfo.port,
        '1.3.6.1.2.1.25.2.3'
    )


def getDiskUsagePercentage(agent):
    table = getStorageTable(agent)
    if table == None:
        return table

    totalDiskSpace = 0
    totalUsedSpace = 0

    for key, value in table.items():

        if value != '1.3.6.1.2.1.25.2.1.4':
            continue

        storageId = key.split('.')[-1]

        totalDiskSpace += float(
            table[storageSizeOID(storageId)])

        totalUsedSpace += float(
            table[storageUsedOID(storageId)])

    return totalUsedSpace / totalDiskSpace * float(100)


def getMemoryUsagePercentage(agent):
    table = getStorageTable(agent)
    if table == None:
        return table

    totalMemorySize = 0
    totalMemoryUsed = 0

    for key, value in table.items():

        storageId = key.split('.')[-1]
        value = value.lower()


        if value == 'physical memory':

            oid = storageUsedOID(storageId)
            totalMemoryUsed += float(table[oid])

            oid = storageSizeOID(storageId)
            totalMemorySize = float(table[oid])

        if value == 'memory buffers':
            oid = storageUsedOID(storageId)
            totalMemoryUsed -= float(table[oid])

        if value == 'shared memory':
            oid = storageUsedOID(storageId)
            totalMemoryUsed += float(table[oid])

        if value == 'cached memory':
            oid = storageUsedOID(storageId)
            totalMemoryUsed -= float(table[oid])

    # Compute percentage.
    return totalMemoryUsed / totalMemorySize * float(100)


def getAverageProcessorLoad(agent):
    table = snmp.snmpWalk(
        agent.snmpVersion,
        agent.community,
        agent.address,
        agent.port,
        '1.3.6.1.2.1.25.3.3.1.2'
    )
    if table == None:
        return table

    totalProcessorLoad = 0
    processorCount = 0


    for key, value in table.items():
        totalProcessorLoad += float(value)
        processorCount += 1


    if not processorCount:
        return totalProcessorLoad

    return totalProcessorLoad / float(processorCount)
