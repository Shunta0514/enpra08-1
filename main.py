from numeron import NumerOn

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
      