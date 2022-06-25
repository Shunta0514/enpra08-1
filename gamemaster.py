import random

class GameMaster:
    """_summary_
    ゲームの正解を生成し、保持するクラス
    
    プロパティ
    correct : 正解の数字
    """
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
        """_summary_
            渡された解答が正解しているのか判定し、その判定をEat,Biteとして返す

        Args:
            answer (_string_): 判定したい解答

        Returns:
            _type_: _description_
            int : 渡した解答の判定結果(Eat)
            int : 渡した解答の判定結果(Bite)
        """
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