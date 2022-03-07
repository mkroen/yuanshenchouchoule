import main
from time import sleep

print('正在加载配置文件...')
sleep(1)#嘿嘿，加点儿正式感
print('欢迎使用《原神》模拟抽卡系统，随时输入q以退出')
while True:
    print('请输入对应字母以进入相应功能：\n\n[A]开始祈愿\n[B]祈愿记录\n[C]充值\n[Q]退出')
    msg = input('')
    msg = msg.title()
    if msg == 'A':
        yi = input('请选择：\n\n[A]祈愿1次\n[B]祈愿10次\n')
        if yi.title() == 'A':
            sleep(1)#sleep，营造氛围嘛
            main.extract()
            sleep(0.5)
            continue
        elif yi.title() == 'B':
            sleep(1)
            main.ten()
            sleep(0.5)
            continue
        elif yi.title() == 'q':
            break
        else:
            print('请输入正确的选项！')
            sleep(1)
            continue
    if msg == 'B':
        num = len(main.have)
        print('您已进行' + str(num) + '次祈愿')
        print('其中有:')
        main.remember()#显示背包的统计
        sleep(1.5)
        continue
    if msg == 'C':
        print('您当前原石余额为：' + str(main.stat.stone))
        chose = input('请选择充值金额：\n\n[A]6元（加赠60原石）\n[B]30元（加赠300原石）\n[C]98元（加赠980原石）'
                      '\n[D]198元（加赠1980原石）\n[E]328元（加赠3280原石）\n[F]648元（加赠6480原石）\n[G]返回\n')
        if chose.title() == 'A':
            main.stat.stone += 120
        elif chose.title() == 'B':
            main.stat.stone += 600
        elif chose.title() == 'C':
            main.stat.stone += 1960
        elif chose.title() == 'D':
            main.stat.stone += 3960
        elif chose.title() == 'E':
            main.stat.stone += 6480
        elif chose.title() == 'F':
            main.stat.stone += 12960
        elif chose.title() == 'G':
            continue
        elif chose == 'q':
            break
        else:
            print('请输入正确的选项！')
            continue
        print('充值成功！当前余额为：' + str(main.stat.stone))
        sleep(1.5)
        continue
    if msg == 'Q':
        break
print('感谢您使用模拟抽卡系统，祝您游戏愉快！')
sleep(1.5)



