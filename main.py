from numeron import NumerOn
from enemy import Enemy

if __name__ == '__main__':
    
    #ローカル変数
    timelimit = 8
    numeron = NumerOn()
    enemy = Enemy()
    print("数字の被らない3つの数字を当ててね[012~987]")
    print("Eat:  数字と数字の収まる位置(桁)が一致してるよ")
    print("Bite: 数字は一致してるけど収まる位置(桁)が違っているよ")
    print("ヒントを頼りに"+ str(timelimit) +"回以内に解いてみよう!敵に負けないように頑張って！")
    while(True):
        if numeron.get_Times() > timelimit:
            print("\033[31mGAME OVER\033[m")
            break
        else:
            try:
                answer = input("数字の被らない3桁の整数を入力してね\n>>>")
            except ValueError:
                print ("\033[31mError: \033[m数字以外を入力しないで")
                continue
            if int(answer) < 11 or 1000 <int(answer):
                print("\033[31mError: \033[m数字の被らない3桁の正の整数を入力してね")
                continue
                
            Eat,  Bite = numeron.judge_answer(answer)
            print("Eat:",Eat)
            print("Bite",Bite)
            if Eat == 3:
                print("\033[32m正解！おめでとう！\033[m")
                print("\033[32m今回の記録は"+ str(int(numeron.get_Times())) + "回です\033[m")
                break
            
            enemy_answer = enemy.answers(answer, Eat, Bite)
            Eat, Bite = numeron.judge_answer(enemy_answer)
            if int(enemy_answer)<100:
                print("敵>>>0"+ str(int(enemy_answer)))
            else:
                print("敵>>>"+ str(int(enemy_answer)))
            print("Eat:",Eat)
            print("Bite",Bite)
            if Eat == 3:
                print("\033[31m残念！先に当てられてしまった！\033[m")
                break
        
      