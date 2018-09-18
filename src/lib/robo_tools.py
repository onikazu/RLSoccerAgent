"""
robo_tools.py
サッカーエージェントで使用している数値・テキスト処理
"""

import math

OUT_OF_RANGE = 999


def getParam(self, message, keyword, number):
    key = "(" + keyword
    index0 = message.find(key)
    if index0 < 0:
        return self.OUT_OF_RANGE

    index1 = message.find(" ", index0 + len(key))
    if number == 4:
        index1 = message.find(" ", index1 + 1)
        index1 = message.find(" ", index1 + 1)
        index1 = message.find(" ", index1 + 1)
    elif number == 3:
        index1 = message.find(" ", index1 + 1)
        index1 = message.find(" ", index1 + 1)
    elif number == 2:
        index1 = message.find(" ", index1 + 1)
    else:
        pass
    index2 = message.find(" ", index1 + 1)
    index3 = message.find(")", index1 + 1)
    if index3 < index2 and index3 != -1 or index2 == -1:
        index2 = index3
    result = 0.0
    try:
        result = float(message[index1:index2])
    except Exception:
        # print("player4[getParam]:文字データによるエラー")
        # print("error 時のgetparamの引数{} ,{}, {}".format(message, keyword, number))
        result = self.OUT_OF_RANGE
    return result


def getObjectMessage(self, message, keyword):
    result = ""
    index0 = message.find(keyword)
    while -1 < index0:
        index1 = message.find(")", index0+2)
        index2 = message.find(")", index1+1)
        result += message[index0:index2+1]
        result += ")"
        index0 = message.find(keyword, index2)
    return result


def getNeckDir(message):
    index0 = message.find("((l")
    lineName = ""
    line = ""
    lineDist = -1 * OUT_OF_RANGE
    lineDir = -1 * OUT_OF_RANGE
    while index0 > -1:
        index1 = message.find(")", index0+3)
        lineName = message[index0+1:index1+1]
        line = "(" + lineName
        index2 = message.find(")", index1+1)
        line += message[index1+1:index2+1]
        dist = getParam(line, lineName, 1)
        dir = getParam(line, lineName, 2)
        if dist > lineDist:
            lineDist = dist
            lineDir = dir
        index0 = message.find("((l", index0+3)
    if lineDist == OUT_OF_RANGE:
        return OUT_OF_RANGE

    playerNeck = OUT_OF_RANGE
    if lineName.startswith("(l b)"):
        if 0 < lineDir and lineDir <= 90:
            playerNeck = 180 - lineDir
        else:
            playerNeck = -lineDir
    elif lineName.startswith("(l t)"):
        if 0 < lineDir and lineDir <= 90:
            playerNeck = -lineDir
        else:
            playerNeck = -180 - lineDir
    elif lineName.startswith("(l l)"):
        if 0 < lineDir and lineDir <= 90:
            playerNeck = -90 - lineDir
        else:
            playerNeck = 90 - lineDir
    elif lineName.startswith("(l r)"):
        if 0 < lineDir and lineDir <= 90:
            playerNeck = 90 - lineDir
        else:
            playerNeck = -90 - lineDir
    return playerNeck


def getDistance(self, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    return math.sqrt(dx * dx + dy * dy)


def normalizeAngle(self, angle):
    if abs(angle) > 720.0:
        print("angle error")
    while angle > 180.0:
        angle -= 360.0
    while angle < -180:
        angle += 360.0
    return angle