# -*- coding:utf-8 -*-

import  pygame
from	pygame.locals	import	*
import  time
import  random
import  threading

class BasePlane(object):

    def __init__(self,screen_temp,image_url,x,y,hp,wide,high):
        self.screen = screen_temp #窗口
        self.image = pygame.image.load(image_url) #对象图片
        self.x = x  #横坐标
        self.y = y  #纵坐标
        self.hp = hp  #生命值
        self.wide = wide  #图片宽度
        self.high = high  #图片高度
        self.bullet_list = [] #用于存储子弹对象
        self.start_time = time.time()

    #显示飞机;调用飞机图片变化方法;判断子弹是否出界，出界则删除子弹对象
    def dispaly(self):
        self.screen.blit(self.image, (self.x, self.y)) #将图片贴到窗口
        self.status_change()
        for bullet in self.bullet_list:
            bullet.display()
            bullet.move()
            if  self.judge(bullet):
                self.bullet_list.remove(bullet)

    # 判断子弹是否超出窗口范围，如果超出返回True
    def judge(self,bullet):
        if (bullet.x < 0) or (bullet.x + bullet.wide > 480) or \
                (bullet.y < 0)  or (bullet.y + bullet.high > 852):
            return True
        else:
            return False

    # 定义飞机开火方法，需要传入子弹对象，需要传入飞机坐标、飞机图片宽度等信息计算子弹坐标
    def fire(self,bullet_obj):
        self.bullet_list.append(bullet_obj(self.screen,self.x,self.y,self.wide,self.high))

    # 飞机图片变化方法，父类没有实际内容，子类需要重写，主要为“dispaly”方法能够引用
    def status_change(self):
        pass

class HeroPlane(BasePlane):
    def __init__(self,screen_temp):
        BasePlane.__init__(self,screen_temp,"./feiji/hero2.png",190,650,300,100,124)
        # 传入的参数依次为：self 、窗口、图片位置、飞机的X坐标，飞机的Y坐标，飞机hp，飞机图片宽度，飞机图片高度

    #定义飞机地用方法，并限制飞机移动范围
    def move_left(self):
        if self.x > -30:
            self.x -= 8
    def move_right(self):
        if self.x < 410:
             self.x += 8
    def move_up(self):
        if self.y > 0:
            self.y -= 8
    def move_down(self):
        if self.y < 700:
            self.y += 8

    #飞机随着hp值变化而更换贴图
    def status_change(self):
        if self.hp >= 400:
            self.image = pygame.image.load("./feiji/hero2.png")
        elif self.hp >= 300:
            self.image = pygame.image.load("./feiji/hero_blowup_n1.png")
        elif self.hp >= 200:
            self.image = pygame.image.load("./feiji/hero_blowup_n2.png")
        elif self.hp >= 100:
            self.image = pygame.image.load("./feiji/hero_blowup_n3.png")
        elif self.hp <= 0:
            self.image = pygame.image.load("./feiji/hero_blowup_n4.png")

#定义敌机类
class EnemyPlane(BasePlane):
    def __init__(self,screen_temp):
        BasePlane.__init__(self,screen_temp,"./feiji/enemy0.png",random.randint(1,460),0,100,51,39)
        #传入的参数依次为：self 、窗口、图片位置、飞机的X坐标，飞机的Y坐标，飞机hp，飞机图片宽度，飞机图片高度

    #敌机移动速度及方向
    def move(self):
        self.y += 2

    #敌机在随着hp的变化更换图片
    def status_change(self):
        if self.hp >= 80:
            self.image = pygame.image.load("./feiji/enemy0.png")
        elif self.hp >= 60:
            self.image = pygame.image.load("./feiji/enemy0_down1.png")
        elif self.hp >= 40:
            self.image = pygame.image.load("./feiji/enemy0_down2.png")
        elif self.hp >= 20:
            self.image = pygame.image.load("./feiji/enemy0_down3.png")
        elif self.hp <= 0:
            self.image = pygame.image.load("./feiji/enemy0_down4.png")

class Boss_1(BasePlane):
    def __init__(self,screen_temp):
        BasePlane.__init__(self,screen_temp,"./feiji/enemy1.png",205,0,600,69,89)
        #传入的参数依次为：self 、窗口、图片位置、飞机的X坐标，飞机的Y坐标，飞机hp，飞机图片宽度，飞机图片高度

    #敌机移动速度及方向
    def move(self):
        self.y += 0.6

    #敌机在随着hp的变化更换图片
    def status_change(self):
        if self.hp >= 500:
            self.image = pygame.image.load("./feiji/enemy1.png")
        elif self.hp >= 400:
            self.image = pygame.image.load("./feiji/enemy1_down1.png")
        elif self.hp >= 300:
            self.image = pygame.image.load("./feiji/enemy1_down2.png")
        elif self.hp >= 200:
            self.image = pygame.image.load("./feiji/enemy1_down3.png")
        elif self.hp <= 0:
            self.image = pygame.image.load("./feiji/enemy1_down4.png")

class Boss_2(BasePlane):
    def __init__(self,screen_temp):
        BasePlane.__init__(self,screen_temp,"./feiji/enemy2.png",165,0,2000,165,246)
        #传入的参数依次为：self 、窗口、图片位置、飞机的X坐标，飞机的Y坐标，飞机hp，飞机图片宽度，飞机图片高度
        self.direction = "right"

    #敌机移动速度及方向
    def move(self):
        if self.direction == "right":
            self.x += 1
        elif self.direction == "left":
            self.x -= 1

        if self.x + self.wide >= 480:
            self.direction = "left"
        elif self.x <= 0:
            self.direction = "right"

    #敌机在随着hp的变化更换图片
    def status_change(self):
        if self.hp >= 800:
            self.image = pygame.image.load("./feiji/enemy2.png")
        elif self.hp >= 600:
            self.image = pygame.image.load("./feiji/enemy2_down1.png")
        elif self.hp >= 400:
            self.image = pygame.image.load("./feiji/enemy2_down2.png")
        elif self.hp >= 200:
            self.image = pygame.image.load("./feiji/enemy2_down3.png")
        elif self.hp <= 0:
            self.image = pygame.image.load("./feiji/enemy2_down4.png")

    # 重写开火，主函数循环20次发射一颗子弹
    def fire(self, bullet_obj, x):
        u = [20 * p for p in range(1, 1000)]
        if x in u:
            self.bullet_list.append(bullet_obj(self.screen, self.x, self.y, self.wide, self.high))

#定义子弹基类
class BaseBullet(object):

    def __init__(self,screen_temp,image_url,hurt,wide,high,speed):
        self.screen = screen_temp
        self.image = pygame.image.load(image_url)
        self.hurt = hurt
        self.wide = wide
        self.high = high
        self.speed = speed

    #显示对象，并调用“move”方法
    def display(self):
        self.screen.blit(self.image, (self.x, self.y))
        self.move()

    # 这个在基类中为空，各个子类根据实际情况重写，主要为了让display方法继承该方法。
    def move(self):
        pass

class HeroBullet(BaseBullet):

    def __init__(self,screen_temp,x,y,planewide,planehigh):
        BaseBullet.__init__(self,screen_temp,"./feiji/bullet.png",20,22,22,10)
        self.x = x + planewide/2 - self.wide/2 +2  # 英雄飞机子弹的X坐标
        self.y = y - 15  #英雄飞机子弹的初始Y坐标

    # 定义子弹的移动速度及移动方向
    def move(self):
        self.y -= self.speed

#定义敌机子弹类
class EnemyBullet(BaseBullet):

    def __init__(self,screen_temp,x,y,planewide,planehigh):
        BaseBullet.__init__(self,screen_temp,"./feiji/bullet1.png",10,9,21,5) #调用父类初始化类参数
        self.x = x + planewide/2 - self.wide/2  #除父类参数外，单独定义子弹初始X坐标
        self.y = y + planehigh #除父类参数外，单独定义子弹初始Y坐标

    #敌机子弹以“speed”速度持续前进
    def move(self):
        self.y += self.speed

class Battle(object):
    def __init__(self,screen):
        self.screen = screen
        self.time = 3
        self.enemy_num = 3
        self.enemy_max_num = 120
        self.enemy_list = [] #存放敌机对象
        self.enemy_total = 0 #一共出现的敌机总数
        self.enemy_escape = 0 #逃逸的敌机数量
        self.hero = HeroPlane(self.screen) #创建hero飞机对象
        self.boss02 = None

    def battle_start(self):
        self.hero.dispaly()
        hero_control(self.hero) #开始键盘监控

        #利用循环建立4个敌机，如果被打掉，就补充,当满足4个时中断循环，一共会创建elf.enemy_max_num个小敌机
        while self.enemy_total < self.enemy_max_num:
            if len(self.enemy_list) <= 3 :
                self.enemy_list.append(EnemyPlane(self.screen))
                self.enemy_total += 1
                print (len(self.enemy_list),self.enemy_total)

            # 定期出现boss01
            if self.enemy_total in [50,70,90] :
                boss01 = Boss_1(self.screen)
                self.enemy_list.append(boss01)
                self.enemy_total += 1

            #最终出boss02
            if self.enemy_total == 100:
                self.boss02 = Boss_2(self.screen)
                self.enemy_list.append(self.boss02)
                self.enemy_total += 1


            # 当敌机超出窗口，删除该敌机对象,并在将逃逸敌机数量+1
            for enemy_instance in self.enemy_list:
                if enemy_instance.y > 850:
                    self.enemy_list.remove(enemy_instance)
                    self.enemy_escape += 1
            else:
                break

        #显示敌机、启动敌机移动，开启敌机开火，当敌机hp小于0时，删除敌机对象
        for enemy in self.enemy_list:
            enemy.dispaly()
            enemy.move()
            #enemy.fire(EnemyBullet)
            if enemy.hp <= 0:
                self.enemy_list.remove(enemy)

            #当hero子弹击中敌机时减少敌机hp，并删除hero子弹对象
            for hero_bullet in self.hero.bullet_list:
                if ((hero_bullet.x + 11) > enemy.x) \
                        and ((hero_bullet.x + 11) < (enemy.x + enemy.wide)) \
                        and (hero_bullet.y < enemy.y + enemy.high) \
                        and (hero_bullet.y > enemy.y):
                    enemy.hp -= hero_bullet.hurt
                    self.hero.bullet_list.remove(hero_bullet)

            # 当敌机子弹击中hero时减少hero hp
            if self.boss02 != None:
                for boss02_bullet in self.boss02.bullet_list:
                    if ((boss02_bullet.x + 11) > enemy.x) \
                            and ((boss02_bullet.x + 11) < (self.hero.x + self.hero.wide)) \
                            and (boss02_bullet.y < self.hero.y + self.hero.high) \
                            and (boss02_bullet.y > self.hero.y):
                        self.hero.hp -= boss02_bullet.hurt
                        self.boss02.bullet_list.remove(boss02_bullet)

    def game_over(self):
        if self.enemy_escape > 10 or self.hero.hp < 0 :
            return False
        return  True



# 控制hero飞机移动
def hero_control(hero_temp):
    for event in pygame.event.get():  #退出程序
        if event.type == QUIT:
            exit()

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            hero_temp.move_left()  #调取heroplane左移方法

        elif pressed_keys[K_RIGHT]:
            hero_temp.move_right()   #调取heroplane右移方法

        if pressed_keys[K_UP]:
            hero_temp.move_up()   #调取heroplane下移方法

        elif pressed_keys[K_DOWN]:
            hero_temp.move_down()  #调取heroplane上移方法

        elif pressed_keys[K_SPACE]:
            hero_temp.fire(HeroBullet)  #调取heroplane开火方法

def main():
    pygame.init()
    screen = pygame.display.set_mode((480, 852), 0, 32)  #创建游戏窗口
    background = pygame.image.load("./feiji/background.png") #创建游戏背景
    pygame.key.set_repeat(500, 3) #设置持续按键，间隔固定时间重复某一事件
    battle_1 = Battle(screen) #建立战局
    font1 = pygame.font.SysFont('arial',16)
    #aa = Boss_2(screen)
    i = 0
    u = [10*p for p in range(1,1000)]
    #win = pygame.image.load("./feiji/quit_nor.png") #胜利画面
    lose = pygame.image.load("./feiji/lose.jpg") #失败画面


    while True:
        # 设定需要显示的背景图
        screen.blit(background, (0, 0)) #刷新背景
        if battle_1.boss02 != None:
            battle_1.boss02.fire(EnemyBullet,i)
        text = font1.render("Escape: %s"%(battle_1.enemy_escape), True, (0, 0, 0))
        screen.blit(text,(380,20))
        battle_1.battle_start()  #开始战局
        time.sleep(0.01) #延迟0.01毫秒
        #pygame.display.update()
        i +=1
        print(battle_1.hero.hp)
        if battle_1.game_over() == False:
            print ("GAME OVER")
            screen.blit(lose, (100, 300))
        pygame.display.update()

if __name__ == "__main__":
    main()