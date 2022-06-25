from operationboad import OperationBoad 

if __name__ == '__main__':
    
    #ローカル変数
    timelimit = 8
    OpBoad = OperationBoad(timelimit)
    OpBoad.expranation()
    tree = OpBoad.create_table()
    tree.mainloop()
    
    