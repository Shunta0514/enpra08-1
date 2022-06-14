from gamemaster import GameMaster
from enemy import Enemy

class NumerOn:
    def __init__(self):
        self._enemy = Enemy()
        self._GM = GameMaster()
        self._answertimes = 0
    
    def judge_answer(self, answer):
        Eat, Bite = self._GM.judge_role(answer)
        self._answertimes += 1
        self._enemy.remember_result(answer,Eat,Bite)
        print("Eat:",Eat)
        print("Bite",Bite)
        return Eat,Bite
    
    def user_write(self):
        while(True):
            try:
                user_answer = input("数字の被らない3桁の整数を入力してね\n\033[32m>>>\033[m")
            except ValueError:
                print ("\033[31mError: \033[m数字以外を入力しないで")
                continue
            try:
                if int(user_answer) < 11 or 1000 <int(user_answer):
                    print("\033[31mError: \033[m数字の被らない3桁の正の整数を入力してね")
                    continue
            except ValueError:
                print ("\033[31mError: \033[m数字以外を入力しないで")
                continue
            break
        return user_answer

    def enemy_write(self,user_answer=-1,Eat=0,Bite=0):
        if int(user_answer) < 0:
            enemy_answer = self._enemy.first_answer()
        else:
            enemy_answer = self._enemy.answers(user_answer, Eat, Bite)
        if int(enemy_answer)<100:
            print("\033[31m敵>>>\033[m0"+ str(int(enemy_answer)))
        else:
            print("\033[31m敵>>>\033[m"+ str(int(enemy_answer)))
        return enemy_answer
    
    def attack_order(self):
        while(True):
            order=input("先攻と後攻を選んで書き込んでください\n\033[32m>>>\033[m")
            if order == "先攻":
                return True
            elif order == "後攻":
                return False
            else:
                print("先攻と後攻から選んでください")
                continue
    @property
    def correct(self):
        return self._GM.correct
    @property
    def answertimes(self):
        return self._answertimes


    