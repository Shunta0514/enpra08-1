from gamemaster import GameMaster
from enemy import Enemy


class NumerOn:
    def __init__(self):
        """_summary_
            Enemy クラスとGameMasterクラスを生成しゲームを進行するクラス
        
        プロパティ
            correct: 生成したGameMasterクラスが持っている正解の数字
            answertimes: ゲーム中に解答が行われた回数
        """
        self._enemy = Enemy()
        self._GM = GameMaster()
        self._answertimes = 0
       
    def judge_answer(self, answer):
        """_summary_
            入力した解答が正解かどうかを判定する
            同時にゲーム中の解答回数を操作し、Enemyクラスが解答を記憶する
        Args:
            answer (_int_): _description_事前に生成した解答

        Returns:
            _int_: Eat、Biteの順番にそれぞれの個数がint型の数字で返される
            
        """
        Eat, Bite = self._GM.judge_role(answer)
        self._answertimes += 1
        self._enemy.remember_result(answer,Eat,Bite)
        return Eat,Bite
       
    def enemy_write(self,user_answer=-1,Eat=0,Bite=0):
        """_summary_
            Enemyクラスの解答を生成する。直前の解答とその判定が渡されるとその値をEnemyクラスに渡し、何も渡されないとEnemyクラスがランダムに解答を作成する
        Args:
            user_answer (int):直前の解答を渡す。Defaults to -1.
            Eat (int): user_answerの判定結果(Eat) Defaults to 0.
            Bite (int): user_answerの判定結果(Bite) Defaults to 0.

        Returns:
            _type_: _description_
            int : 作成した解答を返す
        """
        if int(user_answer) < 0:
            enemy_answer = self._enemy.first_answer()
        else:
            enemy_answer = self._enemy.answers(user_answer, Eat, Bite)
        return enemy_answer
    
    @property
    def correct(self):
        return self._GM.correct
    @property
    def answertimes(self):
        return self._answertimes
    

    