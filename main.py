import sys
from numeron import NumerOn

if __name__ == '__main__':
    
    #ローカル変数
    timelimit = 8
    numeron = NumerOn()
    print("数字の被らない3桁の数字を当ててね")
    print("Eat:  数字と数字の収まる位置(桁)が一致してるよ")
    print("Bite: 数字は一致してるけど収まる位置(桁)が違っているよ")
    print("ヒントを頼りに"+ str(timelimit) +"以内に解いてみよう")
    while(True):
        if numeron.get_Times() > timelimit:
            print("\033[31mGAME OVER\033[m")
            break
        else:
            try:
                answer = int( input("数字の被らない3桁の整数を入力してね\n>>>"))
            except ValueError:
                print ("\033[31mError: \033[m数字以外を入力しないで")
                continue
            if answer < 99 or 1000 <answer:
                print("\033[31mError: \033[m3桁の数字を入力してね")
                continue
                
            Eat,  Bite = numeron.judge_answer(answer)
            print("Eat:",Eat)
            print("Bite",Bite)
            if Eat == 3:
                print("\033[32m正解！おめでとう！\033[m")
                print("\033[32m今回の記録は"+ str(numeron.get_Times()) + "回です\033[m")
                break
        

      