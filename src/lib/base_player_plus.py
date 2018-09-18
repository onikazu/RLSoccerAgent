"""
base_player_plus
analyzeMessageを行うために必要な機能を付け加えたサッカープレイヤーエージェント
"""

from lib import base_player, robo_tools
import threading
import math
import random


class BasePlayerPlus(base_player.BasePlayer, threading.Thread):
    def __init__(self):
        super(BasePlayerPlus, self).__init__()

    def estimatePosition(self, message, neckDir, playerX, playerY):
        result = {"x": 999, "y": 999}
        message = self.getLandMarker(message, playerX, playerY)

        flag = robo_tools.getObjectMessage(message, "((g") + robo_tools.getObjectMessage(message, "((f")
        index0 = flag.find("((")
        X = Y = W = S = 0.0
        flags = 0
        while index0 > -1:
            index1 = flag.find(")", index0 + 2)
            index2 = flag.find(")", index1 + 1)
            name = flag[index0 + 2:index1]
            # print("name", name)
            j = 0
            while self.m_strFlagName[j].endswith(name) is False:
                j += 1
                # if j >= 50:
                #     print("j", j, "name", name)
            try:
                dist = robo_tools.getParam(flag, name, 1)
                dir = robo_tools.getParam(flag, name, 2)
                rad = math.radians(robo_tools.normalizeAngle(dir + neckDir))
                W = 1 / dist
                X += W * (self.m_dFlagX[j] - dist * math.cos(rad))
                Y += W * (self.m_dFlagY[j] - dist * math.sin(rad))
                S += W
                flags += 1
                index0 = flag.find("((", index0 + 2)
                # dist が０になることについて修正
            except ZeroDivisionError:
                dist = robo_tools.getParam(flag, name, 1)
                dir = robo_tools.getParam(flag, name, 2)
                rad = math.radians(robo_tools.normalizeAngle(dir + neckDir))
                W = random.random()
                X += W * (self.m_dFlagX[j] - dist * math.cos(rad))
                Y += W * (self.m_dFlagY[j] - dist * math.sin(rad))
                S += W
                flags += 1
                index0 = flag.find("((", index0 + 2)

        if flags > 0:
            result["x"] = X / S
            result["y"] = Y / S

        return result

    def checkInitialMode(self):
        if self.m_strPlayMode.startswith("before_kick_off") or self.m_strPlayMode.startswith("goal_l") or \
                self.m_strPlayMode.startswith("goal_r"):
            return True
        else:
            return False

    def setKickOffPosition(self):
        if self.m_iNumber == 1:
            self.m_dKickOffX = -50.0
            self.m_dKickOffY = -0.0
        elif self.m_iNumber == 2:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = -15.0
        elif self.m_iNumber == 3:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = -5.0
        elif self.m_iNumber == 4:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = +5.0
        elif self.m_iNumber == 5:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = +15.0
        elif self.m_iNumber == 6:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = -15.0
        elif self.m_iNumber == 7:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = -5.0
        elif self.m_iNumber == 8:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = +5.0
        elif self.m_iNumber == 9:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = +15.0
        elif self.m_iNumber == 10:
            self.m_dKickOffX = -1.0
            self.m_dKickOffY = -5.0
        elif self.m_iNumber == 11:
            self.m_dKickOffX = -4.0
            self.m_dKickOffY = +10.0
        else:
            print("範囲外の背番号の選手です")

    def getLandMarker(self, message, playerX, playerY):
        # Bの解決
        message = message.replace("B", "b", 1)
        # Fの解決
        if message.find("(F)") > -1:
            name = "(F)"
            min_dist = self.OUT_OF_RANGE
            for i in range(2, 55):
                dist = robo_tools.getDistance(playerX, playerY, self.m_dFlagX[i], self.m_dFlagY[i])
                if min_dist > dist:
                    min_dist = dist
                    name = self.m_strFlagName[i]
            message = message.replace("F", name, 1)

        if message.find("(G)") > -1:
            name = "(G)"
            min_dist = self.OUT_OF_RANGE
            for i in range(2):
                dist = robo_tools.getDistance(playerX, playerY, self.m_dFlagX[i], self.m_dFlagY[i])
                if min_dist > dist:
                    min_dist = dist
                    name = self.m_strFlagName[i]
            message = message.replace("G", name, 1)

        return message