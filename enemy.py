import numpy as np
import random
import copy
from tenacity import before_sleep_log
class Enemy:
    def __init__(self):
        """
        Enemyクラスのインスタンス変数
        self._unuseable_number: 各桁において数字をランダムに生成する時はこの辞書からリストを呼び出して生成する
        self._allregister: 既出の数字とその判定結果を全て登録するnumpy配列
        self._important_register: 直前に2Eatの結果になった数字とその結果
        """
        self._unuseable_number = {0:list(np.arange(0,10)),#1の位
                                  1:list(np.arange(0,10)),#10の位
                                  2:list(np.arange(0,10)),#100の位
                                  }
        
        self._allregister = np.empty((0,3),int)
        self._important_place =[]
        
      
        
    def disassemble_toplace(self, answer):        
        """_summary_
            3桁の整数を1の位、10の位、100の位に分解してリストにして返す

        Args:
            answer(str): 桁ごとに分解したい3桁の解答

        Returns:
            list: [1の位, 10の位, 100の位]の順番に格納されている
        """
        answer = int(answer)
        answers_once = answer % 10
        answers_tens = ((answer - answers_once) % 100) / 10
        answers_hundreds = ((answer - answers_once - answers_tens*10)) / 100
        answers_place = [answers_once, int(answers_tens), int(answers_hundreds)]
        return answers_place
    
    def assemble(self, place=[]):
        """_summary_
            引数リストに格納されている3つの数字を3桁の整数に変換して返す
        
        Args:
            place (list): [1の位, 10の位, 100の位]の順番に格納されているリスト

        Returns:
            int: 引数のリストが表していた3桁の整数
        """

        return 100*(place[2])+10*(place[1])+(place[0])
    
    def register_result(self, answer, eat, bite):
        """_summary_
            引数として渡した数字とその判定結果(Eat,Bite)をnumpy配列として変数allregisterに記憶する

        Args:
            answer(str): インスタンスが受け取った解答
            eat(str):    引数answerの判定結果
            bite(str):   引数answerの判定結果

        Returns:
            None
        """
        result_array = np.array([[int(answer), eat, bite]])
        self._allregister = np.append(self._allregister, result_array ,axis = 0)
        
    def remember_result(self, answer, eat, bite):
        """_summary_
            引数の解答をメンバ変数リストallregisterに記録し、その解答の結果がEat=0であったらそれらの番号をランダム生成の候補から消す

        Args:
            answer(str): インスタンスが受け取った解答
            eat(str):    引数answerの判定結果
            bite(str):   引数answerの判定結果

        Returns:
            None
        """
        self.register_result(answer, eat, bite)
        place = self.disassemble_toplace(answer)
        if eat == 0:
            for i in range(3):
                if place[i] in self._unuseable_number[i]:
                    self._unuseable_number[i].remove(place[i])
            if bite == 0:
                for j in range(3):
                    for k in range(3):
                        if place[j] in self._unuseable_number[k]:
                            self._unuseable_number[k].remove(place[j])
        if eat == 2:
            self._important_place = copy.copy(place)
        
    def prioritize(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        postpone = False
        enemy_answer = 0
        for i in range(((self._allregister.shape[0])-2),-1,-1):
            #---過去にE,B=2,0があった場合その結果から答えを生成する
            if self._allregister[i][1] == 2:
                enemy_answer = self.E2B0(self._important_place)
                postpone = True
                return postpone, enemy_answer
            
        return postpone, enemy_answer
    
    def judge_overlap(self,place=[]):
        """_summary_
            引数リストの中の値が全て異なっている場合False,一つでも重なっているとTrueを返す
        Args:
            place (list, optional): 各桁の数字を格納したリスト. Defaults to [].

        Returns:
            bool:  値が全て異なっている場合False,一つでも重なっているとTrueを返す
        """
        if(place[0] != place[1]
               and place[0] != place[2]
               and place[1] != place[2]):
            return False
        return True
    
    def judge_used(self, nextanswer):
        """渡した値を既に解答に使っている場合はTrue,使っていない場合はFalseを返す"""
        for i in range(self._allregister.shape[0]):
            if nextanswer == self._allregister[i][0]:
                return True
        return False
    
    def first_answer(self):
        """人間よりも前に解答順が回ってきた時はこの関数を用いて解答を生成する"""
        enemy_overlap = True
        while (enemy_overlap):
                enemy_answer = random.randint(12,987)#数値をランダム生成
                enemy_place = self.disassemble_toplace(enemy_answer)#桁を分解
                enemy_overlap = self.judge_overlap(enemy_place)#桁同士の被りを確認
        return enemy_answer
    
    def answers(self, before_answer, before_eat, before_bite):
        """直前の解答結果を元に解答を生成する"""
        before_answer = int(before_answer)
        self.remember_result(before_answer,before_eat, before_bite) #人間の解答を記憶
        before_place = self.disassemble_toplace(before_answer) #以前の解答を分解      
        if before_eat == 0:
            if before_bite == 0:
                enemy_answer = self.E0B0(before_place)
                return enemy_answer
            
            elif before_bite == 1:
                enemy_answer = self.E0B1(before_place)
                return enemy_answer
            
            elif before_bite == 2:
                enemy_answer = self.E0B2(before_place)
                return enemy_answer
            
            elif before_bite == 3:
                enemy_answer = self.E0B3(before_place)
                return enemy_answer
        
        elif before_eat == 1:
            if before_bite == 0:
                enemy_answer = self.E1B0(before_place)
                return enemy_answer
            
            elif before_bite == 1:
                enemy_answer = self.E1B1(before_place)
                return enemy_answer
            
            elif before_bite == 2:
                enemy_answer = self.E1B2(before_place)
                return enemy_answer
            
        elif before_eat == 2:
            enemy_answer = self.E2B0(before_place)
            return enemy_answer
        
        
        
        
    
    def E0B0(self, before_place):
        """_summary_

        Args:
            before_place (_type_): _description_

        Returns:
            _type_: _description_
        """
        postpone, enemy_answer = self.prioritize()
        if postpone == True:
            return enemy_answer
        else:
            enemy_used = True
            enemy_overlap = True
            while(enemy_used == True or enemy_overlap ==True):
                for i in range(3):
                    before_place[i] = random.choice(self._unuseable_number[i])
                enemy_overlap = self.judge_overlap(before_place)
                enemy_answer = self.assemble(before_place)
                enemy_used = self.judge_used(enemy_answer)
            return enemy_answer
    
    def E0B1(self, before_place):
        """_summary_

        Args:
            before_place (_type_): _description_

        Returns:
            _type_: _description_
        """
        postpone, enemy_answer = self.prioritize()
        if postpone == True:
            return enemy_answer
        else:
            enemy_used = True 
            enemy_overlap = True
            buckup_beforeplace = copy.copy(before_place) #ループした時に引数を失わないようにバックアップをとる
            while(enemy_used == True or enemy_overlap ==True):
                before_place = copy.copy(buckup_beforeplace)
                sixpattern = random.randint(0,5)
                if sixpattern == 0:
                    before_place[0] = random.choice(self._unuseable_number[0])
                    before_place[1] = before_place[2]
                    before_place[2] = random.choice(self._unuseable_number[2])
                elif sixpattern == 1:
                    before_place[1] = before_place[0]
                    before_place[0] = random.choice(self._unuseable_number[0])
                    before_place[2] = random.choice(self._unuseable_number[2])
                elif sixpattern == 2:
                    before_place[0] = before_place[2]
                    before_place[1] = random.choice(self._unuseable_number[1])
                    before_place[2] = random.choice(self._unuseable_number[2])
                elif sixpattern == 3:
                    before_place[0] = before_place[1]
                    before_place[1] = random.choice(self._unuseable_number[1])
                    before_place[2] = random.choice(self._unuseable_number[2])
                elif sixpattern == 4:
                    before_place[2] = before_place[0]
                    before_place[0] = random.choice(self._unuseable_number[0])
                    before_place[1] = random.choice(self._unuseable_number[1])
                else:
                    before_place[2] = before_place[1]
                    before_place[0] = random.choice(self._unuseable_number[0])
                    before_place[1] = random.choice(self._unuseable_number[1])
                enemy_overlap = self.judge_overlap(before_place)
                enemy_answer = self.assemble(before_place)
                enemy_used = self.judge_used(enemy_answer)
            return enemy_answer
    
    def E0B2(self, before_place):
        """_summary_

        Args:
            before_place (_type_): _description_

        Returns:
            _type_: _description_
        """
        postpone, enemy_answer = self.prioritize()
        if postpone == True:
            return enemy_answer
        else:
            enemy_used = True 
            enemy_overlap = True
            buckup_beforeplace = copy.copy(before_place) #ループした時に引数を失わないようにバックアップをとる
            while(enemy_used == True or enemy_overlap ==True):
                before_place = copy.copy(buckup_beforeplace)
                threepattern = random.randint(0,2)
                if threepattern == 0:
                    before_place[0] = random.choice(self._unuseable_number[0])
                    tmp = before_place[1]
                    before_place[1] = before_place[2]
                    before_place[2] = tmp
                elif threepattern == 1:
                    before_place[1] = random.choice(self._unuseable_number[1])
                    tmp = before_place[0]
                    before_place[0] = before_place[2]
                    before_place[2] = tmp
                else:
                    before_place[2] = random.choice(self._unuseable_number[2])
                    tmp = before_place[0]
                    before_place[0] = before_place[1]
                    before_place[1] = tmp
                enemy_overlap = self.judge_overlap(before_place)
                enemy_answer = self.assemble(before_place)
                enemy_used = self.judge_used(enemy_answer)
            return enemy_answer
    
    def E0B3(self,before_place):
        """直前の解答がEat = 0,Bite = 3の時の解答を生成する"""
        postpone, enemy_answer = self.prioritize()
        if postpone == True:
            return enemy_answer
        else:
            enemy_used = True 
            buckup_beforeplace = copy.copy(before_place) #ループした時に引数を失わないようにバックアップをとる
            while(enemy_used):
                before_place = copy.copy(buckup_beforeplace)
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
            return enemy_answer
    
    def E1B0(self,before_place):
        """_summary_

        Args:
            before_place (_type_): _description_

        Returns:
            _type_: _description_
        """
        postpone, enemy_answer = self.prioritize()
        if postpone == True:
            return enemy_answer
        else:
            enemy_used = True 
            enemy_overlap = True
            buckup_beforeplace = copy.copy(before_place) #ループした時に引数を失わないようにバックアップをとる
            while(enemy_used == True or enemy_overlap ==True):
                before_place = copy.copy(buckup_beforeplace)
                threepattern = random.randint(0,2)
                if threepattern == 0:
                    before_place[0] = before_place[0]
                    before_place[1] = random.choice(self._unuseable_number[1])
                    before_place[2] = random.choice(self._unuseable_number[2])
                elif threepattern == 1:
                    before_place[1] = before_place[1]
                    before_place[0] = random.choice(self._unuseable_number[0])
                    before_place[2] = random.choice(self._unuseable_number[2])
                else:
                    before_place[2] = before_place[2]
                    before_place[1] = random.choice(self._unuseable_number[1])
                    before_place[0] = random.choice(self._unuseable_number[0])
                enemy_overlap = self.judge_overlap(before_place)
                enemy_answer = self.assemble(before_place)
                enemy_used = self.judge_used(enemy_answer)
            return enemy_answer
    
    def E1B1(self,before_place):
        """_summary_

        Args:
            before_place (_type_): _description_

        Returns:
            _type_: _description_
        """
        enemy_used = True 
        enemy_overlap = True
        buckup_beforeplace = copy.copy(before_place) #ループした時に引数を失わないようにバックアップをとる
        for i in range(((self._allregister.shape[0])-2),-1,-1):
            if self._allregister[i][1] == 2:
                register_place = self.disassemble_toplace(self._allregister[i][0])
                
                #過去のEat=2の解答とまったく同じ数字を用いていた場合、過去のEat=2の解答からランダムに1つ数字を変えて解答を生成する
                if all(map(before_place.__contains__, (register_place[0], register_place[1],register_place[2]))): 
                    while(enemy_used == True or enemy_overlap ==True):
                        enemy_place = copy.copy(register_place)
                        num = random.randint(0,2)
                        enemy_place[num] = random.choice(self._unuseable_number[num])
                        enemy_overlap = self.judge_overlap(enemy_place)
                        enemy_answer = self.assemble(enemy_place)
                        enemy_used = self.judge_used(enemy_answer)
                    return enemy_answer
                #過去のE=2と違う数字を用いていた場合、過去のEat=2の解答から重複する数字だけ参照し、残りの数字はランダムに変えて解答を生成する
                else:
                    while(enemy_used == True or enemy_overlap ==True):
                        enemy_place = [0,0,0]
                        for j in range(3):
                            if register_place[j] in before_place:#befoe_placeと同じ数字が入っていたらregister_placeと同じ値を採用
                                enemy_place[j] = copy.copy(register_place[j])
                            else:
                                enemy_place[j] = copy.copy(random.choice(self._unuseable_number[j]))
                        enemy_overlap = self.judge_overlap(enemy_place)
                        enemy_answer = self.assemble(enemy_place)
                        enemy_used = self.judge_used(enemy_answer)
                    return enemy_answer
            
        #----参照した結果、過去にEat=2が無かった場合    
        while(enemy_used == True or enemy_overlap ==True):
            before_place = copy.copy(buckup_beforeplace)
            sixpattern = random.randint(0,5)
            if sixpattern == 0:
                before_place[0] = before_place[0]
                before_place[1] = before_place[2]
                before_place[2] = random.choice(self._unuseable_number[2])    
            elif sixpattern == 1:
                before_place[0] = before_place[0]
                before_place[2] = before_place[1]
                before_place[1] = random.choice(self._unuseable_number[1])
            elif sixpattern == 2:
                before_place[1] = before_place[1]
                before_place[0] = before_place[2]
                before_place[2] = random.choice(self._unuseable_number[2])
            elif sixpattern == 3:
                before_place[1] = before_place[1]
                before_place[2] = before_place[0]
                before_place[0] = random.choice(self._unuseable_number[0])
            elif sixpattern == 4:
                before_place[2] = before_place[2]
                before_place[0] = before_place[1]
                before_place[1] = random.choice(self._unuseable_number[1])
            else:
                before_place[2] = before_place[2]
                before_place[1] = before_place[0]
                before_place[0] = random.choice(self._unuseable_number[0])
            enemy_overlap = self.judge_overlap(before_place)
            enemy_answer = self.assemble(before_place)
            enemy_used = self.judge_used(enemy_answer)
        return enemy_answer
    
    
    def E1B2(self,before_place):
        """直前の解答がEat=1,Bite=2の時の解答を生成する"""
        enemy_used = True 
        buckup_beforeplace = copy.copy(before_place) #ループした時に引数を失わないようにバックアップをとる
        while(enemy_used):
            before_place = copy.copy(buckup_beforeplace)
            threepattern = random.randint(0,2)
            if threepattern == 0:
                    before_place[0] = before_place[0]
                    tmp = before_place[1]
                    before_place[1] = before_place[2]
                    before_place[2] = tmp
            elif threepattern == 1:
                    before_place[1] = before_place[1]
                    tmp = before_place[0]
                    before_place[0] = before_place[2]
                    before_place[2] = tmp
            else:
                    before_place[2] = before_place[2]
                    tmp = before_place[0]
                    before_place[0] = before_place[1]
                    before_place[1] = tmp
            enemy_answer = self.assemble(before_place)
            enemy_used = self.judge_used(enemy_answer)
        return enemy_answer
    
    def E2B0(self,before_place):
        """
        直前の解答がEat=2,Bite=0の時の解答を生成する
        最初にallregister配列を参照して過去にEat=2の結果があるかどうか探す
        過去の結果に存在した場合は重複した数字だけをそのまま使用する
        過去の結果に存在しなかった場合はランダムに数字を一つ変更して解答を生成する
        """
        enemy_used = True 
        enemy_overlap = True
        buckup_beforeplace = copy.copy(before_place) #ループした時に引数を失わないようにバックアップをとる
        for i in range(((self._allregister.shape[0])-2),-1,-1):
            #---過去にE,B=2,0があった場合
            if self._allregister[i][1] == 2:
                register_place = copy.copy(self.disassemble_toplace(self._allregister[i][0]))
                #過去のEat=2の解答とまったく同じ数字を用いていた場合、処理を飛ばす
                if before_place == register_place:
                    continue
                else:
                    while(enemy_used == True or enemy_overlap ==True):
                        enemy_place =[0,0,0]
                        before_place = copy.copy(buckup_beforeplace)
                        for j in range(3):
                            if (register_place[j] == before_place[j]):
                                enemy_place[j] = before_place[j]
                            else:
                                enemy_place[j] = random.choice(self._unuseable_number[j])
                        enemy_overlap = self.judge_overlap(enemy_place)
                        enemy_answer = self.assemble(enemy_place)
                        enemy_used =self.judge_used(enemy_answer)
                    return enemy_answer
                
        #----参照した結果、過去にEat=2が無かった場合
        while(enemy_used == True or enemy_overlap ==True):
            before_place = copy.copy(buckup_beforeplace)
            num = random.randint(0,2)
            before_place[num] = random.choice(self._unuseable_number[num])
            enemy_overlap = self.judge_overlap(before_place)
            enemy_answer = self.assemble(before_place)
            enemy_used = self.judge_used(enemy_answer)
        return enemy_answer
    
    
        
    
        
    
        
            
        
            
            
                
                
                
                
                            
                
            
            
            
                    
                                
                            