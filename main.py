import sys
from numeron import NumerOn

if __name__ == '__main__':
    numeron = NumerOn()
    while(True):
        try:
            answer = int( input("数字の被らない3桁の整数を入力してください\n"))
        except ValueError:
            print ("\033[31mError: \033[m数字以外を入力しないでください")
            continue
        if answer < 99 or 1000 <answer:
            print("\033[31mError: \033[m3桁の数字を入力してください")
            continue
            
        Eat,  Bite = numeron.judge_answer(answer)
        print("Eat:",Eat)
        print("Bite",Bite)
        if Eat == 3:
            break
        
    print("正解！おめでとうございます！")
      