from numeron import NumerOn
import tkinter, tkinter.messagebox
from tkinter import ttk
import re

class OperationBoad:
    def __init__(self,timelimit):
        self._numeron = NumerOn()
        self.timelimit = timelimit
        
    def expranation(self):
        self.exp_tki = tkinter.Tk()
        self.exp_tki.geometry("700x300")
        self.exp_tki.title(u"Game Master")
        Rule = tkinter.Label(text = u"数字の被らない3つの数字を当ててね[012～987]",font = 14)
        Eat = tkinter.Label(text = u"Eat:  数字と数字の収まる位置(桁)が一致してるよ",font =14)
        Bite = tkinter.Label(text = u"Bite: 数字は一致してるけど収まる位置(桁)が違っているよ",font = 14)
        Advise = tkinter.Label(text = u"ヒントを頼りに"+ str(self.timelimit) +"回以内に解いてみよう。敵に負けないように頑張って！",font = 14)
        Rule.place(x=25, y=20)
        Eat.place(x=25, y=60)
        Bite.place(x=25, y=100)
        Advise.place(x=25, y=140)
        first = tkinter.Button(self.exp_tki, text = "先攻", command = self.order_first_click,font = (u"ＭＳ ゴシック", 18,))
        second = tkinter.Button(self.exp_tki, text = "後攻", command = self.order_second_click,font = (u"ＭＳ ゴシック", 18,))
        first.pack(side=tkinter.LEFT,anchor=tkinter.S,expand= True,fill= tkinter.X)
        second.pack(side=tkinter.RIGHT,anchor=tkinter.S,expand = True,fill= tkinter.X)
        self.exp_tki.mainloop()
        
        if self.order == 0:
            return True
        if self.order == 1:
            return False
    
    def order_first_click(self):
        self.order = 0
        self.exp_tki.destroy()
    
    def order_second_click(self):
        self.order = 1
        self.exp_tki.destroy()
        
    def create_table(self):
        column  = ("Number","Eat","Bite")
        self.tki = tkinter.Tk()
        self.tki.title("Score Record")
        self.tki.geometry("300x500")
        Script1 = tkinter.Label(text = "User:Green",font = 20)
        Script1.pack(side = tkinter.TOP)
        Script2 = tkinter.Label(text = "Machine:Red",font = 20)
        Script2.pack(side = tkinter.TOP)
        
        
        self.tree = ttk.Treeview(self.tki, columns = column, height=self.timelimit*2)
        
        self.tree.column("#0",width = 0, stretch = "no")
        self.tree.column("Number",anchor = "center", width = 100)
        self.tree.column("Eat",anchor = "center", width = 100)
        self.tree.column("Bite",anchor = "center", width = 100)  
        
        self.tree.heading("#0",text = "")
        self.tree.heading("Number",text = "Number",anchor="center")
        self.tree.heading("Eat",text = "Eat",anchor="center")
        self.tree.heading("Bite",text = "Bite",anchor="center")
        
        self.tree.tag_configure("red",foreground="red")
        self.tree.tag_configure("green",foreground="green")
        self.tree.pack(side =tkinter.TOP)
        
        if self.order == 1:
            answer = self._numeron.enemy_write()
            Eat,Bite = self._numeron.judge_answer(answer)
            if answer <100:
                self.tree.insert(parent = "",index="end", values =("0"+str(answer), Eat, Bite),tags = "red")
            else:
                self.tree.insert(parent = "",index="end", values =(str(answer), Eat, Bite),tags = "red")
            if Eat == 3:
                self.Lose()
                return 0
        
        rule = tkinter.Label(text = "数字の被らない3つの数字を入力")
        rule.pack(side =tkinter.TOP)
                
        vc = self.tki.register(self.limitchar)
        self.txt = tkinter.Entry(self.tki,validate="key",validatecommand=(vc,"%S"),width = 20)
        self.txt.pack(side=tkinter.TOP)
        
        button = tkinter.Button(self.tki, text = "解答",command = self.recoding_result,font = 10)
        button.pack(side=tkinter.BOTTOM)
        
        return self.tki
    
    def limitchar(self,string):
        if re.match(re.compile("[0-9]+"),string):
            return True
        return False
    
    def recoding_result(self):
        if self.order == 0:
            self._answer, self._Eat, self._Bite = self.create_answer()
            self.tree.insert(parent = "",index="end", values =(self._answer, self._Eat, self._Bite),tags = "green")
            if self._Eat == 3:
                self.Win()
                return 0
            answer = self._numeron.enemy_write(self._answer,self._Eat,self._Bite)
            Eat,Bite = self._numeron.judge_answer(answer)
            if answer <100:
                self.tree.insert(parent = "",index="end", values =("0"+str(answer), Eat, Bite),tags = "red")
            else:
                self.tree.insert(parent = "",index="end", values =(str(answer), Eat, Bite),tags = "red")
            if Eat == 3:
                self.Lose()
                return 0
            if self._numeron.answertimes == self.timelimit*2:
                self.GameOver()
                return 0
        else:
            self._answer, self._Eat, self._Bite = self.create_answer()
            self.tree.insert(parent = "",index="end", values =(self._answer, self._Eat, self._Bite),tags = "green")
            if self._Eat == 3:
                self.Win()
                return 0
            if self._numeron.answertimes == self.timelimit*2:
                self.GameOver()
                return 0
            answer = self._numeron.enemy_write(self._answer,self._Eat,self._Bite)
            Eat,Bite = self._numeron.judge_answer(answer)
            if answer <100:
                self.tree.insert(parent = "",index="end", values =("0"+str(answer), Eat, Bite),tags = "red")
            else:
                self.tree.insert(parent = "",index="end", values =(str(answer), Eat, Bite),tags = "red")
            if Eat == 3:
                self.Lose()
                return 0
        
    def create_answer(self):
        if  self.order == 0 and self._numeron.answertimes %2 == 0:
            #ユーザー先攻
            answer = self.user_write()
            Eat,Bite = self._numeron.judge_answer(answer)
            
        elif self.order != 0 and self._numeron.answertimes %2 != 0:
            #ユーザー後攻
            answer = self.user_write()
            Eat,Bite = self._numeron.judge_answer(answer)
        return answer, Eat, Bite
    
    def user_write(self):
        answer = self.txt.get()
        self.txt.delete(0,tkinter.END)
        try:
            if int(answer)<10 or 1000<int(answer):
                self.irregular_enter()
        except ValueError:
            self.irregular_enter()
        
        return answer

    def irregular_enter(self):
        self.irr = tkinter.Toplevel()
        self.irr.title("Score Record")
        self.irr.geometry("300x200")
        Script = tkinter.Label(self.irr, text = "入力が正しくありません",font = 10)
        Script.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        button = tkinter.Button(self.irr, text = "閉じる",command = self.irr_button)
        button.pack(side=tkinter.BOTTOM)
        
    def irr_button(self):
        self.txt.delete(0,tkinter.END)
        self.tki.destroy()
    
    def Win(self):
        self.win = tkinter.Toplevel()
        self.win.title("WIN")
        self.win.geometry("300x200")
        Script1 = tkinter.Label(self.win, text = "正解！おめでとう！",font = 10)
        Script2 = tkinter.Label(self.win, text = "今回の記録は"+ str(int(self._numeron.answertimes/2)) + "回です",font = 10)
        Script1.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        Script2.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        button = tkinter.Button(self.win, text = "閉じる",command = self.win_button)
        button.pack(side=tkinter.BOTTOM)
        
        
    def win_button(self):
        self.tki.destroy()
        
    def Lose(self):
        self.lose = tkinter.Toplevel()
        self.lose.title("LOSE")
        self.lose.geometry("300x200")
        Script = tkinter.Label(self.lose, text = "残念！負けてしまった！！",font = 10)
        Script.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        button = tkinter.Button(self.lose, text = "閉じる",command = self.lose_button)
        button.pack(side=tkinter.BOTTOM)
        
        
    def lose_button(self):
        self.tki.destroy()
    
    def GameOver(self):
        self.over = tkinter.Toplevel()
        self.over.title("GAME OVER")
        self.over.geometry("300x200")
        Script1 = tkinter.Label(self.over, text = "GAME OVER",font = 10)
        if self._numeron.correct<100:
            Script2 = tkinter.Label(self.over, text = "答えは0"+str(self._numeron.correct)+"です。",font = 10)
        else:
            Script2 = tkinter.Label(self.over, text = "答えは"+str(self._numeron.correct)+"です。",font = 10)
        Script1.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        Script2.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        button = tkinter.Button(self.over, text = "閉じる",command = self.gameover_button)
        button.pack(side=tkinter.BOTTOM)
        
        
    def gameover_button(self):
        self.tki.destroy()