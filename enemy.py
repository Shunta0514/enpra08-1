from dis import disassemble
import random

from sympy import false
class Enemy:
    def __init__(self):
        self._timelimit
        self._answertimes
        self._used_answer = [] #一度答えた3桁の数字を格納
        self._unuseable_number = [] #以前の解答から使えないとわかる数字
        
    def disassemble(self, answer):
        #3桁の整数を1の位、10の位、100の位に分解してリスト[1,10,100]にして返す
        answers_once = answer % 10
        answers_tens = ((answer - answers_once) % 100) / 10
        answers_hundreds = ((answer - answers_once - answers_tens*10)) / 100
        answers_place = [answers_once, answers_tens, answers_hundreds]
        return answers_place
    
    def assemble(self, place=[]):
        return place[0]+place[1]*10+place[2]*100
    
    def judge_booking(place=[]):
        """渡したリストの中の値が全て違う場合False,一つでも重なっているとTrueを返す"""
        if(place[0] != place[1]
               and place[0] != place[2]
               and place[1] != place[2]):
            return False
        return True
    
    def judge_used(self, nextanswer):
        """渡した値を既に使っている場合はTrue,使っていない場合はFalseを返す"""
        for i in len(self._used_answer):
            if nextanswer == self._used_answer[i]:
                return True
            else:
                return False
    
    def first_answer(self):
        enemy_master = True
        while (enemy_master):
                enemy_answer = random.randint(102,987)#数値をランダム生成
                enemy_place = self.disassemble(enemy_answer)#桁を分解
                enemy_master = self.judge_booking(enemy_place)#被りを確認
                self._used_answer.append(enemy_answer)#使用済みリストに追加
        return enemy_answer
        
        
    def answers (self, before_answer, before_eat , before_bite):
        enemy_master = True #初期化
        self._used_answer.append(before_answer) #以前の解答を記憶
        before_place = disassemble(before_answer) #以前の解答を分解
        
        """-----ここまで共通動作-----"""
        if before_bite == 3:
            while(enemy_master):
                twopattern = random.randint(0,1)
                if twopattern == 0:
                    tmp = before_place[0]
                    before_place[0] = before_place[1]
                    before_place[1] = before_place[2]
                    before_place[2] = tmp
                else:
                    tmp = before_place[0]
                    before_place[0] = before_place[2]
                    before_place[2] = before_place[1]
                    before_place[1] = tmp
                enemy_answer = self.assemble[before_place]
                enemy_master = self.judge_used(enemy_answer)
            self._used_answer.append(enemy_answer)
            return enemy_answer
        
        if before_eat == 1 and before_bite == 2:
            while(enemy_master):
                threepattern = random.randint(0,2)
                if threepattern == 0:
                    before_place [0] = before_place[0]
                    tmp = before_place[1]
                    before_place[1] = before_place[2]
                    before_place[2] = tmp
                elif threepattern == 1:
                    before_place [1] = before_place[1]
                    tmp = before_place[0]
                    before_place[0] = before_place[2]
                    before_place[2] = tmp
                else:
                    before_place [2] = before_place[2]
                    tmp = before_place[0]
                    before_place[0] = before_place[1]
                    before_place[1] = tmp
                enemy_answer = self.assemble[before_place]
                enemy_master = self.judge_used(enemy_answer)
            self._used_answer.append(enemy_answer)
            return enemy_answer
        
        if before_eat == 0 and before_bite ==0: