import random

"""卡池内容（未设置四星up角色）"""
up = '魈'
st5 = [up, up, up, up, up, '刻晴', '莫娜', '七七', '迪卢克', '琴']
cha_4 = ['安柏', '丽莎', '凯亚', '芭芭拉', '雷泽', '菲谢尔', '班尼特', '诺艾尔', '菲谢尔', '砂糖',
         '迪奥娜', '北斗', '凝光', '香菱', '行秋', '重云', '辛焱']
weapon_4 = ['弓藏', '祭礼弓', '绝弦', '西风猎弓', '昭心', '祭礼残章', '流浪乐章', '西风秘典', '西风长枪',
            '雨裁', '匣里灭辰', '祭礼大剑', '钟剑', '西风大剑', '匣里龙吟', '祭礼剑', '笛剑', '西风剑']
st4 = weapon_4 + cha_4
get = []#这是每次抽奖后存储抽出内容的列表
have = []#这是存储总抽出内容的列表

class Stats:
    """跟踪游戏统计信息"""
    def __init__(self):
        self.total = 0#记录总抽卡次数（似乎没用到）
        self.up_num = 0#记录up保底次数（180发保底）
        self.num_4 = 0#记录四星保底次数（10发保底）
        self.num_5 = 0#记录五星保底次数（90发保底）
        self.stone = 0#这个用于充值系统，记录原石数

stat = Stats()


def single():
    """不保底时的抽奖"""
    i = random.randint(1, 10001)#生成10000个整数
    if i in range(1, 61):#五星中奖概率为0.6%
        a = random.randint(0, 5)
        star = st5[a]
        stat.num_5 = 0
    elif i in range(61, 316):#四星角色概率为2.55%
        cha = random.randint(0, len(cha_4)-1)
        star = cha_4[cha]
        stat.num_4 = 0
    elif i in range(316, 571):#四星武器概率为2.55%
        wea = random.randint(0, len(weapon_4)-1)
        star = weapon_4[wea]
        stat.num_4 = 0
    elif i in range(571, 10001):#其余为三星
        star = '三星'
    else:
    #不知道为什么，实际操作中总是会生成写奇奇怪怪的
    #东西，为了不影响原函数，这里else直接忽视
        return None
    if star == up:
        stat.num_5 = 0
        stat.up_num = 0
    add(star)#这个函数会在后面解释


def check_up():
    """检查保底"""
    if stat.up_num < 179:#检查up角色保底
        if stat.num_5 < 89:#检查五星保底
            if stat.num_4 < 9:#检查四星保底
                single()#如果没到保底，就正常抽卡
            else:
            #如果到保底了，就直接送出期望物品
                o_4 = random.randint(0, len(st4) - 1)
                star = st4[o_4]
                add(star)
                stat.num_4 = 0
        else:#同理，不赘述了
            o_5 = random.randint(0, len(st5) - 1)
            star = st5[o_5]
            add(star)
            stat.num_5 = 0
    else:
        star = up
        add(star)
        stat.up_num = 0


def add(star):
    """每次抽卡完毕的常规操作"""
    record(star)#记录保底数据
    get.append(star)#将抽到的物品加入单次显示
    have.append(star)#将抽到的内容加入背包
    stat.total += 1#抽奖次数记录+1（真的没用到）


def record(star):
    """记录数据变化"""
    if star != '魈':#抽不到就加一
        stat.up_num += 1
    if star not in st4:
        stat.num_4 += 1
    if star not in st5:
        stat.num_5 += 1


def remember():
    """统计抽卡内容"""
    value_cnt = {}#将中奖添加到列表里
    for h in have:
        value_cnt[h] = value_cnt.get(h, 0) + 1
    print(value_cnt)


def extract():
    """单抽"""
    if stat.stone >= 160:#这里添加了个判断原石
        del get[:]
        check_up()
        stat.stone -= 160
        print(get)
    else:#充值系统我放在交互程序的文件里了
        print('您的原石不足，请充值！')


def ten():
    """十连函数"""
    if stat.stone >= 1600:
        del get[:]
        for num in range(0, 10):#操作十次
            check_up()
        stat.stone -= 1600
        print(get)
    else:
        print('您的原石不足，请充值！')

