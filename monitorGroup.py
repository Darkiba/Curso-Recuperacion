from agentT import agentT
from agent import agent

class MonitorGroup:

    def __init__(self):
        self.monitors = dict()
        self.agents = list()
        self.queue = list()

    def addAgentMonitor(self, agent):
        self.commitPending()
        if not self.containsAgentMonitor(agent):
            identifier = agent.getIdentifier()
            self.monitors[identifier] = agentT(agent)
            self.monitors[identifier].setGroup(self)
            self.agents.append(agent)

    def containsAgentMonitor(self, agent):
        return (agent.getIdentifier() in self.monitors)

    def removeAgentMonitor(self, agent):
        if self.containsAgentMonitor(agent):
            del self.agents[self.agents.index(agent)]
            self.monitors[agent.getIdentifier()].stop()
            del self.monitors[agent.getIdentifier()]

    def getAgentList(self):
        self.commitPending()
        return self.agents

    def __del__(self):
        for agent, monitor in self.monitors.items():
            monitor.stop()

    def stageRemoval(self, agent):
        self.queue.append(agent)

    def commitPending(self):
        for agent in self.queue:
            self.removeAgentMonitor(agent)
        self.queue.clear()
