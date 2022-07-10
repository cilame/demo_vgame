import time
import random

import vgame

# vgame.DEBUG = True
# vgame.Map.DEBUG = True

import os, sys
def base_path(path):
    return os.path.join(sys._MEIPASS if getattr(sys, 'frozen', None) else os.path.dirname(__file__), path)

path = base_path('source/image')
mpath = base_path('source/music')

window = vgame.Initer(size=(400, 600))
main = vgame.Theater(path+'/background.png',size=(480, 600))
pause = vgame.Theater(path+'/background.png',size=(480, 600))
death = vgame.Theater(path+'/background.png',size=(480, 600))

vgame.Anime(vgame.Text(0, textcolor=(255,0,0), textformat='方向键：WASD；子弹：J', textscale=2)).local(main, (160,40))
label = vgame.Anime(vgame.Text(0, textside='r', textwidth=150, textcolor=(255,0,0), textformat='分数:{:>3d}', textscale=2)).local(main, (160,15))
label_info = vgame.Anime(vgame.Text(0, textcolor=(255,0,0), textformat='生存时间:{:f}', textscale=2)).local(main, (160,65))
label_level = vgame.Anime(vgame.Text(1, textcolor=(255,0,0), textformat='难度等级:{:d}', textscale=2)).local(main, (160,90))

unpause = vgame.Button(vgame.Text('暂停')).local(pause, (window.size[0]/2, window.size[1]/2))
restart = vgame.Button(vgame.Text('重开')).local(death, (window.size[0]/2, window.size[1]/2))
label_info.local(restart, (160,65))

unpause.click = lambda: vgame.change_theater(main)
unpause.control = lambda self, c:unpause.click() if self.delay(c and c.get('p1')[1]) else None

def _restart():
    global main_time
    main_time = time.time()
    for i in main.Enemy: 
        i.kill()
        if i.status['bgbar']:i.status['bgbar'].kill()
        if i.status['hpbar']:i.status['hpbar'].kill()
    for i in main.Bullet: i.kill()
    label.text = 0
    vgame.change_theater(main)
    player.local(main, init_local)
restart.click = _restart
restart.control = lambda self, c: _restart() if self.delay(c and c.get('p1')[1]) else None

try:
    bg_music = vgame.Music(mpath + '/game_music.wav', .2).play(-1)
    bullet_player = vgame.Music(mpath + '/bullet.wav', .2)
    enemy0_dplayer = vgame.Music(mpath + '/enemy0_down.wav', .3)
except:
    class temp:
        def play(*a,**kb):pass
    bullet_player = temp
    enemy0_dplayer = temp

player_imgs = [
    path+'/hero1.png',
    path+'/hero2.png',
]
init_local = (window.size[0]/2,window.size[1]-62)
main_time = time.time()
player = vgame.Player(player_imgs, rate=200, showsize=(50, 62)).local(main, init_local).follow(main, .2)
player.direction = lambda self, d: self.mover.move(d.get('p1'), 6)
def control(self, c):
    if self.delay(c and c.get('p1')[0], time=100, repeat=True): create_bullet()
    if self.delay(c and c.get('p1')[1]): vgame.change_theater(pause)
player.control = control

enemy0_dead = [path+'/enemy0_down1.png',path+'/enemy0_down2.png',path+'/enemy0_down3.png',path+'/enemy0_down4.png',]
enemy1_dead = [path+'/enemy1_down1.png',path+'/enemy1_down2.png',path+'/enemy1_down3.png',path+'/enemy1_down4.png',]
enemy2_dead = [path+'/enemy1_down1.png',path+'/enemy1_down2.png',path+'/enemy1_down3.png',path+'/enemy1_down4.png',]
hero_blowup = [path+'/hero_blowup_n1.png',path+'/hero_blowup_n2.png',path+'/hero_blowup_n3.png',path+'/hero_blowup_n4.png',]
def get_level():
    ttime = time.time() - main_time
    if ttime < 5:
        lv = 1; ticket = 200; speed_lv = 0
    elif ttime < 10:
        lv = 2; ticket = 150; speed_lv = 2
    else:
        lv = 3; ticket = 50; speed_lv = 4
    return lv, ticket, speed_lv, ttime

def enemy_creater(self):
    lv, ticket, speed_lv, ttime = get_level()
    label_info.text = ttime
    label_level.text = lv
    if self.delay(True, time=ticket, repeat=True):
        if random.randint(0, 10) <= 6:
            x, y, speed, enemysize, enemy_dead, score = random.randint(15, main.size[0]-15), 30, random.randint(2, 7) + speed_lv, (25,20), enemy0_dead, 100
            angle = random.randint(-5, 5)
            raise_num = (random.random()-0.5) * 0.1
            enemy = vgame.Enemy(path+'/enemy0.png', showsize=enemysize).local(main, (x, y))
            enemy.status['hp'] = 3
            enemy.status['maxhp'] = 3
            enemy.status['bgbar'] = vgame.Anime((0,0,0), showsize=(enemy.showsize[0], 3)).local(main, (x, y-15))
            enemy.status['hpbar'] = vgame.Anime((0,255,0), showsize=(enemy.showsize[0], 3)).local(main, (x, y-15))
        elif random.randint(0, 10) <= 8:
            x, y, speed, enemysize, enemy_dead, score = random.randint(15, main.size[0]-15), 30, random.randint(2, 4) + speed_lv, (35,45), enemy1_dead, 300
            angle = random.randint(-15, 15)
            raise_num = (random.random()-0.5) * 0.5
            enemy = vgame.Enemy(path+'/enemy1.png', showsize=enemysize).local(main, (x, y))
            enemy.status['hp'] = 7
            enemy.status['maxhp'] = 7
            enemy.status['bgbar'] = vgame.Anime((0,0,0), showsize=(enemy.showsize[0], 3)).local(main, (x, y-25))
            enemy.status['hpbar'] = vgame.Anime((0,255,0), showsize=(enemy.showsize[0], 3)).local(main, (x, y-25))
        elif random.randint(0, 10) <= 10:
            x, y, speed, enemysize, enemy_dead, score = random.randint(15, main.size[0]-15), 30, random.randint(1, 3) + speed_lv, (60,100), enemy1_dead, 800
            angle = random.randint(-30, 30)
            raise_num = (random.random()-0.5)
            enemy = vgame.Enemy(path+'/enemy2.png', showsize=enemysize).local(main, (x, y))
            enemy.status['hp'] = 25
            enemy.status['maxhp'] = 25
            enemy.status['bgbar'] = vgame.Anime((0,0,0), showsize=(enemy.showsize[0], 3)).local(enemy, offsets=(0,-60))
            enemy.status['hpbar'] = vgame.Anime((0,255,0), showsize=(enemy.showsize[0], 3)).local(enemy, offsets=(0,-60))
        else:
            return
        def idle(self):
            nonlocal angle
            angle += raise_num
            self.mover.move_angle(90+angle, speed)
            self.status['hpbar'].mover.move_angle(90+angle, speed)
            self.status['bgbar'].mover.move_angle(90+angle, speed)
            if self.outbounds():
                self.status['hpbar'].kill()
                self.status['bgbar'].kill()
                self.kill()
            v = self.collide(vgame.Bullet)
            if v:
                v[0].kill()
                self.status['hp'] -= 2
                if self.status['hp'] <= 0:
                    self.kill()
                    self.status['hpbar'].kill()
                    self.status['bgbar'].kill()
                    label.text += score
                    deadanime = vgame.Anime(enemy_dead, rate=50, showsize=enemysize, loop=1).local(main, self.rect.center)
                    enemy0_dplayer.play()
                else:
                    if self.status['hpbar']: 
                        barlen = int(self.status['hp']*self.showsize[0]/self.status['maxhp'])
                        color = (0,255,0) if barlen/self.showsize[0] > 0.3 else (255,0,0)
                        self.status['hpbar'].imager = vgame.Image(color, showsize=(barlen, 3))
            v = self.collide(vgame.Player)
            if v:
                self.status['hpbar'].kill()
                self.status['bgbar'].kill()
                v[0].kill(); self.kill()
                enemy0_dplayer.play()
                anime = vgame.Anime(hero_blowup, rate=100, showsize=(50, 62), loop=1).local(main, v[0].rect.center)
                anime.endanime = lambda :vgame.change_theater(death)
        enemy.idle = idle
        enemy.in_entity = False

label.idle = enemy_creater

def create_bullet():
    x, y = player.rect.center
    def one(dx, ag=0, dy=0):
        bullet = vgame.Bullet(path+'/bullet1.png', showsize=(4, 10)).local(main, (x+dx, y-15))
        def idle(self):
            if self.outbounds():
                self.kill()
            self.mover.move_angle(ag-90, 10)
        bullet.idle = idle
        bullet.rotate = ag
        bullet_player.play()
    def two(): one(-10) or one(10)
    def three(): one(-15,-15) or one(0) or one(15,15)
    def five(): one(-20,-20) or one(-10,-10) or one(0,0) or one(10,10) or one(20,20)
    if label.text > 1000: five()
    elif label.text > 500: three()
    elif label.text > 0: two()
    else: one(0)
