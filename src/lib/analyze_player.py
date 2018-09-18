"""
analyze_player.py
analyzeMessageを行うサッカープレイヤーエージェント
"""

from lib import base_player_plus, robo_tools
import threading
import math


class AnalyzePlayer(base_player_plus.BasePlayerPlus, threading.Thread):
    def __init__(self):
        super(AnalyzePlayer, self).__init__()
        self.OUT_OF_RANGE = 999.9

    def analyzeMessage(self, message):
        # 初期メッセージの処理
        # print("p11:message:", message)
        if message.startswith("(init "):
            self.analyzeInitialMessage(message)
        # 視覚メッセージの処理
        elif message.startswith("(see "):
            self.analyzeVisualMessage(message)
        # 体調メッセージの処理
        elif message.startswith("(sense_body "):
            self.analyzePhysicalMessage(message)
            # この部分にコマンドを決定するコードを挿入してやる
            if self.m_strPlayMode.startswith("play_on"):
                self.beforeSendCommandFirstTime()
                self.beforeSendCommand()
            self.send(self.m_strCommand)

        # 聴覚メッセージの処理
        elif message.startswith("(hear "):
            self.analyzeAuralMessage(message)
        # サーバパラメータの処理
        elif message.startswith("(server_param"):
            self.analyzeServerParam(message)
        # プレーヤーパラメータの処理
        elif message.startswith("(player_param"):
            self.analyzePlayerParam(message)
        # プレーヤータイプの処理
        elif message.startswith("(player_type"):
            self.analyzePlayerType(message)
            # print("player_type_message", message)
        # エラーの処理
        else:
            print("p11 サーバーからエラーが伝えられた:", message)
            print("p11 エラー発生原因のコマンドは右記の通り :", self.m_strCommand[self.m_iTime])

    def analyzeInitialMessage(self, message):
        index0 = message.index(" ")
        index1 = message.index(" ", index0 + 1)
        index2 = message.index(" ", index1 + 1)
        index3 = message.index(")", index2 + 1)

        self.m_strSide = message[index0+1:index1]
        self.m_iNumber = int(message[index1+1:index2])
        self.m_strPlayMode = message[index2+1:index3]

    def analyzeVisualMessage(self, message):
        time = int(robo_tools.getParam(message, "see", 1))
        if time < 1:
            return
        self.m_dNeck = robo_tools.getNeckDir(message)
        if self.m_dNeck == self.OUT_OF_RANGE:
            return
        if self.checkInitialMode():
            self.m_dX = self.m_dKickOffX
            self.m_dY = self.m_dKickOffY

        pos = self.estimatePosition(message, self.m_dNeck, self.m_dX, self.m_dY)
        self.m_dX = pos["x"]
        self.m_dY = pos["y"]
        if message.find("(b)") == -1:
            return
        ballDist = robo_tools.getParam(message, "(b)", 1)
        ballDir = robo_tools.getParam(message, "(b)", 2)
        rad = math.radians(robo_tools.normalizeAngle(self.m_dNeck + ballDir))
        self.m_dBallX = self.m_dX + ballDist * math.cos(rad)
        self.m_dBallY = self.m_dY + ballDist * math.sin(rad)

    def analyzePhysicalMessage(self, message):
        self.m_iTime = int(robo_tools.getParam(message, "sense_body", 1))
        # スタミナ情報の解析
        st = message.split(" ")
        for i in range(len(st)):
            if st[i] == "(stamina":
                self.m_dStamina = float(st[i+1])

    def analyzeAuralMessage(self, message):
        index0 = message.find(" ")
        index1 = message.find(" ", index0+1)
        index2 = message.find(" ", index1+1)
        index3 = message.find(")", index2+1)
        strSpeaker = message[index1+1:index2]
        strContent = message[index2+1:index3]

    def analyzeServerParam(self, message):
        # print("serverParam: ", message)
        self.m_strServerParam = message

    def analyzePlayerParam(self, message):
        self.m_strPlayerParam = message

    def analyzePlayerType(self, message):
        # print("m_strPlayerType: ", self.m_strPlayerType)
        # print(message)
        id = int(robo_tools.getParam(message, "id", 1))
        # print("id: ", id)
        self.m_strPlayerType[id] = message

    def beforeSendCommand(self):
        return

    def beforeSendCommandFirstTime(self):
        return

    def checkFinishLearn(self):
        return