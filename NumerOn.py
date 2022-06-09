import random
class NumerOn:
    def __init__(self):
        self.gamemaster = True
        while (self.gamemaster):
            self._correct = random.randint(102,987)
            self._once = self._correct % 10
            self._tens = ((self._correct - self._once) % 100) / 10
            self._hundreds = (self._correct - self._once - self._tens*10) / 100
            if(self._once != self._tens
               and self._once != self._hundreds
               and self._tens != self._hundreds):
                self.gamemaster = False
        self._place = [self._once, self._tens, self._hundreds]
            

        
    def get_Correct(self):
        print (self._correct)
    
   
    def judge_answer(self, answer):
        answers_once = answer % 10
        answers_tens = ((answer - answers_once) % 100) / 10
        answers_hundreds = ((answer - answers_once - answers_tens*10)) / 100
        answers_place = [answers_once, answers_tens, answers_hundreds]
        Eat = 0
        Bite = 0
        for i in range (3):
            for j in range (3):
                if answers_place [i] == self._place [j]:
                    if i != j:
                        Bite +=1
                    if i == j:
                        Eat +=1
        return Eat, Bite
    
    
    
if __name__ == '__main__':
    numeron = NumerOn()
    while(True):
        answer = int( input("数字の被らない3桁の整数を入力してください\n"))
        Eat,  Bite = numeron.judge_answer(answer)
        print("Eat:",Eat)
        print("Bite",Bite)
        if Eat == 3:
            break
        
    print("正解！おめでとうございます！")
      


    