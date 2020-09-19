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
vel=.5  
  
screenwidth=1000
screenheight=800
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

gold=4


placing_tile=False

shotcount=0

gamestart=False

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
            if (pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]) and self.x>self.vel*2.5:
                self.x-=self.vel*2.5
            if (pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d])and self.x<1000-screenwidth-self.vel*2.5:
                self.x+=self.vel*2.5
            if (pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w])and self.y>self.vel*2.5:
                self.y-=self.vel*2.5
            if (pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s])and self.y<screenheight-self.height-self.vel*2.5:
                self.y+=self.vel*2.5

        else:
            if (pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]) and self.x>self.vel:
                self.x-=self.vel
            if (pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]) and self.x<screenwidth-self.width-self.vel:
                self.x+=self.vel
            if (pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]) and self.y>self.vel:
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
        hpoutline= (self.center[0]-self.hp, self.y-15, maxhp*2, round(maxhp/3)+5)
        hpbox= (self.center[0]-self.hp, self.y-15, maxhp*2*self.hp/self.maxhp, round(maxhp/3)+5)
        if self.good:
            pygame.draw.rect(screen, (0,150,0), hpbox , 0)
        else:
            pygame.draw.rect(screen, (150,0,50), hpbox , 0)
        pygame.draw.rect(screen, (255,255,255), hpoutline , 3)

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
            zombielist[i].shot+=1
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
        self.good=True


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
        self.cost=1
        self.good=True
        self.description=''


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
        super().__init__(ID, x, y, vel)
        self.spawnlocatedistance=(thinglist[0].center[0]-(self.width/2))-self.x
        self.delay=delay
        self.shot=0
        self.shotcount=random.choice(range(0,99))
        self.good=False
            
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
                xvec=self.spawnlocatedistance/sqrt((self.spawnlocatedistance**2)+((thinglist[0].center[1]-(self.height/2))**2))
                yvec= 475/sqrt((self.spawnlocatedistance**2)+(475**2))
                self.x+=.2*xvec* self.vel
                self.y+=.2*yvec* self.vel
    
    def zombieanimate(self):
        self.shotcount+=self.shot
        if self.shotcount+1>=100:
            self.shotcount=0
        if self.shot>0:
            self.img= self.imglist[self.shotcount//20]
        else: 
            self.img=self.imglist[0]

def zombiedead(i):
    del zombielist[i]
    global zombiecount
    zombiecount-=1
    global gold
    goldchance= random.choice(range(100))
    if goldchance>60:
        gold+=1

class button():
    def __init__(self):
        self.width=40
        self.height=40
    
    def draw(self):
        self.img=pygame.transform.scale(self.img, (self.width,self.height))
        pygame.draw.rect(screen, (0,0,0),self.rect, 2)
        screen.blit(self.img, (self.x,self.y))
        self.textsurface= myfont2.render(f'Cost: {self.cost}', False, (0, 0, 0))
        screen.blit(self.textsurface, (self.x,self.y+self.height+10))
          
    def clickedon(self, pos):
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

    def spawnthing(self):
        global gold
        global number_of_objects
        if gold-self.soldier.cost<0:
            ####Display text: Can't buy
            return False
        else:
            thinglist.append(self.soldier)
            gold-=self.soldier.cost
            number_of_objects+=1
            return True
    
    def showinfo(self):
        text1=myfont.render(f'DMG: {self.dmg}', False, (0, 0, 0))
        text2=myfont.render(f'HP: {self.hp}', False, (0, 0, 0))
        text3=myfont.render(f'{self.description}', False, (0, 0, 0))
        screen.blit(text1, (self.x,self.y-150))
        screen.blit(text2, (self.x,self.y-100))
        screen.blit(text3, (self.x,self.y-50))

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

class button1(button, soldier):
    def __init__(self):
        button.__init__(self)
        self.x=20
        self.y=820
        self.soldier=soldier(number_of_objects, x, y, vel)
        self.img=self.soldier.img
        self.info=False
        self.rect=pygame.Rect(self.x,self.y,self.width, self.height)
        self.cost=self.soldier.cost
        self.hp=self.soldier.hp
        self.dmg=self.soldier.dmg
        self.description=self.soldier.description

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
        b1.draw() #Button
        if b1.info==True:
            b1.showinfo()
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
                zombielist[i].zombieanimate()
                zombielist[i].drawhpbox()
                zombielist[i].shot=0
        
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

        if event.type == pygame.KEYDOWN and event.key==pygame.K_g: ###press g to turn on grid overlay
            gridon = not gridon
        
        if not fighting:
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if number_of_objects==0:
                        gamestart=True
                        number_of_objects+=1
                        placing_tile=True
                        ###Initialize buttons here!
                        start=startbutton()
                        place=placebutton()
                        delete=deletebutton()
                        b1=button1()
                        
            if event.type== pygame.MOUSEBUTTONUP and gamestart==True:   
                pos=pygame.mouse.get_pos()
                b1.info=False

                if start.clickedon(pos) and not placing_tile:             
                #####Zombie creation listW
                    phase+=1
                    zombielist=[]
                    print((5*pow(2, phase-1)))
                    zombiecount=10 + (5*pow(2, phase-1))
                    print(zombiecount)
                    
                    globaldelay=0 ###Sets a delay count that staggers the spawn of zombies
                    for i in range(zombiecount):
                        z= random.choice(range(0,950))
                        delay= random.choice(range(1,4000))
                        zombielist.append(zombie(i, z, 0, vel, delay))
                    fighting=True


                if delete.clickedon(pos) and placing_tile and number_of_objects>=2:
                    number_of_objects-=1
                    thinglist.pop(number_of_objects)
                    placing_tile= False


                if b1.clickedon(pos) and not placing_tile: ###If button clicked on
                    if event.button == 1: ###Consider creating a list of buttons to simplify this
                        if b1.spawnthing():
                            b1=button1() ### reinitilize button
                            placing_tile=True
            
                    if event.button == 2 or event.button==3: ###Needs fixing
                        b1=button1()
                        b1.info==True
                

                if place.clickedon(pos) and not collision and placing_tile:
                    ###Saves object onto nearest grid location
                    thinglist[number_of_objects-1].changex(round25(thinglist[number_of_objects-1].x))
                    thinglist[number_of_objects-1].changey(round25(thinglist[number_of_objects-1].y))
                    xpos.append(thinglist[number_of_objects-1].x)
                    ypos.append(thinglist[number_of_objects-1].y)
                    objectwidth.append(thinglist[number_of_objects-1].width)
                    objectheight.append(thinglist[number_of_objects-1].height)
                    placing_tile=False
                    print('clicked place')

    if fighting:
    
        globaldelay+=1 ###Staggers entrance of zombies
        dead=False
        while fighting:
            dead=False
            for i in range(zombiecount):
                if zombielist[i].hp<=.1:
                    zombiedead(i)
                    dead=True
                    break
            if len(zombielist)==0:
                fighting=False
                phase+=1
                placing_tile=False
                break
            for i in range(number_of_objects):
                thinglist[i].zombiehealthupdate()
                if thinglist[i].hp<=.1:
                    del thinglist[i]
                    del xpos[i]
                    del ypos[i]
                    del objectheight[i]
                    del objectwidth[i]  
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

