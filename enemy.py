import numpy as np
import random
class Enemy:
    def __init__(self):
        self._used_answer = [] #一度答えた3桁の数字を格納
        self._unuseable_number = []#使えない番号------おいおいランダム生成の番号から個々の値を抜きたい
        self._allregister = np.array([])
      
        
    def disassemble_toplace(self, answer):
        #3桁の整数を1の位、10の位、100の位に分解してリスト[1,10,100]にして返す
        answers_once = answer % 10
        answers_tens = ((answer - answers_once) % 100) / 10
        answers_hundreds = ((answer - answers_once - answers_tens*10)) / 100
        answers_place = [answers_once, answers_tens, answers_hundreds]
        return answers_place
    
    def assemble(self, place=[]):
        return place[0]+place[1]*10+place[2]*100
    
    def register_result(self, answer, eat, bite):
        #引数として渡した数字とその結果をnumpy配列としてallregisterに記憶する
        np.append(self._allregister, np.array([answer, eat, bite]),axis = 0)
    
    def judge_overlap(self,place=[]):
        """渡したリストの中の値が全て違う場合False,一つでも重なっているとTrueを返す"""
        if(place[0] != place[1]
               and place[0] != place[2]
               and place[1] != place[2]):
            return False
        return True
    
    def judge_used(self, nextanswer):
        """渡した値を既に使っている場合はTrue,使っていない場合はFalseを返す"""
        for i in range(len(self._used_answer)):
            if nextanswer == self._used_answer[i]:
                return True
        return False
    
    def first_answer(self):
        enemy_booking = True
        while (enemy_booking):
                enemy_answer = random.randint(102,987)#数値をランダム生成
                enemy_place = self.disassemble_toplace(enemy_answer)#桁を分解
                enemy_booking = self.judge_overlap(enemy_place)#被りを確認
                self._used_answer.append(enemy_answer)#使用済みリストに追加
        return enemy_answer
        
        
    def answers(self, before_answer, before_eat , before_bite):
        enemy_used = True #初期化
        enemy_overlap = True
        self._used_answer.append(before_answer) #以前の解答を記憶
        before_place = self.disassemble_toplace(before_answer) #以前の解答を分解
        
        """-----ここまで共通動作-----"""
        if before_bite == 3:
            while(enemy_used):
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
                enemy_answer = self.assemble(before_place)
                enemy_used = self.judge_used(enemy_answer)
            self._used_answer.append(enemy_answer)
            return enemy_answer
        
        elif before_eat == 1 and before_bite == 2:
            while(enemy_used):
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
                enemy_answer = self.assemble(before_place)
                enemy_used = self.judge_used(enemy_answer)
            self._used_answer.append(enemy_answer)
            return enemy_answer
        
        elif before_eat == 2:
            enemy_place =[]
            for i in range(self._allregister.shape[0]):
                if self._allregister[i][1] == 2:#---過去に2,0があった場合
                    while(enemy_used):
                        while(enemy_overlap):
                            register_place = self.disassemble_toplace(self._allregister[i][0])
                            for j in range(3):
                                if (register_place[j] == before_place[j]):
                                    enemy_place[j] = before_place[j]
                                else:
                                    enemy_place[j] = random.randint(0,9)
                            enemy_overlap = self.judge_overlap(enemy_place)
                        enemy_answer = self.assemble(enemy_place)
                        enemy_used =self.judge_used(enemy_answer)
                    self._used_answer.append(enemy_answer)
                    self.register_result(before_answer, before_eat, before_bite)#記録をallregisterに登録
                    return enemy_answer       
            #----過去に2,0が無かった場合
            while(enemy_used):
                while(enemy_overlap):
                    num = random.randint(0,2)
                    before_place[num] = random.randint(0,9)
                    enemy_overlap = self.judge_overlap(before_place)
                enemy_answer = self.assemble(before_place)
                enemy_used = self.judge_used(enemy_answer)
            self._used_answer.append(enemy_answer)
            self.register_result(before_answer, before_eat, before_bite)#記録をallregisterに登録
            return enemy_answer
        
        elif before_eat == 1:
            if before_bite ==1:
                while(enemy_used):
                    while(enemy_overlap):
                        sixpattern = random.randint(0,6)
                        if sixpattern == 0:
                            before_place [0] = before_place[0]
                            before_place[1] = before_place[2]
                            before_place[2] = random.randint(0,9)
                        elif sixpattern == 1:
                            before_place [0] = before_place[0]
                            before_place[2] = before_place[1]
                            before_place[1] = random.randint(0,9)
                        elif sixpattern == 2:
                            before_place [1] = before_place[1]
                            before_place[0] = before_place[2]
                            before_place[2] = random.randint(0,9)
                        elif sixpattern == 3:
                            before_place [1] = before_place[1]
                            before_place[2] = before_place[0]
                            before_place[0] = random.randint(0,9)
                        elif sixpattern == 4:
                            before_place [2] = before_place[2]
                            before_place[0] = before_place[1]
                            before_place[1] = random.randint(0,9)
                        else:
                            before_place [2] = before_place[2]
                            before_place[1] = before_place[0]
                            before_place[0] = random.randint(0,9)
                        enemy_overlap = self.judge_overlap(before_place)
                    enemy_answer = self.assemble(before_place)
                    enemy_used = self.judge_used(enemy_answer)
                self._used_answer.append(enemy_answer)
                self.register_result(before_answer, before_eat, before_bite)#記録をallregisterに登録
                return enemy_answer
            elif before_bite == 0:
                while(enemy_used):
                    while(enemy_overlap):
                        threepattern = random.randint(0,6)
                        if threepattern == 0:
                            before_place [0] = before_place[0]
                            before_place[1] = random.randint(0,9)
                            before_place[2] = random.randint(0,9)
                        elif threepattern == 1:
                            before_place [1] = before_place[1]
                            before_place[0] = random.randint(0,9)
                            before_place[2] = random.randint(0,9)
                        else:
                            before_place [2] = before_place[2]
                            before_place[1] = random.randint(0,9)
                            before_place[0] = random.randint(0,9)
                        enemy_overlap = self.judge_overlap(before_place)
                    enemy_answer = self.assemble(before_place)
                    enemy_used = self.judge_used(enemy_answer)
                self._used_answer.append(enemy_answer)
                self.register_result(before_answer, before_eat, before_bite)#記録をallregisterに登録
                return enemy_answer
        
        elif before_eat == 0:
            if before_bite == 1:
                while(enemy_used):
                    while(enemy_overlap):
                        sixpattern = random.randint(0,6)
                        if sixpattern == 0:
                            before_place[0] = random.randint(0,9)
                            before_place[1] = before_place[2]
                            before_place[2] = random.randint(0,9)
                        elif sixpattern == 1:
                            before_place[0] = random.randint(0,9)
                            before_place[2] = before_place[1]
                            before_place[1] = random.randint(0,9)
                        elif sixpattern == 2:
                            before_place[1] = random.randint(0,9)
                            before_place[0] = before_place[2]
                            before_place[2] = random.randint(0,9)
                        elif sixpattern == 3:
                            before_place[1] = random.randint(0,9)
                            before_place[2] = before_place[0]
                            before_place[0] = random.randint(0,9)
                        elif sixpattern == 4:
                            before_place[2] = random.randint(0,9)
                            before_place[0] = before_place[1]
                            before_place[1] = random.randint(0,9)
                        else:
                            before_place[2] = random.randint(0,9)
                            before_place[1] = before_place[0]
                            before_place[0] = random.randint(0,9)
                        enemy_overlap = self.judge_overlap(before_place)
                    enemy_answer = self.assemble(before_place)
                    enemy_used = self.judge_used(enemy_answer)
                self._used_answer.append(enemy_answer)
                self.register_result(before_answer, before_eat, before_bite)#記録をallregisterに登録
                return enemy_answer
            
            elif before_bite == 0:
                self._unuseable_number.extend(before_place)
                while (enemy_used):
                    while(enemy_overlap):
                        enemy_answer = random.randint(102,987)#数値をランダム生成
                        enemy_place = self.disassemble_toplace(enemy_answer)#桁を分解
                        enemy_overlap = self.judge_overlap(enemy_place)#被りを確認
                    enemy_used = self.judge_used(enemy_answer)
                self._used_answer.append(enemy_answer)#使用済みリストに追加
                self.register_result(before_answer, before_eat, before_bite)#記録をallregisterに登録
                return enemy_answer
                
                
                
                
                            
                
            
            
            
                    
                                
                            