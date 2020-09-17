import pysnmp.hlapi as snmp


def snmpGet(snmpVersion, community, host, port, oids):
    objectTypes = [snmp.ObjectType(snmp.ObjectIdentity(oid)) for oid in oids]

    errorIndication, errorStatus, errorIndex, varBinds = next(
        snmp.getCmd(snmp.SnmpEngine(),
                    snmp.CommunityData(community, mpModel=snmpVersion),
                    snmp.UdpTransportTarget((host, port)),
                    snmp.ContextData(),
                    *objectTypes
                    )
    )

    if errorIndication:
        print(errorIndication)
        return None

    if errorStatus:
        print('%s at %s', errorStatus.prettyPrint(),
              errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
        return None

    results = [(str(name), str(value)) for name, value in varBinds]

    return dict(results)


def snmpWalk(snmpVersion, community, host, port, oid):
    generator = snmp.nextCmd(snmp.SnmpEngine(),
                             snmp.CommunityData(community, mpModel=snmpVersion),
                             snmp.UdpTransportTarget((host, port)),
                             snmp.ContextData(),
                             snmp.ObjectType(snmp.ObjectIdentity(oid)),
                             lexicographicMode=False
                             )

    results = dict()

    for errorIndication, errorStatus, errorIndex, varBinds in generator:
        if errorIndication:
            print(errorIndication)
            continue

        if errorStatus:
            print('%s at %s', errorStatus.prettyPrint(),
                  errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
            continue

        for name, value in varBinds:
            results[str(name)] = str(value)

    return results
