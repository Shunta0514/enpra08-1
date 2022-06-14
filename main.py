from numeron import NumerOn
from enemy import Enemy
        
def user_attack():
    while(True):
        try:
            user_answer = input("数字の被らない3桁の整数を入力してね\n\033[32m>>>\033[m")
        except ValueError:
            print ("\033[31mError: \033[m数字以外を入力しないで")
            continue
        if int(user_answer) < 11 or 1000 <int(user_answer):
            print("\033[31mError: \033[m数字の被らない3桁の正の整数を入力してね")
            continue
        Eat,  Bite = numeron.judge_answer(user_answer)
        break
    print("Eat:",Eat)
    print("Bite:",Bite)
    return user_answer, Eat, Bite

def enemy_attack(user_answer=-1,Eat=0,Bite=0):
    if int(user_answer) < 0:
        enemy_answer = enemy.first_answer()
    else:
        enemy_answer = enemy.answers(user_answer, Eat, Bite)
    Eat, Bite = numeron.judge_answer(enemy_answer)
    enemy.remember_result(enemy_answer,Eat,Bite)
    if int(enemy_answer)<100:
        print("\033[31m敵>>>\033[m0"+ str(int(enemy_answer)))
    else:
        print("\033[31m敵>>>\033[m"+ str(int(enemy_answer)))
    print("Eat:",Eat)
    print("Bite",Bite)
    return Eat
    
    
def attack_order():
    while(True):
        order=input("先攻と後攻を選んで書き込んでください\n\033[32m>>>\033[m")
        if order == "先攻":
            return True
        elif order == "後攻":
            return False
        else:
            print("先攻と後攻から選んでください")
            continue
    

if __name__ == '__main__':
    
    #ローカル変数
    timelimit = 8
    numeron = NumerOn()
    enemy = Enemy()
    order = attack_order()
    
    print("数字の被らない3つの数字を当ててね[012~987]")
    print("Eat:  数字と数字の収まる位置(桁)が一致してるよ")
    print("Bite: 数字は一致してるけど収まる位置(桁)が違っているよ")
    print("ヒントを頼りに"+ str(timelimit) +"回以内に解いてみよう!敵に負けないように頑張って！")
    
    while(True):
        if numeron.get_Times() == timelimit*2:
            print("\033[31mGAME OVER\033[m")
            print("答えは"+str(numeron.get_Correct()))
            break

        if order == False:
            Eat = enemy_attack()
            if Eat == 3:
                print("\033[31m残念！先に当てられてしまった！\033[m")
                break
            order = True
            
        user_answer, Eat, Bite = user_attack()
        if Eat == 3:
            print("\033[32m正解！おめでとう！\033[m")
            print("\033[32m今回の記録は"+ str(int(numeron.get_Times()/2)) + "回です\033[m")
            break
        
        if numeron.get_Times() == timelimit*2:
            print("\033[31mGAME OVER\033[m")
            print("答えは"+str(numeron.get_Correct()))
            break
        
        Eat = enemy_attack(user_answer,Eat,Bite)
        if Eat == 3:
            print("\033[31m残念！先に当てられてしまった！\033[m")
            break
        
      