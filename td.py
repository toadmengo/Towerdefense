import pygame
import random
from math import sqrt

pygame.init()
screen= pygame.display.set_mode((1000,1000))

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
myfont2= pygame.font.SysFont('Comic Sans MS', 16)

x=475
y=475
  
screenwidth=1000
screenheight=800
screen.fill((130,125,120))
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

gold=3

shottimerrange=200

placing_tile=False

shotcount=0

gamestart=False

clock=pygame.time.Clock() ###Measure framerate
fastspeed=10
normalspeed=6
globalspeed= normalspeed ###(adjusts for speed, does not currently function because only affects initialization)
vel=.5*globalspeed

def round25(x):
    rounded=round(x/25)
    rounded= 25*rounded
    return rounded
 
class object():
    def __init__(self, ID, x, y, vel):
        self.ID=ID
        self.x=x
        self.y=y
        self.center= [round(self.x+self.width/2), round(self.y+self.height/2)]
        self.img=pygame.transform.scale(self.img, (self.width,self.height))
        self.surf=self.img
        self.hitbox=(self.x, self.y,self.width,self.height) ###delete??

        ###Shooting calculations
        self.shooting=False
        self.shottimer=random.choice(range(1, shottimerrange))
        self.shootingat=-1

        self.right=True
        self.up=False
        self.down=False
        
        
        
    def moveobject(self):  

        pressed_keys = pygame.key.get_pressed()
        screenlowerbound=300

        if pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT]: ##Move faster when left shifting!
            if (pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]) and self.x>self.vel*2.5:
                self.x-=self.vel*2.5
            if (pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d])and self.x<screenwidth-self.vel*2.5:
                self.x+=self.vel*2.5
            if (pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w])and self.y-self.vel*2.5>screenlowerbound:
                self.y-=self.vel*2.5
            if (pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s])and self.y<screenheight-self.height-self.vel*2.5:
                self.y+=self.vel*2.5

        else:
            if (pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]) and self.x>self.vel:
                self.x-=self.vel
            if (pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]) and self.x<screenwidth-self.width-self.vel:
                self.x+=self.vel
            if (pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]) and self.y-self.vel*2.5>screenlowerbound:
                self.y-=self.vel
            if (pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]) and self.y<screenheight-self.height-self.vel:
                self.y+=self.vel
        self.center= [round(self.x+self.width/2), round(self.y+self.height/2)]



    def changex(self, newx): ##Change the x cord
        self.x=newx
    def changey(self, newy): ##Change the y cord
        self.y=newy

    def draw(self):
        self.surf=self.img
        screen.blit(self.surf, (self.x,self.y))

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

    def drawhitbox(self, screen):
        self.hitbox=(round25(self.x), round25(self.y),self.width,self.height)
        pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
    def drawrange(self, screen):
        if self.range>0:
            pygame.draw.circle(screen, (255,0,0), self.center, self.range, 2)

    def collisioncheck(self):
        colliding=False
        for i in range(len(thinglist)-1):
            if round25(self.x)-thinglist[i].x<thinglist[i].width and thinglist[i].x-round25(self.x)<self.width and round25(self.y)-thinglist[i].y<thinglist[i] .height and thinglist[i].y-round25(self.y)<self.height:
                colliding=True
        return colliding
        
    def zombieshottrack(self): ### some redundancy here
        distlist=[]
        indexlist=[] ###Could use dictionary
        self.shooting=False
        self.right=True
        self.up=False
        self.down=False
        for i in range(zombiecount):
            a= (self.center[0]-zombielist[i].center[0])**2 + (self.center[1]-zombielist[i].center[1])**2
            centerdistance=sqrt(a)
            if centerdistance<=self.range:
                distlist.append(centerdistance)
                indexlist.append(i)
        if len(distlist)>0:
            if self.shortrange:
                centerdistance=min(distlist)
            elif not self.shortrange:
                centerdistance=max(distlist)
            closest=[]
            closest.append(distlist.index(centerdistance))
            i=indexlist[closest[0]]
            xdif=self.center[0]-zombielist[i].center[0]
            if centerdistance<=self.range and fighting: 
                ###Shooting calculations
                self.shottimer+=self.firerate
                if self.shottimer>=shottimerrange: ##Rate of zombie getting hit
                    self.shooting=True
                    self.shootingat=zombielist[i].ID
                    self.shottimer=0
                ###Positions for soldiers
                if xdif>=0:
                    self.right=False
                if zombielist[i].y<self.y-zombielist[i].range*.5:
                    self.up=True
                if zombielist[i].y>self.y+self.range*.5:
                    self.down=True

###Classes
class castle(object):
    def __init__(self, ID, x, y, vel):
        self.width=150
        self.height=150
        self.img=pygame.image.load(r'image/fortress.png')
        self.range=0
        ###needs range function
        self.maxhp=40
        self.hp=self.maxhp
        self.vel=vel
        super().__init__(ID, x, y, vel)
        self.right=True
        self.up=False
        self.down=False
        self.good=True


class soldier(object):
    def __init__(self, ID, x, y, vel):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/soldierR.png')
        self.range=180
        self.maxhp=20
        self.hp=self.maxhp
        self.dmg=2
        self.firerate=5
        self.vel=vel
        super().__init__(ID, x, y, vel)
        self.imglist=[pygame.image.load(r'image/soldierR.png'), pygame.image.load(r'image/soldierTR.png'),pygame.image.load(r'image/soldierTL.png'), pygame.image.load(r'image/soldierL.png'), pygame.image.load(r'image/soldierBL.png'), pygame.image.load(r'image/soldierBR.png')]
        self.cost=1
        self.good=True
        self.shortrange=True
        self.description=''

class wall(object):
    def __init__(self, ID, x, y, vel):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/barbed-wire.png')
        self.imglist=[]
        for i in range(6):
            self.imglist.append(pygame.image.load(r'image/barbed-wire.png'))
        self.range=0
        self.maxhp=90
        self.hp=self.maxhp
        self.dmg=0
        self.firerate=0
        self.vel=vel
        super().__init__(ID, x, y, vel)
        self.cost=2
        self.good=True
        self.shortrange=True
        self.description='Great for tanking zombies'

class machinegun(object):
    def __init__(self, ID, x, y, vel):
        self.width=75
        self.height=75
        self.img=pygame.image.load(r'image/MGR.png')
        self.imglist=[pygame.image.load(r'image/MGR.png'),pygame.image.load(r'image/MGTR.png'),pygame.image.load(r'image/MGTL.png'),pygame.image.load(r'image/MGL.png'),pygame.image.load(r'image/MGBL.png'),pygame.image.load(r'image/MGBR.png')]
        self.range=175
        self.maxhp=5
        self.hp=self.maxhp
        self.dmg=1
        self.firerate=30
        self.vel=vel
        super().__init__(ID, x, y, vel)
        self.cost=3
        self.good=True
        self.shortrange=True
        self.description='High Firerate, quite vulnerable'

class sniper(object):
    def __init__(self, ID, x, y, vel):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/sniperR.png')
        self.imglist=[pygame.image.load(r'image/sniperR.png'),pygame.image.load(r'image/sniperTR.png'),pygame.image.load(r'image/sniperTL.png'),pygame.image.load(r'image/sniperL.png'),pygame.image.load(r'image/sniperBL.png'),pygame.image.load(r'image/sniperBR.png')]
        self.range=320
        self.maxhp=5
        self.hp=self.maxhp
        self.dmg=50
        self.firerate=1
        self.vel=vel
        super().__init__(ID, x, y, vel)
        self.cost=2
        self.good=True
        self.shortrange=False
        self.description='Long range damage, quite vulnerable'


###ZOMBIES

class zombie(object):
    def __init__(self, ID, x, y, vel):
        super().__init__(ID, x, y, vel)
        self.spawnlocatedistancex=(thinglist[0].center[0]-(self.width/2))-self.x
        self.spawnlocatedistancey=(thinglist[0].center[1]-(self.height/2))-self.y
        self.shot=0
        self.good=False
        self.xvec=self.spawnlocatedistancex/sqrt((self.spawnlocatedistancex**2)+(self.spawnlocatedistancey**2))
        self.yvec= self.spawnlocatedistancey/sqrt((self.spawnlocatedistancex**2)+(self.spawnlocatedistancey**2))

            
    def zombiemove(self):
        self.center= [round(self.x+self.width/2), round(self.y+self.height/2)]
        movement= True
        distlist=[]
        if globaldelay>=self.delay:
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
        for j in thinglist:
            if j.shooting and j.shootingat==self.ID:
                self.gotshot=True
                self.img= self.imglist[1]
                self.hp-=j.dmg
                print(f"hp:{self.ID}={self.hp}")
        if not self.gotshot:
            self.img= self.imglist[0]

class starterzombie(zombie):
    def __init__(self, ID, x, y, vel, delay):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/zombie.png')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/zombie.png'), (self.width,self.height)), pygame.transform.scale(pygame.image.load(r'image/zombieshot.png'), (self.width,self.height))]
        self.range=75
        self.maxhp=12
        self.hp=self.maxhp
        self.dmg=4.5*globalspeed
        self.delay=delay
        self.gold=1
        self.vel=vel
        super().__init__(ID, x, y, vel)

        #self.round?

class zombieimp(zombie):
    def __init__(self, ID, x, y, vel, delay):
        self.width=25
        self.height=25
        self.img=pygame.image.load(r'image/babyzombie.png')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/babyzombie.png'), (self.width,self.height)), pygame.transform.scale(pygame.image.load(r'image/babyzombieshot.png'), (self.width,self.height))]
        self.range=40
        self.maxhp=5
        self.hp=self.maxhp
        self.dmg=10*globalspeed
        self.delay=delay+400
        self.gold=0
        self.vel=vel*2.5 ###Maybe do when initiating?
        super().__init__(ID, x, y, vel)
        
class zombietank(zombie):
    def __init__(self, ID, x, y, vel, delay):
        self.width=75
        self.height=75
        self.img=pygame.image.load(r'image/zombietank.png')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/zombietank.png'), (self.width,self.height)), pygame.transform.scale(pygame.image.load(r'image/zombietankshot.png'), (self.width,self.height))]
        self.range=100
        self.maxhp=100
        self.hp=self.maxhp
        self.dmg=10*globalspeed
        self.delay=delay
        self.gold=2
        self.vel=vel*.6 ###Maybe do when initiating?
        super().__init__(ID, x, y, vel)
        

def zombiedead(i):
    global gold
    goldchance= random.choice(range(100))
    if goldchance>40: ###Goldchance
        gold+=zombielist[i].gold
    del zombielist[i]
    global zombiecount
    zombiecount-=1

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
        text4=myfont.render(f'{self.soldier.description}', False, (0, 0, 0))
        screen.blit(text1, (20,self.y-250))
        screen.blit(text2, (20,self.y-200))
        screen.blit(text3, (20,self.y-150))
        screen.blit(text4, (20,self.y-80))

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
        self.soldier=soldier(number_of_objects, thinglist[0].x, thinglist[0].y, vel)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 0


class button2(button):
    def __init__(self):
        button.__init__(self)
        self.x=80
        self.y=820
        self.soldier=wall(number_of_objects, thinglist[0].x, thinglist[0].y, vel)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 1

class button3(button):
    def __init__(self):
        button.__init__(self)
        self.x=140
        self.y=820
        self.soldier=machinegun(number_of_objects, thinglist[0].x, thinglist[0].y, vel)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 2

class button4(button):
    def __init__(self):
        button.__init__(self)
        self.x=200
        self.y=820
        self.soldier=sniper(number_of_objects, thinglist[0].x, thinglist[0].y, vel)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.round= 2


thinglist=[]
thinglist.append(castle(-1, x, y, vel))

def drawscreen():   ##Drawscreen draws the object to the screen
    screen.fill((130,125,120)) ##Screen color
    if number_of_objects>=1:
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
            thinglist[number_of_objects-1].moveobject() ##This line ensures that only the most recent object is allowed to move
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
                if event.key==pygame.K_SPACE:
                    if number_of_objects==0 and phase==0 and gamestart==False:
                        gamestart=True
                        number_of_objects+=1
                        placing_tile=True
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
                        number_of_buttons= len(buttonlist)
                        
                 
            if event.type== pygame.MOUSEBUTTONUP and gamestart==True:   
                pos=pygame.mouse.get_pos()

                if start.clickedon(pos) and not placing_tile:             
                #####Zombie creation list
                    phase+=1
                    globaldelay=0 ###Sets a delay count that staggers the spawn of zombies
                    zombielist=[]
                    a=pow(2, phase-1)
                    if phase>=0 and phase<3:
                        zc=3 + (5*(a))
                        zombiecount=zc
                        for i in range(zc):
                            zombielist.append(starterzombie(i, random.choice(range(0,950)), 0, vel, random.choice(range(1,400+20*zc))))
                    if phase>=3:
                        zc=a
                        zombiecount=zc*6
                        for i in range(zc*2):
                            zombielist.append(starterzombie(i, random.choice(range(0,950)), 0, vel, random.choice(range(1,400+20*zc))))
                        for i in range(zc*3):
                            zombielist.append(zombieimp(i+zc, random.choice(range(0,950)), 0, vel, random.choice(range(1,400+20*zc)))) 
                        for i in range(zc):
                            zombielist.append(zombietank(i+2*zc, random.choice(range(0,950)), 0, vel, random.choice(range(1,400+20*zc)))) 

                    fighting=True
                    print(f"zombiecount:{zombiecount}")

                if delete.clickedon(pos) and placing_tile and number_of_objects>=2:
                    gold+=thinglist[number_of_objects-1].cost
                    number_of_objects-=1
                    thinglist.pop(number_of_objects)
                    placing_tile= False
                    for i in buttonlist:
                        i.info=False
                    
                for i in range(len(buttonlist)):    
                    if buttonlist[i].clickedon(pos) and not placing_tile: ###If button clicked on
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
                            
                            buttonlist[i].spawnthing()
                               
                            placing_tile=True
                            buttonlist[i].info=True   

                if place.clickedon(pos) and not collision and placing_tile:
                    ###Saves object onto nearest grid location
                    thinglist[number_of_objects-1].changex(round25(thinglist[number_of_objects-1].x))
                    thinglist[number_of_objects-1].changey(round25(thinglist[number_of_objects-1].y))
                    placing_tile=False
                    for i in buttonlist:
                        i.info=False
                    
                    

    if fighting:
    
        globaldelay+=1 ###Staggers entrance of zombies
        dead=False
        while fighting:
            dead=False
            for i in range(zombiecount):
                if zombielist[i].hp<=.1:
                    zombiedead(i)
                    dead=True

                    fr=int(clock.get_fps())
                    #print(fr) ##DELETETHIS
                    break

            if len(zombielist)==0:
                fighting=False
                placing_tile=False

                ###initialize new buttons here
                #if phase ==1:
                    #b2=button2()
                    #number_of_buttons+=1
                    #buttonlist.append(b2)

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

