import pygame

pygame.init() 

import pygame
import random
from math import sqrt

screen = pygame.display.set_mode((1000,1000))
screen.fill((130,125,120))
pygame.font.init()

myfont = pygame.font.SysFont('Comic Sans MS', 30)
myfont2= pygame.font.SysFont('Comic Sans MS', 16)

x=475
y=475
  
screenwidth=1000
screenheight=800
number_of_objects=0
number_of_buttons=0

collision= False
xpos=[0]
ypos=[0]
objectwidth=[0]
objectheight=[0]

gridon = False

phase=0 ###phase tells the game what round it's on
fighting=False

gold=4

shottimerrange=400

placing_tile=False
tiledown=True

shotcount=0

gamestart=False

clock=pygame.time.Clock() ###Measure framerate
fastspeed=10
normalspeed=6
globalspeed= normalspeed ###(adjusts for speed, does not currently function because only affects initialization)
vel=.5*globalspeed

pos=[0,0]

thinglist=[]
zombiecount=0

globaldelay=0

def zombiedead(i):
    global gold
    goldchance= random.choice(range(100))
    if goldchance>50: ###Goldchance
        gold+=zombielist[i].gold
    del zombielist[i]
    global zombiecount
    zombiecount-=1

def displayintro():
        textsurface= myfont.render(f'Welcome to Zombiegame by Todd!', False, (0, 0, 0))
        screen.blit(textsurface,(250, 50))
        textsurface= myfont2.render(f"You are tasked with defending humanity's last fortress from oncoming zombies", False, (0, 0, 0))
        screen.blit(textsurface,(100, 120))
        textsurface= myfont2.render(f'You will be able to buy soldiers from the shop with gold.', False, (0, 0, 0))
        screen.blit(textsurface,(100, 150))
        textsurface= myfont2.render(f'After that, you can move the soldier around with the mouse and put the tile down', False, (0, 0, 0))
        screen.blit(textsurface,(100, 180))
        textsurface= myfont2.render(f'You can then place the soldier by pressing the place button or pressing SPACE', False, (0, 0, 0))
        screen.blit(textsurface,(100, 210))
        textsurface= myfont2.render(f'You can also delete the soldier by pressing the delete button or pressing BACKSPACE', False, (0, 0, 0))
        screen.blit(textsurface,(100, 240))
        textsurface= myfont2.render(f'Once you are satisfied, press the start button, and zombies will attack from the top of the screen', False, (0, 0, 0))
        screen.blit(textsurface,(100, 270))
        textsurface= myfont.render(f'Good luck! press ENTER to start', False, (0, 0, 0))
        screen.blit(textsurface,(250, 310))

def round25(x):
    rounded=round(x/25)
    rounded= 25*rounded
    return rounded

class object():
    def __init__(self, ID):
        self.ID=ID
        self.center= [round(self.x+self.width/2), round(self.y+self.height/2)]
        self.img=pygame.transform.scale(self.img, (self.width,self.height))
        self.surf=self.img
        self.hitbox=(self.x, self.y,self.width,self.height) ###delete??

        ###Shooting calculations
        self.shooting=False
        shottimerrange=400
        self.shottimer=random.choice(range(1, shottimerrange))
        self.shootingat=-1
        self.startfiringprocess=False
        self.startmoving=False
        self.explosions=[]
        self.projectiles=[]

        self.right=True
        self.up=False
        self.down=False
    
    def draw(self):
        self.surf=self.img
        screen.blit(self.surf, (self.x,self.y))
    
    def drawhpbox(self):
        if self.maxhp<=40:
            maxhp=self.maxhp
        else:
            maxhp=40
        hpoutline= (self.center[0]-maxhp-6, self.y-15, maxhp*2+12, round(maxhp/4)+10)
        if self.hp>=0:
            hpbox= (self.center[0]-maxhp-6, self.y-15, (maxhp*2+12)*(self.hp/self.maxhp), round(maxhp/4)+10)
        else:
            hpbox= (0,0,0,0)
        if self.good:
            pygame.draw.rect(screen, (0,150,0), hpbox , 0)
        else:
            pygame.draw.rect(screen, (150,0,50), hpbox , 0)
        pygame.draw.rect(screen, (255,255,255), hpoutline , 3)

    
class defenseobject(object):
    def __init__(self, ID):
        self.x=475
        self.y=475
        self.vel=3
        self.right=True
        self.up=False
        self.down=False
        self.good=True
        super().__init__(ID)

    def moveobjectmouse(self):
        screenlowerbound=300
        pos=pygame.mouse.get_pos()
        self.x=pos[0]-self.width/2
        self.y=pos[1]-self.height/2

        if self.x<=0:
            self.x=0
        if self.x+self.width>=screenwidth:
            self.x=screenwidth-self.width
        if self.y<=screenlowerbound:
            self.y=screenlowerbound
        if self.y+self.height>=screenheight:
           self.y=screenheight-self.height

        self.center= [round(self.x+self.width/2), round(self.y+self.height/2)]

    def drawsoldier(self):
        if self.right:
            if self.up:
                self.img=pygame.transform.scale(self.imglist[1], (self.width,self.height))
            elif self.down:
                self.img=pygame.transform.scale(self.imglist[5], (self.width,self.height))
            else:
                self.img=pygame.transform.scale(self.imglist[0], (self.width,self.height))
        elif not self.right:
            if self.up:
                self.img=pygame.transform.scale(self.imglist[2], (self.width,self.height))
            elif self.down:
                self.img=pygame.transform.scale(self.imglist[4], (self.width,self.height))
            else:
                self.img=pygame.transform.scale(self.imglist[3], (self.width,self.height))
        self.surf=self.img           
        screen.blit(self.surf, (self.x,self.y))

    def drawhitbox(self, screen):
        self.hitbox=(round25(self.x), round25(self.y),self.width,self.height)
        pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
    def drawrange(self, screen):
        if self.range>0:
            pygame.draw.circle(screen, (255,0,0), self.center, self.range, 2)
            if self.type=='longrange':
                pygame.draw.circle(screen, (255,0,0), self.center, self.innerrange, 2)

    def collisioncheck(self):
        colliding=False
        for i in range(len(thinglist)-1):
            if round25(self.x)-thinglist[i].x<thinglist[i].width and thinglist[i].x-round25(self.x)<self.width and round25(self.y)-thinglist[i].y<thinglist[i] .height and thinglist[i].y-round25(self.y)<self.height:
                colliding=True
        return colliding
        
    def zombieshottrack(self): ### some redundancy here
        if self.type!='terrain' and fighting:
            self.shooting=False
            self.aiming=False
            self.right=True
            self.up=False
            self.down=False
            distlist=[]
            indexlist=[] ###Could use dictionary
            if self.type=='shortrange':
                self.target=self.range
            elif self.type=='longrange':
                self.target=self.innerrange
            for i in range(zombiecount):
                if zombielist[i].startmoving:
                    a= (self.center[0]-zombielist[i].center[0])**2 + (self.center[1]-zombielist[i].center[1])**2
                    centerdistance=sqrt(a)
                    if self.type=='areadmg':
                        if centerdistance<=self.range:
                            distlist.append(centerdistance)
                            indexlist.append(i)
                    elif self.type=='shortrange':
                        if centerdistance<=self.target:
                            self.target=centerdistance
                            index=i
                            self.aiming=True
                    elif self.type=='longrange':
                        if centerdistance>=self.target and centerdistance<=self.range:
                            self.target=centerdistance
                            index=i
                            self.aiming=True
            if self.type!="areadmg" and self.aiming:          
                i=index
                xdif=self.center[0]-zombielist[i].center[0]
                ydif=self.center[1]-zombielist[i].center[1]
                traveldist=self.target
                ###Tells soldiers what direction to aim
                if xdif>=0:
                    self.right=False
                if zombielist[i].y<self.y-zombielist[i].range*.5:
                    self.up=True
                if zombielist[i].y>self.y+self.range*.5:
                    self.down=True

                if not self.splash:
                    ###Shooting calculations
                    self.shottimer+=self.firerate
                    if self.shottimer>=shottimerrange: ##Rate of zombie getting hit
                        self.shooting=True
                        self.shootingat=zombielist[i].ID
                        self.shottimer=self.shottimer%shottimerrange
                
            if self.splash and self.type!='areadmg':
                if self.firerate<10:
                    self.shottimer+=self.firerate
                    if self.aiming:
                        if self.shottimer>=shottimerrange*(1-self.firerate/20)-traveldist/self.projectilespeed and self.shottimer<shottimerrange*(1-self.firerate/20)-traveldist/self.projectilespeed+self.firerate and not self.startfiringprocess:
                            self.traveldistsplash=sqrt(xdif**2+ydif**2)
                            self.xdifsplash=xdif
                            self.ydifsplash=ydif
                            self.startfiringprocess=True
                            self.explosions=[]
                            self.projectiles=[]
                            for i in range(len(self.splashes)):
                                self.explosions.append(splash((self.center[0]-self.splashes[i]*self.xdifsplash)-self.splashradius[i]/2, (self.center[1]-self.splashes[i]*self.ydifsplash)-self.splashradius[i]/2, self.splashradius[i],self.dmg)) ###Make the explosions cntered
                                self.projectiles.append(projectile(self.center[0]-self.pwidth/2, self.center[1]-self.pheight/2, self.pwidth, self.pheight, self.projectileimg, self.projectilespeed))

                            self.timetotravel=self.traveldistsplash/self.pspeed
                    if self.startfiringprocess:
                        if self.shottimer>=shottimerrange*(1-self.firerate/20)-self.traveldistsplash/self.projectilespeed and self.shottimer<shottimerrange*(1-self.firerate/20) and len(self.projectiles)>0:
                            for i in self.projectiles:
                                i.x-=self.xdifsplash/self.timetotravel
                                i.y-=self.ydifsplash/self.timetotravel ##Right now, the projectilespeed is proportionate to the firerate
                                i.draw()

                        elif self.shottimer>=shottimerrange*(1-self.firerate/20) and self.shottimer<shottimerrange*(1-self.firerate/20)+self.firerate and len(self.explosions)>0:
                            self.shooting=True
                            for i in self.explosions:
                                i.shooting=True
                                i.zombieshottrack()
                                i.draw()
                            self.projectiles=[]

                    if self.shottimer>=shottimerrange*(1-self.firerate/20)+self.firerate:
                        self.shooting=False
                        if len(self.explosions)>0:
                            for i in self.explosions:
                                i.shooting=False
                                i.draw()
                if self.shottimer>=shottimerrange:
                    self.shottimer=0
                    self.explosions=[]
                    self.startfiringprocess=False
                
            if self.type=='areadmg':
                for j in indexlist:
                    zombielist[j].hp-=self.dmg
                    
###Classes
class castle(defenseobject):
    def __init__(self, ID):
        self.width=150
        self.height=150
        self.img=pygame.image.load(r'image/fortress.png')
        self.range=0
        ###needs range function
        self.maxhp=40
        self.hp=self.maxhp
        self.vel=3
        super().__init__(ID)
        self.type='terrain'
        self.splash=False

class soldier(defenseobject):
    def __init__(self, ID):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/soldierR.png')
        self.range=180
        self.maxhp=20
        self.hp=self.maxhp
        self.dmg=2
        self.firerate=10
        super().__init__(ID)
        self.imglist=[pygame.image.load(r'image/soldierR.png'), pygame.image.load(r'image/soldierTR.png'),pygame.image.load(r'image/soldierTL.png'), pygame.image.load(r'image/soldierL.png'), pygame.image.load(r'image/soldierBL.png'), pygame.image.load(r'image/soldierBR.png')]
        self.cost=1
        self.good=True
        self.type='shortrange'
        self.splash=False
        self.description=''

class wall(defenseobject):
    def __init__(self, ID):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/barbed-wire.png')
        self.imglist=[]
        for i in range(6):
            self.imglist.append(pygame.image.load(r'image/barbed-wire.png'))
        self.range=0
        self.maxhp=120
        self.hp=self.maxhp
        self.dmg=0
        self.firerate=0
        super().__init__(ID)
        self.cost=2
        self.good=True
        self.type='terrain'
        self.splash=False
        self.description='Great for tanking zombies'

class machinegun(defenseobject):
    def __init__(self, ID):
        self.width=75
        self.height=75
        self.img=pygame.image.load(r'image/MGR.png')
        self.imglist=[pygame.image.load(r'image/MGR.png'),pygame.image.load(r'image/MGTR.png'),pygame.image.load(r'image/MGTL.png'),pygame.image.load(r'image/MGL.png'),pygame.image.load(r'image/MGBL.png'),pygame.image.load(r'image/MGBR.png')]
        self.range=175
        self.maxhp=5
        self.hp=self.maxhp
        self.dmg=1
        self.firerate=60
        super().__init__(ID)
        self.cost=3
        self.type='shortrange'
        self.splash=False
        self.description='High Firerate, quite vulnerable'

class sniper(defenseobject):
    def __init__(self, ID):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/sniperR.png')
        self.imglist=[pygame.image.load(r'image/sniperR.png'),pygame.image.load(r'image/sniperTR.png'),pygame.image.load(r'image/sniperTL.png'),pygame.image.load(r'image/sniperL.png'),pygame.image.load(r'image/sniperBL.png'),pygame.image.load(r'image/sniperBR.png')]
        self.range=320
        self.innerrange=100
        self.maxhp=5
        self.hp=self.maxhp
        self.dmg=75
        self.firerate=1
        super().__init__(ID)
        self.cost=2
        self.type='longrange'
        self.splash=False
        self.description='Long range damage, quite vulnerable'

class grenadier(defenseobject):
    def __init__(self, ID):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/grenadierR.png')
        self.range=180
        self.maxhp=20
        self.hp=self.maxhp
        self.dmg=9
        self.firerate=4
        super().__init__(ID)
        self.imglist=[pygame.image.load(r'image/grenadierR.png'), pygame.image.load(r'image/grenadierTR.png'),pygame.image.load(r'image/grenadierTL.png'), pygame.image.load(r'image/grenadierL.png'), pygame.image.load(r'image/grenadierBL.png'), pygame.image.load(r'image/grenadierBR.png')]
        self.cost=4
        self.type='shortrange'
        self.splash=True
        self.splashes=[1]
        self.splashradius=[100]
        self.description='Does damage in an area'
        ##Projectileinfo
        self.projectileimg=pygame.image.load(r'image/grenade.png')
        self.pwidth=25
        self.pheight=25
        self.projectileimg=pygame.transform.scale(self.projectileimg, (self.pwidth,self.pheight))
        self.projectilespeed=5
        self.pspeed=self.projectilespeed*self.firerate

class artillery(defenseobject):
    def __init__(self, ID):
        self.width=100
        self.height=100
        self.img=pygame.image.load(r'image/artilleryR.png')
        self.range=500
        self.innerrange=150
        self.maxhp=2
        self.hp=self.maxhp
        self.dmg=35
        self.firerate=1.5##Change!
        super().__init__(ID)
        self.imglist=[pygame.image.load(r'image/artilleryR.png'), pygame.image.load(r'image/artilleryTR.png'),pygame.image.load(r'image/artilleryTL.png'), pygame.image.load(r'image/artilleryL.png'), pygame.image.load(r'image/artilleryBL.png'), pygame.image.load(r'image/artilleryBR.png')]
        self.cost=8##Change
        self.type='longrange'
        self.splash=True
        self.splashes=[1]
        self.splashradius=[180]
        self.description='Does massive damage in an area'
        ##Projectileinfo
        self.projectileimg=pygame.image.load(r'image/grenade.png')
        self.pwidth=5
        self.pheight=5
        self.projectileimg=pygame.transform.scale(self.projectileimg, (self.pwidth,self.pheight))
        self.projectilespeed=3
        self.pspeed=self.projectilespeed*self.firerate

class projectile(defenseobject):
    def __init__(self, x, y, width, height, img, speed):
        ID=-1
        self.width=width
        self.height=height
        self.img=pygame.transform.scale(img, (width,height))
        self.vel=speed
        super().__init__(ID)
        self.x=x
        self.y=y

class splash(defenseobject):
    def __init__(self, x, y, radius, dmg):
        ID=-1
        self.dmg=dmg
        self.vel=0
        self.radius=radius
        self.width=self.radius
        self.height=self.radius
        self.range=self.radius
        self.img=pygame.image.load(r'image/explode.png')
        self.type='areadmg'
        self.splash=False
        super().__init__(ID)
        self.x=x
        self.y=y
        self.center= [round(self.x+self.width/2), round(self.y+self.height/2)]

###ZOMBIES
class zombie(object):
    def __init__(self, ID):
        self.x=random.choice(range(-200,1150))
        self.y=-100
        self.delay=random.choice(range(400+zombiecount))
        super().__init__(ID)
        self.spawnlocatedistancex=(thinglist[0].center[0]-(self.width/2))-self.x
        self.spawnlocatedistancey=(thinglist[0].center[1]-(self.height/2))-self.y
        self.shot=0
        self.good=False
        self.xvec=self.spawnlocatedistancex/sqrt((self.spawnlocatedistancex**2)+(self.spawnlocatedistancey**2))
        self.yvec= self.spawnlocatedistancey/sqrt((self.spawnlocatedistancex**2)+(self.spawnlocatedistancey**2))
       
    def zombiemove(self):
        self.center= [round(self.x+self.width/2), round(self.y+self.height/2)]
        distlist=[]
        movement=True
        if globaldelay>=self.delay:
            self.startmoving=True
            for i in range(number_of_objects):
                a= (self.center[0]-thinglist[i].center[0])**2 + (self.center[1]-thinglist[i].center[1])**2
                centerdistance=sqrt(a)
                distlist.append(centerdistance)
            centerdistance=min(distlist)
            i=distlist.index(centerdistance)
            if centerdistance<=self.range:
                movement= False
                if thinglist[i].hp>=0.1: ####Damage Computation
                    thinglist[i].hp-=self.dmg/1000       
            if movement:
                self.x+=.4*self.xvec* self.vel
                self.y+=.4*self.yvec* self.vel
    
    def zombiehealth(self):
        self.gotshot=False
        if self.startmoving:
            for j in thinglist:
                if j.shooting and j.shootingat==self.ID:
                    self.gotshot=True
                    self.img= self.imglist[1]
                    self.hp-=j.dmg
            if not self.gotshot:
                self.img= self.imglist[0]

class starterzombie(zombie):
    def __init__(self, ID):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/zombie.png')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/zombie.png'), (self.width,self.height)), pygame.transform.scale(pygame.image.load(r'image/zombieshot.png'), (self.width,self.height))]
        self.range=75
        self.maxhp=12
        self.hp=self.maxhp
        self.dmg=4.5*globalspeed
        self.gold=1
        self.vel=3
        super().__init__(ID)

class betterzombie(zombie):
    def __init__(self, ID):
        self.width=60
        self.height=60
        self.img=pygame.image.load(r'image/zombie.png')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/zombie.png'), (self.width,self.height)), pygame.transform.scale(pygame.image.load(r'image/zombieshot.png'), (self.width,self.height))]
        self.range=80
        self.maxhp=20
        self.hp=self.maxhp
        self.dmg=6*globalspeed
        self.gold=1
        self.vel=3
        super().__init__(ID)

class bosszombie(zombie):
    def __init__(self, ID):
        self.width=125
        self.height=125
        self.img=pygame.image.load(r'image/zombie.png')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/zombie.png'), (self.width,self.height)), pygame.transform.scale(pygame.image.load(r'image/zombieshot.png'), (self.width,self.height))]
        self.range=100
        self.maxhp=4000
        self.hp=self.maxhp
        self.dmg=10*globalspeed
        self.gold=10
        self.vel=1.5
        super().__init__(ID)
        #self.round?

class zombieimp(zombie):
    def __init__(self, ID):
        self.width=25
        self.height=25
        self.img=pygame.image.load(r'image/babyzombie.png')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/babyzombie.png'), (self.width,self.height)), pygame.transform.scale(pygame.image.load(r'image/babyzombieshot.png'), (self.width,self.height))]
        self.range=50
        self.maxhp=7
        self.hp=self.maxhp
        self.dmg=20*globalspeed
        self.gold=0
        self.vel=6 ###Maybe do when initiating?
        super().__init__(ID)
        self.delay=self.delay+400
        
class zombietank(zombie):
    def __init__(self, ID):
        self.width=75
        self.height=75
        self.img=pygame.image.load(r'image/zombietank.png')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/zombietank.png'), (self.width,self.height)), pygame.transform.scale(pygame.image.load(r'image/zombietankshot.png'), (self.width,self.height))]
        self.range=85
        self.maxhp=100
        self.hp=self.maxhp
        self.dmg=7*globalspeed
        self.gold=1
        self.vel=2
        super().__init__(ID)
        
class zombieimprange(zombie):
    def __init__(self, ID):
        self.width=25
        self.height=25
        self.img=pygame.image.load(r'image/zombieimprange.jpg')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/zombieimprange.jpg'), (self.width,self.height)), pygame.transform.scale(pygame.image.load(r'image/zombieimprangeshot.jpg'), (self.width,self.height))]
        self.range=130
        self.maxhp=15
        self.hp=self.maxhp
        self.dmg=12*globalspeed
        self.gold=1
        self.vel=12.5 ###Maybe do when initiating?
        super().__init__(ID)
        self.delay=self.delay+400

class button():
    def __init__(self):
        self.width=40
        self.height=40
    
    def draw(self):
        if (phase>self.round) or (phase==self.round and not fighting):
            self.img=pygame.transform.scale(self.img, (self.width,self.height))
            pygame.draw.rect(screen, (0,0,0),self.rect, 2)
            screen.blit(self.img, (self.x,self.y))
            self.textsurface= myfont2.render(f'Cost: {self.soldier.cost}', False, (0, 0, 0))
            screen.blit(self.textsurface, (self.x,self.y+self.height+10))
          
    def clickedon(self, pos):
        if phase>=self.round:
            if self.rect.collidepoint(pos):
                return True
            else:
                return False
        else:
            return False

    def goldcheck(self):
        if gold-self.soldier.cost<0:
            ####Display text: Can't buy
            return False
        else:
            return True

    def spawnthing(self):
        global gold
        global number_of_objects
        thinglist.append(self.soldier)
        gold-=self.soldier.cost
        number_of_objects+=1
    
    def showinfo(self):
        text1=myfont.render(f'DMG: {self.soldier.dmg}', False, (0, 0, 0))
        text2=myfont.render(f'ATKSPD: {self.soldier.firerate}', False, (0, 0, 0))
        text3=myfont.render(f'HP: {self.soldier.hp}', False, (0, 0, 0))
        text4=myfont2.render(f'{self.soldier.description}', False, (0, 0, 0))
        yinfo=850
        pygame.draw.rect(screen, (200,160,40), (15,yinfo-250-10, 235, 200),0 )
        screen.blit(text1, (20,yinfo-250))
        screen.blit(text2, (20,yinfo-200))
        screen.blit(text3, (20,yinfo-150))
        screen.blit(text4, (20,yinfo-100))
        
    def drawfuncbutton(self):
        pygame.draw.rect(screen, self.color,self.rect, 2)
        self.textsurface= myfont2.render(f'{self.func}', False, (0, 0, 0))
        screen.blit(self.textsurface, (self.x+20,self.y+5))

class startbutton(button):
    def __init__(self):
        button.__init__(self)
        self.x=875
        self.y=930
        self.height=40
        self.width=75
        self.color=(255,0,0)
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.func= 'Start'
        self.round= 0
class placebutton(button):
    def __init__(self):
        button.__init__(self)
        self.x=100
        self.y=930
        self.height=40
        self.width=75
        self.color=(0,255,0)
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.func= 'Place'
        self.round= 0
class deletebutton(button):
    def __init__(self):
        button.__init__(self)
        self.x=200
        self.y=930
        self.height=40
        self.width=75
        self.color= (255,0,0)
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.func= 'Delete'
        self.round= 0

class button1(button):
    def __init__(self):
        button.__init__(self)
        self.x=20
        self.y=820
        self.soldier=soldier(number_of_objects)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 0

class button2(button):
    def __init__(self):
        button.__init__(self)
        self.x=80
        self.y=820
        self.soldier=wall(number_of_objects)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 1

class button3(button):
    def __init__(self):
        button.__init__(self)
        self.x=140
        self.y=820
        self.soldier=machinegun(number_of_objects)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 2

class button4(button):
    def __init__(self):
        button.__init__(self)
        self.x=200
        self.y=820
        self.soldier=sniper(number_of_objects)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 2

class button5(button):
    def __init__(self):
        button.__init__(self)
        self.x=260
        self.y=820
        self.soldier=grenadier(number_of_objects)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 3

class button6(button):
    def __init__(self):
        button.__init__(self)
        self.x=320
        self.y=820
        self.soldier=artillery(number_of_objects)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 4##Change

thinglist.append(castle(-1))

def drawscreen():   ##Drawscreen draws the object to the screen
    screen.fill((130,125,120)) ##Screen color
    if not gamestart:
        ###Info text
        displayintro()
    if gamestart:
    ###Create grid lines
        if gridon and not fighting:
            for i in range(0,screenwidth, 25):
                pygame.draw.line(screen, (0,0,0), [i,0], [i,screenheight], 1)
            for i in range(0,screenheight, 25):   
                pygame.draw.line(screen, (0,0,0), [0,i], [screenwidth,i], 1)

    ###Create a sidebar
        pygame.draw.rect(screen, (255,255,255), (0,screenheight,screenwidth,200), 0)
        for i in buttonlist:
            i.draw() #Button
            if i.info==True:
                i.showinfo()
        textsurface= myfont.render(f'Gold: {gold}', False, (0, 0, 0))
        screen.blit(textsurface,(850, 870)) #show gold
        textsurface= myfont.render(f'Round: {phase}', False, (0, 0, 0))
        screen.blit(textsurface,(850, 825)) #show gold
        if not placing_tile and not fighting:
            start.drawfuncbutton()
        elif placing_tile and not fighting:
            place.drawfuncbutton()
            if number_of_objects>=2:
                delete.drawfuncbutton()
        
        if fighting:
            for i in range(zombiecount):
                zombielist[i].zombiemove()
                zombielist[i].draw()
                zombielist[i].drawhpbox()
   
        if placing_tile and not fighting:
            ##obsolete with mouse feature (thinglist[number_of_objects-1].moveobject()) ##This line ensures that only the most recent object is allowed to move
            if number_of_objects>=2:
                thinglist[number_of_objects-1].drawrange(screen) 
        for i in range(number_of_objects):
            if i!=0:
                if fighting:
                    thinglist[i].zombieshottrack()
                    
                thinglist[i].drawsoldier() ##Draws all objects that have been created
            if not fighting:
                thinglist[i].drawhitbox(screen) 
            else:
                thinglist[i].drawhpbox()
        thinglist[0].draw()
        if fighting:
            for zombie in zombielist:
                zombie.zombiehealth()

        clock.tick(40)
                
    pygame.display.update()

running=True
while running:

    if number_of_objects>=2:
        if thinglist[number_of_objects-1].collisioncheck() and placing_tile == True:
            collision= True
        else:
            collision= False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_g and not fighting: ###press g to turn on grid overlay
                gridon = not gridon

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT]: ###NEEDS WORK
            globalspeed= fastspeed
        if event.type== pygame.KEYUP:
            if event.key==pygame.K_LSHIFT or event.key==pygame.K_RSHIFT:
                globalspeed=normalspeed
        
        if not fighting:
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    if number_of_objects==0 and phase==0 and gamestart==False:
                        gamestart=True
                        number_of_objects+=1
                        placing_tile=True
                        tiledown=False
                        ###Initialize buttons here!
                        start=startbutton()
                        place=placebutton()
                        delete=deletebutton()
                        buttonlist=[]
                        b1=button1()
                        buttonlist.append(b1)
                        b2=button2()
                        buttonlist.append(b2)
                        b3=button3()
                        buttonlist.append(b3)
                        b4=button4()
                        buttonlist.append(b4)
                        b5=button5()
                        buttonlist.append(b5)
                        b6=button6()
                        buttonlist.append(b6)
                        number_of_buttons= len(buttonlist)
                 
            if (event.type==pygame.MOUSEBUTTONUP or event.type==pygame.KEYDOWN) and gamestart==True:   
                pos=pygame.mouse.get_pos()

                if (start.clickedon(pos) and event.type==pygame.MOUSEBUTTONUP) and not placing_tile:             
                #####Zombie creation list
                    phase+=1
                    globaldelay=0 ###Sets a delay count that staggers the spawn of zombies
                    zombielist=[]
                    a=round(pow(1.67, phase-1))
                    if phase>=0 and phase<3:
                        goldgive=1
                        zc=round(7*(a))
                        zombiecount=zc
                        for i in range(zc):
                            zombielist.append(starterzombie(i))

                    if phase>=3 and phase<5:
                        goldgive=2
                        zc=(a+6)/1.5
                        a1=round(zc*1.7)
                        a2=round(zc*2)
                        a3=round(zc*.6)
                        zombiecount=a1+a2+a3
                        for i in range(a1):
                            zombielist.append(starterzombie(i))
                        for i in range(a2):
                            zombielist.append(zombieimp(i+zc))
                        for i in range(a3):
                            zombielist.append(zombietank(i+2*zc))
                    if (phase>=5 and phase<7) or (phase>=8):
                        goldgive=3
                        zc=a-6
                        a1=round(zc*3)
                        a2=round(zc*2)
                        a3=round(zc*.33)
                        zombiecount=a1+a2+a3
                        for i in range(a1):
                            zombielist.append(betterzombie(i))
                        for i in range(a2):
                            zombielist.append(zombieimprange(i+zc))
                        for i in range(a3):
                            zombielist.append(zombietank(i+2*zc))

                        if phase==7:
                            goldgive=4
                            zombielist.append(zombieboss(i, random.choice(range(-200,1150)), -100, vel, 100))

                    fighting=True
                    print(f"zombiecount:{zombiecount}")

                if ((delete.clickedon(pos) and event.type== pygame.MOUSEBUTTONUP) or (event.type==pygame.KEYDOWN and event.key==pygame.K_BACKSPACE)) and placing_tile and number_of_objects>=2 and tiledown:
                    gold+=thinglist[number_of_objects-1].cost
                    number_of_objects-=1
                    thinglist.pop(number_of_objects)
                    placing_tile= False
                    for i in buttonlist:
                        i.info=False

                if event.type==pygame.MOUSEBUTTONUP and not tiledown and placing_tile and not collision:
                    thinglist[number_of_objects-1].x = (round25(thinglist[number_of_objects-1].x))
                    thinglist[number_of_objects-1].y = (round25(thinglist[number_of_objects-1].y))   
                    tiledown=True  
                    
                for i in range(len(buttonlist)):    
                    if (buttonlist[i].clickedon(pos) and event.type== pygame.MOUSEBUTTONUP) and not placing_tile: ###If button clicked on
                        if buttonlist[i].goldcheck() and phase>=buttonlist[i].round:##Change so button initilializes after first
                            if buttonlist[i]==b1:
                                b1=button1() ### reinitilize button
                                buttonlist[i]=b1 
                            if buttonlist[i]==b2:
                                b2=button2()
                                buttonlist[i]=b2
                            if buttonlist[i]==b3:
                                b3=button3()
                                buttonlist[i]=b3  
                            if buttonlist[i]==b4:
                                b4=button4()
                                buttonlist[i]=b4 
                            if buttonlist[i]==b5:
                                b5=button5()
                                buttonlist[i]=b5 
                            if buttonlist[i]==b6:
                                b6=button6()
                                buttonlist[i]=b6 
                            buttonlist[i].spawnthing()
                            tiledown=False
                            placing_tile=True
                            buttonlist[i].info=True                

                if ((place.clickedon(pos) and event.type== pygame.MOUSEBUTTONUP) or (event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE)) and not collision and placing_tile and tiledown:
                    ###Saves object onto nearest grid location
                    placing_tile=False
                    for i in buttonlist:
                        i.info=False

    if not tiledown and placing_tile and gamestart:
        thinglist[number_of_objects-1].moveobjectmouse()

    if fighting:
        globaldelay+=1
        dead=False
        while fighting:
            dead=False
            for i in range(zombiecount):
                if zombielist[i].hp<=.1:
                    zombiedead(i)
                    dead=True

                    fr=int(clock.get_fps())
                    #print(fr) prints framerate
                    break

            if len(zombielist)==0:
                placing_tile=False
                for i in thinglist:
                    if i.splash==True:
                        i.explosions=[]
                gold+=goldgive
                fighting=False
                
                break
            for i in range(number_of_objects):
                if thinglist[i].hp<=.1:
                    if i==0:
                        running=False
                        ####Add something if the player loses!
                    del thinglist[i] 
                    number_of_objects-=1
                    dead= True 
                    break ###If somebody dies, the loop is run again to check for another death before health changes
            if len(thinglist)==0:
                fighting=False
                break
            if dead==False:
                break

    drawscreen() 


pygame.quit()

