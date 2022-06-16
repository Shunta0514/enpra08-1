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
        return Eat,Bite
       
    def enemy_write(self,user_answer=-1,Eat=0,Bite=0):
        if int(user_answer) < 0:
            enemy_answer = self._enemy.first_answer()
        else:
            enemy_answer = self._enemy.answers(user_answer, Eat, Bite)
        return enemy_answer
    
    @property
    def correct(self):
        return self._GM.correct
    @property
    def answertimes(self):
        return self._answertimes
    
    @property
    def correct(self):
        return self._GM.correct


    