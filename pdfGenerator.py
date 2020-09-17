
import rrdConstants
import snmpQuery
import pdfkit
import jinja2
import os


class pdfGenerator:

    def __init__(self, agent, agent2):
        self.resourceFolder = agent.getIdentifier()
        self.agentInfo = agent
        self.resourceFolder2 = agent2.getIdentifier()
        self.agentInfo2 = agent2
        self.loadTemplate()

    def loadTemplate(self):
        templateLoader = jinja2.FileSystemLoader(searchpath='./')
        templateEnv = jinja2.Environment(loader=templateLoader)
        self.template = templateEnv.get_template('reportTemplate.html')

    def renderGraphs(self, startTime, endTime):
        return

    def getAgentSysInfo(self):
        return snmpQuery.snmpWalk(
            self.agentInfo.snmpVersion,
            self.agentInfo.community,
            self.agentInfo.address,
            self.agentInfo.port,
            '1.3.6.1.2.1.1'
        )
    def getAgentSysInfo2(self):
        return snmpQuery.snmpWalk(
            self.agentInfo2.snmpVersion,
            self.agentInfo2.community,
            self.agentInfo2.address,
            self.agentInfo2.port,
            '1.3.6.1.2.1.1'
        )

    def renderHTML(self):
        sysInfo = self.getAgentSysInfo()
        sysInfo2 = self.getAgentSysInfo2()
        sysDescr = sysInfo['1.3.6.1.2.1.1.1.0'].lower()
        logo = 'infoLogo.png'
        if 'windows' in sysDescr:
            logo = 'infoLogo.png'
        elif 'linux' in sysDescr:
            logo = 'infoLogo.png'

        self.renderedHTML = self.template.render(
            agentOSLogo=os.path.abspath(logo),
            agentCommunity=self.agentInfo.community,
            agentSysName=sysInfo['1.3.6.1.2.1.1.5.0'],
            agentSysDescr=sysInfo['1.3.6.1.2.1.1.1.0'],
            agentSysUpTime=sysInfo['1.3.6.1.2.1.1.3.0'],
            agentSysContact=sysInfo['1.3.6.1.2.1.1.4.0'],
            agentSysLocation=sysInfo['1.3.6.1.2.1.1.6.0'],
            agentCommunity2=self.agentInfo2.community,
            agentSysName2=sysInfo2['1.3.6.1.2.1.1.5.0'],
            agentSysDescr2=sysInfo2['1.3.6.1.2.1.1.1.0'],
            agentSysUpTime2=sysInfo2['1.3.6.1.2.1.1.3.0'],
            agentSysContact2=sysInfo2['1.3.6.1.2.1.1.4.0'],
            agentSysLocation2=sysInfo2['1.3.6.1.2.1.1.6.0'],
            memoryGraphFile=os.path.abspath(
                self.resourceFolder + '/' + rrdConstants.MEMORY_GRAPH),
            diskGraphFile=os.path.abspath(
                self.resourceFolder + '/' + rrdConstants.DISK_GRAPH),
            cpuGraphFile=os.path.abspath(
                self.resourceFolder + '/' + rrdConstants.CPU_GRAPH),
            memoryGraphFile2=os.path.abspath(
                self.resourceFolder2 + '/' + rrdConstants.MEMORY_GRAPH),
            diskGraphFile2=os.path.abspath(
                self.resourceFolder2 + '/' + rrdConstants.DISK_GRAPH),
            cpuGraphFile2=os.path.abspath(
                self.resourceFolder2 + '/' + rrdConstants.CPU_GRAPH)
        )

    def makeReport(self, fileName, startTime, endTime):
        self.renderGraphs(startTime, endTime)
        self.renderHTML()
        pdfkit.from_string(self.renderedHTML, fileName + '.pdf')
