import algeol as al

def main(argv, dic):
    if len(argv) < 2:
        print('コマンド引数がありません')
        print('対抗コマンド：')
        for key in dic.keys():
            print(' - ' + key)
        return
    s0 = argv[1]
    if s0 == 'all':
        print('全コマンドを実行します')
        for fn in dic.values():
            fn()
    elif s0 not in dic:
        print('%s は未対応のコマンドです' % s0)
        print('対抗コマンド：')
        for key in dic.keys():
            print(' - ' + key)
    else:
        dic[s0]()
