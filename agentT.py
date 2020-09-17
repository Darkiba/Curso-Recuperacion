from storage import SnmpMonitorStorage
from threading import Thread

import snmpBaseLineQueries as perf
import rrdConstants
import snmpQuery
import logging
import time
import sys


class agentT(Thread):

    def __init__(self, agent):
        Thread.__init__(self)
        self.storage = SnmpMonitorStorage(agent)
        self.agent = agent
        self.running = True
        self.start()

    def setGroup(self, group):
        self.group = group

    def stop(self):
        self.running = False

    def __del__(self):
        self.stop()

    def run(self):
        while self.running:
            try:
                updates = dict()

                updates[rrdConstants.DS_MEMORY] = perf.getMemoryUsagePercentage(self.agent)
                updates[rrdConstants.DS_DISK] = perf.getDiskUsagePercentage(self.agent)
                updates[rrdConstants.DS_CPU] = perf.getAverageProcessorLoad(self.agent)

                self.storage.updateDatabase(updates)

                time.sleep(10)

            except:
                #print('Exception while monitoring %s : %s',
                              #self.agent, sys.exc_info())
                self.stop()

        self.group.stageRemoval(self.agent)
        self.group = None
