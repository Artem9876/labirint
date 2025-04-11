from pygame import*
font.init()
window = display.set_mode((700,500))
font1 = font.SysFont('Times New Roman', 70)
win = font1.render('ТЫ ПОБЕДИЛ!',True,(255,0,0))
lose = font1.render('ТЫ ПРОИГРАЛ!',True,(255,0,0))
class GameSprite(sprite.Sprite):
    def __init__(self, picture,w,h,x,y):
        super().__init__()
        self.image = transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def __init__(self,picture,w,h,x,y,x_speed,y_speed):
        super().__init__(picture,w,h,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        if self.x_speed >0:
            if self.rect.right >= 700:
                self.x_speed = 0
        if self.x_speed < 0:
            if self.rect.left <= 0:
                self.x_speed = 0

        self.rect.x += self.x_speed

        walls_touched = sprite.spritecollide(self,walls, False)
        if self.x_speed>0:
            for p in walls_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        if self.x_speed<0:
            for p1 in walls_touched:
                self.rect.left = max(self.rect.left, p1.rect.right)
        if self.y_speed > 0:
            if self.rect.bottom >= 500:
                self.y_speed = 0
        if self.y_speed < 0:
            if self.rect.top <=0:
                self.y_speed = 0
        self.rect.y += self.y_speed
        walls_touched = sprite.spritecollide(self,walls, False)
        if self.y_speed>0:
            for p in walls_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        if self.y_speed<0:
            for p in walls_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    def fire(self):
        bullet = Bullet('jam.png', 15,20, self.rect.right, self.rect.centery, 10)
        bullets.add(bullet) 
class Enemy(GameSprite):
    def __init__(self, picture, w, h, x, y, speed):
        super().__init__(picture,w,h,x,y)
        self.speed = speed
        self.direction = 'top'
    def update(self):
        if self.direction == 'top':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
        if self.rect.y<=120:
            self.direction = 'bottom'
        elif self.rect.y >= 310:
            self.direction = 'top'
class Bullet(GameSprite):
    def __init__(self,picture,w,h,x,y,speed):
        super().__init__(picture,w,h,x,y)
        self.speed = speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700:
            self.kill()
    
bullets = sprite.Group()

                

display.set_caption('Лабиринт')
run = True
finish = False
walls = sprite.Group()
wall = GameSprite('platform_v.png',65,300,200,0)
wall1 = GameSprite('platform_v.png',90,40,130,260)
wall2 = GameSprite('platform_v.png',65,100,200,400)
wall3 = GameSprite('platform_v.png',300,65,200,70)
wall4 = GameSprite('platform_v.png',80,40,250,400)
walls.add(wall, wall1, wall2, wall3, wall4)
minion = Player('minion1.png',100,100,0,0,0,0)
banan = GameSprite('banan.png', 100, 100, 600, 420)
zlodey = Enemy('zlodey1.png', 160,190,430,270,5)
monsters = sprite.Group()
monsters.add(zlodey)
while run:
    for ev in event.get():
        if ev.type == QUIT:
            run = False
        elif ev.type == KEYDOWN:
            if ev.key == K_SPACE:
                minion.fire()
            if ev.key == K_w:
                minion.y_speed = -5
            elif ev.key == K_s:
                minion.y_speed = 5
            elif ev.key == K_a:
                minion.x_speed = -5
            elif ev.key == K_d:
                minion.x_speed = 5
        elif ev.type == KEYUP:
            if ev.key == K_w:
                minion.y_speed = 0
            elif ev.key == K_s:
                minion.y_speed = 0
            elif ev.key == K_a:
                minion.x_speed = 0
            elif ev.key == K_d:
                minion.x_speed = 0
    if finish == False:
        window.fill((3,192,60))
        minion.update()
        minion.reset()
        banan.reset()
        monsters.draw(window)
        monsters.update()
        walls.draw(window)
        bullets.update()
        bullets.draw(window)
        sprite.groupcollide(bullets, walls, True, False)
        if len(sprite.groupcollide(bullets, monsters, True, True))>0:
            zlodey.rect.x = 900
      
        if sprite.collide_rect(minion,banan):
            finish = True
            window.blit(win,(100,180))
        if sprite.collide_rect(minion,zlodey):
            finish = True
            window.blit(lose,(100,180))

    time.delay(50)
        
        
    display.update()



