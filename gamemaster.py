import random

class GameMaster:
    def __init__(self):
        self.gamemaster = True
        while (self.gamemaster):
            self._once = random.randint(0,9)
            self._tens = random.randint(0,9)
            self._hundreds = random.randint(0,9)
            if(self._once != self._tens
               and self._once != self._hundreds
               and self._tens != self._hundreds):
                self.gamemaster = False
        self._place = [self._once, self._tens, self._hundreds]
        self._correct = self._once + self._tens*10 + self._hundreds*100
        
    def judge_role(self, answer):
        
        answer = int(answer)
        answers_once = answer % 10
        answers_tens = ((answer - answers_once) % 100) / 10
        answers_hundreds = ((answer - answers_once - answers_tens*10)) / 100
        answers_place = [answers_once, int(answers_tens), int(answers_hundreds)]
        Eat = 0
        Bite = 0
        for i in range (3):
            for j in range (3):
                if answers_place [i] == self._place [j]:
                    if i != j:
                        Bite +=1
                    elif i == j:
                        Eat +=1
        return Eat, Bite
    
    @property
    def correct(self):
        return self._correct