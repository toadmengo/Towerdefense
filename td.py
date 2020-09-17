import pygame
import random
from math import sqrt

pygame.init()
screen= pygame.display.set_mode((1000,1000))

x=475
y=475
vel=.4   
  
screen.fill((130,125,120))
number_of_objects=0

collision= False
xpos=[0]
ypos=[0]
objectwidth=[0]
objectheight=[0]

gridon = False

phase=0 ###phase tells the game what round it's on
fighting=False


placing_tile=False

shotcount=0

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
        self.vel=vel
        self.img=pygame.transform.scale(self.img, (self.width,self.height))
        self.surf=self.img
        self.hitbox=(self.x, self.y,self.width,self.height) ###delete??
        
    def moveobject(self):  

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LSHIFT] or pressed_keys[pygame.K_RSHIFT]: ##Move faster when left shifting!
            if pressed_keys[pygame.K_LEFT] and self.x>self.vel*2.5:
                self.x-=self.vel*2.5
            if pressed_keys[pygame.K_RIGHT] and self.x<1000-self.width-self.vel*2.5:
                self.x+=self.vel*2.5
            if pressed_keys[pygame.K_UP] and self.y>self.vel*2.5:
                self.y-=self.vel*2.5
            if pressed_keys[pygame.K_DOWN] and self.y<1000-self.height-self.vel*2.5:
                self.y+=self.vel*2.5

        else:
            if pressed_keys[pygame.K_LEFT] and self.x>self.vel:
                self.x-=self.vel
            if pressed_keys[pygame.K_RIGHT] and self.x<1000-self.width-self.vel:
                self.x+=self.vel
            if pressed_keys[pygame.K_UP] and self.y>self.vel:
                self.y-=self.vel
            if pressed_keys[pygame.K_DOWN] and self.y<1000-self.height-self.vel:
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
        hpoutline= (self.center[0]-20, self.y-15, 40, 15)
        hpbox= (self.center[0]-20, self.y-15, 40*self.hp/self.maxhp, 15)
        pygame.draw.rect(screen, (255,0,0), hpoutline , 4)
        pygame.draw.rect(screen, (60,80,240), hpbox , 0)
    def drawhitbox(self, screen):
        self.hitbox=(round25(self.x), round25(self.y),self.width,self.height)
        pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
    def drawrange(self, screen):
        pygame.draw.circle(screen, (255,0,0), self.center, self.range, 2)

    def collisioncheck(self):
        for a in range(len(xpos)):
            if round25(self.x)-xpos[a]<objectwidth[a] and xpos[a]-round25(self.x)<self.width and round25(self.y)-ypos[a]<objectheight[a] and ypos[a]-round25(self.y)<self.height:
                return True
        
    def zombiehealthupdate(self): ### some redundancy here
        distlist=[]
        for i in range(zombiecount):
            a= (self.center[0]-zombielist[i].center[0])**2 + (self.center[1]-zombielist[i].center[1])**2
            centerdistance=sqrt(a)
            distlist.append(centerdistance)
        centerdistance=min(distlist)
        i=[]
        i.append(distlist.index(centerdistance))
        i=i[0]
        xdif=self.center[0]-zombielist[i].center[0]
        self.right=True
        self.up=False
        self.down=False
        if centerdistance<=self.range:
            zombielist[i].shot=True
            if zombielist[i].hp>0:
                zombielist[i].hp-=self.dmg/1000
            if fighting:
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
        self.hp=40
        self.maxhp=self.hp
        super().__init__(ID, x, y, vel)
        self.right=True
        self.up=False
        self.down=False


class soldier(object):
    def __init__(self, ID, x, y, vel):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/soldierR.png')
        self.range=150
        ###needs range function
        self.hp=25
        self.maxhp=self.hp
        self.dmg=3
        super().__init__(ID, x, y, vel)
        self.imglist=[pygame.image.load(r'image/soldierR.png'), pygame.image.load(r'image/soldierTR.png'),pygame.image.load(r'image/soldierTL.png'), pygame.image.load(r'image/soldierL.png'), pygame.image.load(r'image/soldierBL.png'), pygame.image.load(r'image/soldierBR.png')]
        self.right=True
        self.up=False
        self.down=False


class zombie(object):
    def __init__(self, ID, x, y, vel, delay):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'image/zombie.png')
        self.imglist=[pygame.transform.scale(pygame.image.load(r'image/zombie.png'), (self.width,self.height)),pygame.transform.scale(pygame.image.load(r'image/zombie.png'), (self.width,self.height)),pygame.transform.scale(pygame.image.load(r'image/zombie.png'), (self.width,self.height)),pygame.transform.scale(pygame.image.load(r'image/zombieshot.png'), (self.width,self.height)),pygame.transform.scale(pygame.image.load(r'image/zombieshot.png'), (self.width,self.height)),pygame.transform.scale(pygame.image.load(r'image/zombieshot.png'), (self.width,self.height))]
        self.range=75
        ###needs range function
        self.hp=10
        self.maxhp=self.hp
        self.dmg=2
        self.spawnlocatedistance=475-x
        self.delay=delay
        super().__init__(ID, x, y, vel)
        self.shot=False
        self.shotcount=random.choice(range(0,99))
            
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
                xvec=self.spawnlocatedistance/sqrt((self.spawnlocatedistance**2)+(475**2))
                yvec= 475/sqrt((self.spawnlocatedistance**2)+(475**2))
                self.x+=.12*xvec
                self.y+=.12*yvec
    
    def zombieanimate(self):
        self.shotcount+=1
        if self.shotcount+1>=100:
            self.shotcount=0
        if self.shot:
            self.img= self.imglist[self.shotcount//20]
        else: 
            self.img=self.imglist[0]



###Prepared objects#####
########Thing list, describes the order of the created objects

thinglist=[]
thinglist.append(castle(-1, x, y, vel))
for i in range(8):
    thinglist.append(soldier(-1, x, y, vel))



def drawscreen():   ##Drawscreen draws the object to the screen
    screen.fill((130,125,120)) ##Screen color

    ###Create grid lines
    if gridon and not fighting:
        for i in range(0,1000, 25):
            pygame.draw.line(screen, (0,0,0), [i,0], [i,1000], 1)
            pygame.draw.line(screen, (0,0,0), [0,i], [1000,i], 1)

    if number_of_objects>=1:
        if placing_tile and not fighting:
            thinglist[number_of_objects-1].moveobject() ##This line ensures that only the most recent object is allowed to move
            if number_of_objects>=2:
                thinglist[number_of_objects-1].drawrange(screen) 
        for i in range(number_of_objects):
            if i!=0:
                if fighting:
                    thinglist[i].zombiehealthupdate()
                thinglist[i].drawsoldier() ##Draws all objects that have been created
            if not fighting:
                thinglist[i].drawhitbox(screen) 
            else:
                thinglist[i].drawhpbox()
        thinglist[0].draw()
        
        if fighting:
            for i in range(zombiecount):
                zombielist[i].zombiemove()
                zombielist[i].draw()
                zombielist[i].zombieanimate()
                zombielist[i].drawhpbox()
                zombielist[i].shot=False

                

                
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

            if event.key==pygame.K_g: ###press g to turn on grid overlay
                gridon = not gridon
            
            if not fighting:
                if event.key== pygame.K_SPACE and collision == False:
                    if not placing_tile:
                        if not fighting:
                            ###spawn zombie mechanism
                            if number_of_objects==5 and phase==0:
                                
                                #####Zombie creation list
                                zombielist=[]
                                zombiecount=15
                                globaldelay=0 ###Sets a delay count that staggers the spawn of zombies
                                for i in range(zombiecount):
                                    z= random.choice(range(0,950))
                                    delay= random.choice(range(1,4000))
                                    zombielist.append(zombie(i, z, 0, vel, delay))
                                fighting=True
                                
                            else:    
                                number_of_objects+=1
                                placing_tile=not placing_tile
              
                    else:
                        ###Saves object onto nearest grid location
                        thinglist[number_of_objects-1].changex(round25(thinglist[number_of_objects-1].x))
                        thinglist[number_of_objects-1].changey(round25(thinglist[number_of_objects-1].y))
                        xpos.append(thinglist[number_of_objects-1].x)
                        ypos.append(thinglist[number_of_objects-1].y)
                        objectwidth.append(thinglist[number_of_objects-1].width)
                        objectheight.append(thinglist[number_of_objects-1].height)
                        placing_tile=not placing_tile  

    if fighting:

        globaldelay+=1 ###Staggers entrance of zombies
        dead=False
        while fighting:
            if len(zombielist)==0 or len(thinglist)==0:
                fighting=False
            dead=False
            for i in range(zombiecount):
                if zombielist[i].hp<=.1:
                    del zombielist[i]
                    zombiecount-=1
                    dead=True
                    break
            for i in range(number_of_objects):
                thinglist[i].zombiehealthupdate()
                if thinglist[i].hp<=.1:
                    del thinglist[i]  
                    number_of_objects-=1
                    dead= True 
                    break ###If somebody dies, the loop is run again to check for another death before health changes
            if dead==False:
                break


    drawscreen() 



pygame.quit()

