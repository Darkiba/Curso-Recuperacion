import notificationMsg as msgs

import time


class notification:

    def __init__(self, agent):
        self.readyPending = False
        self.setPending = False
        self.goPending = False

        self.agent = agent

        self.lastReady = 0
        self.lastSet = 0
        self.lastGo = 0

    def flushPending(self):
        if self.goPending:
            if self.sendGoNotification():
                self.readyPending = False
                self.setPending = False

        if self.setPending:
            if self.sendSetNotification():
                self.readyPending = False

        if self.readyPending:
            self.sendReadyNotification()

    def sendReadyNotification(self):
        now = int(time.time())
        if now - self.lastReady < 2000:
            self.readyPending = True
            return False

        readyMsg = msgs.ReadyMessage(self.agent)
        readyMsg.sendMessage()

        self.readyPending = False
        self.lastReady = now
        return True

    def sendSetNotification(self):
        now = int(time.time())
        if now - self.lastSet < 2000:
            self.setPending = True
            return False

        setMsg = msgs.SetMessage(self.agent)
        setMsg.sendMessage()

        self.setPending = False
        self.lastSet = now
        return True

    def sendGoNotification(self):
        now = int(time.time())
        if now - self.lastGo < 2000:
            self.goPending = True
            return False

        goMsg = msgs.GoMessage(self.agent)
        goMsg.sendMessage()

        self.goPending = False
        self.lastGo = now
        return True
