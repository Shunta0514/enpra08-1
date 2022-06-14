from numeron import NumerOn    

if __name__ == '__main__':
    
    #ローカル変数
    timelimit = 8
    numeron = NumerOn()
    order = numeron.attack_order()
    
    print("数字の被らない3つの数字を当ててね[012~987]")
    print("Eat:  数字と数字の収まる位置(桁)が一致してるよ")
    print("Bite: 数字は一致してるけど収まる位置(桁)が違っているよ")
    print("ヒントを頼りに"+ str(timelimit) +"回以内に解いてみよう!敵に負けないように頑張って！")
    
    while(True):
        if numeron.answertimes == timelimit*2:
            print("\033[31mGAME OVER\033[m")
            print("答えは"+str(numeron.correct))
            break
        """-----Macine Process-----"""
        if order == False:
            answer = numeron.enemy_write()
            Eat,Bite = numeron.judge_answer(answer)
            if Eat == 3:
                print("\033[31m残念！先に当てられてしまった！\033[m")
                break
            order = True
        """-----User Process-----"""
        answer = numeron.user_write()
        Eat,Bite = numeron.judge_answer(answer)
        if Eat == 3:
            print("\033[32m正解！おめでとう！\033[m")
            print("\033[32m今回の記録は"+ str(int(numeron.answertimes/2)) + "回です\033[m")
            break
        
        if numeron.answertimes == timelimit*2:
            print("\033[31mGAME OVER\033[m")
            print("答えは"+str(numeron.correct))
            break
            
        """-----Macine Process-----"""
        answer = numeron.enemy_write(answer,Eat,Bite)
        Eat,Bite = numeron.judge_answer(answer)
        if Eat == 3:
            print("\033[31m残念！先に当てられてしまった！\033[m")
            break
        
      