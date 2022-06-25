from numeron import NumerOn
import tkinter, tkinter.messagebox
from tkinter import ttk
import re

class OperationBoad:
    def __init__(self,timelimit):
        """_summary_
            人間がNumeronに解答を提出するときに使用するモニター
        Args:
            timelimit (_int_): 解答できる回数を渡す
        """
        self._numeron = NumerOn()
        self.timelimit = timelimit
        
    def expranation(self):
        """_summary_
            ゲーム開始直後にゲームのルール説明を表示し、先攻後攻を選択させるボタンを持つ
        Returns:
            None
        """
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
        
    
    def order_first_click(self):
        """_summary_
            先攻を選択すると動作する関数
        """
        self.order = 0
        self.exp_tki.destroy()
    
    def order_second_click(self):
        """_summary_
            後攻を選択すると動作する関数
        """
        self.order = 1
        self.exp_tki.destroy()

    def create_table(self):
        """_summary_
            ゲームを実行する操作盤

        _type_: _description_
            Tk : 作成したGUIを渡す
        """
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
        """_summary_
            作成したテキストボックスの入力を制限する関数。半角の数字のみ入力可能にする。
        Args:
            string (_string_): テキストボックスに入力した文字が渡される

        Returns:
            _bool_: 半角数字が入力された時のみTrueを返しそれ以外はFalseを返す
        """
        if re.match(re.compile("[0-9]+"),string):
            return True
        return False
    
    def recoding_result(self):
        """_summary_
            解答ボタンを押したときに動作する関数。解答を受け取り、判定を表示。そのまま連続して機械に解答を作成させその判定を表示する。
            勝敗が決まる、解答回数が上限に達するとポップアップを表示しGUIを閉じる
        Returns:
            
            
        """
        if self.order == 0:
            self._answer = self.user_write()
            self._Eat, self._Bite = self._numeron.judge_answer(self._answer)
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
            self._answer = self.user_write()
            self._Eat, self._Bite = self._numeron.judge_answer(self._answer)
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
    
    def user_write(self):
        """_summary_
            作成したテキストボックスからユーザーの解答を取得し正常な入力が成されたか判定する関数。
            解答が2桁、あるいは3桁の時はそのまま値を返す。
            不適切な解答が入力されるとポップアップを表示し、作成したGUIを終了する。

        Returns:
            _type_: _description_
            string : テキストボックスから取得した解答
        """
        answer = self.txt.get()
        self.txt.delete(0,tkinter.END)
        try:
            if int(answer)<10 or 1000<int(answer):
                self.irregular_enter()
        except ValueError:
            self.irregular_enter()
        
        return answer

    def irregular_enter(self):
        """_summary_
            user_write関数で不適切な入力が成された時に呼び出される関数。
            サブウインドウを表示し、同時に親ウインドウを閉じるボタンを表示する。
        """
        self.irr = tkinter.Toplevel()
        self.irr.title("Score Record")
        self.irr.geometry("300x200")
        Script = tkinter.Label(self.irr, text = "入力が正しくありません",font = 10)
        Script.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        button = tkinter.Button(self.irr, text = "閉じる",command = self.destroy_button)
        button.pack(side=tkinter.BOTTOM)
    
    def Win(self):
        """_summary_
            recording_result関数でユーザーが勝利すると呼び出される関数。
            サブウインドウを表示し、同時に親ウインドウを閉じるボタンを表示する。
        """
        self.win = tkinter.Toplevel()
        self.win.title("WIN")
        self.win.geometry("300x200")
        Script1 = tkinter.Label(self.win, text = "正解！おめでとう！",font = 10)
        Script2 = tkinter.Label(self.win, text = "今回の記録は"+ str(int(self._numeron.answertimes/2)) + "回です",font = 10)
        Script1.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        Script2.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        button = tkinter.Button(self.win, text = "閉じる",command = self.destroy_button)
        button.pack(side=tkinter.BOTTOM)
        
    def Lose(self):
        """_summary_
            recording_result関数でコンピューターが勝利すると呼び出される関数。
            サブウインドウを表示し、同時に親ウインドウを閉じるボタンを表示する。
        """
        self.lose = tkinter.Toplevel()
        self.lose.title("LOSE")
        self.lose.geometry("300x200")
        Script = tkinter.Label(self.lose, text = "残念！負けてしまった！！",font = 10)
        Script.pack(side = tkinter.TOP,anchor=tkinter.CENTER)
        button = tkinter.Button(self.lose, text = "閉じる",command = self.destroy_button)
        button.pack(side=tkinter.BOTTOM)
    
    def GameOver(self):
        """_summary_
            recording_result関数で解答回数が上限に達すると呼び出される関数。
            サブウインドウを表示し、同時に親ウインドウを閉じるボタンを表示する。
        """
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
        button = tkinter.Button(self.over, text = "閉じる",command = self.destroy_button)
        button.pack(side=tkinter.BOTTOM)
        
        
    def destroy_button(self):
        """_summary_
            サブウインドウでボタンが押されると呼び出される関数。親ウインドウのGUIを閉じる。
        """
        self.tki.destroy()