import pygame
import random

pygame.init()
screen= pygame.display.set_mode((1000,1000))

x=475
y=475
vel=.4   
  
screen.fill((130,125,120))

collision= False
xpos=[0]
ypos=[0]
objectwidth=[0]
objectheight=[0]

gridon = False

phase=0 ###phase tells the game what round it's on
fighting=False
placing_tile=False

def round25(x):
    rounded=round(x/25)
    rounded= 25*rounded
    return rounded
 
class object():
    def __init__(self, ID, x, y, vel):
        self.ID=ID
        self.x=x
        self.y=y
        self.vel=vel
        self.img=pygame.transform.scale(self.img, (self.width,self.height))
        self.surf=self.img
        self.hitbox=(self.x, self.y,self.width,self.height)

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


    def changex(self, newx): ##Change the x cord
        self.x=newx
    def changey(self, newy): ##Change the y cord
        self.y=newy

    def draw(self, screen):
        screen.blit(self.surf, (self.x,self.y))
        self.hitbox=(round25(self.x), round25(self.y),self.width,self.height)
        pygame.draw.rect(screen, (255,0,0),self.hitbox, 2)
   

    def collisioncheck(self):
        for a in range(len(xpos)):
            if round25(self.x)-xpos[a]<objectwidth[a] and xpos[a]-round25(self.x)<self.width and round25(self.y)-ypos[a]<objectheight[a] and ypos[a]-round25(self.y)<self.height:
                return True
        

###Change classes!
class castle(object):
    def __init__(self, ID, x, y, vel):
        self.width=150
        self.height=150
        self.img=pygame.image.load(r'C:\Users\tftme\Towerdefense\fortress.png')
        self.range=0
        ###needs range function
        self.hp=20
        super().__init__(ID, x, y, vel)

class spear(object):
    def __init__(self, ID, x, y, vel):
        self.width=50
        self.height=50
        self.img=pygame.image.load(r'C:\Users\tftme\Towerdefense\spear.png')
        self.range=75
        ###needs range function
        self.hp=10
        self.dmg=1
        super().__init__(ID, x, y, vel)



########Thing list, describes the order of the created objects
number_of_objects=0
thinglist=[]
thinglist.append(castle(number_of_objects-1, x, y, vel))
for i in range(8):
    thinglist.append(spear(number_of_objects-1, x, y, vel))
        

def drawscreen():   ##Drawscreen draws the object to the screen
    screen.fill((130,125,120)) ##Screen color

    ###Create grid lines
    if gridon:
        for i in range(0,1000, 25):
            pygame.draw.line(screen, (0,0,0), [i,0], [i,1000], 1)
            pygame.draw.line(screen, (0,0,0), [0,i], [1000,i], 1)


    if number_of_objects>=1:
        if placing_tile:
            thinglist[number_of_objects-1].moveobject() ##This line ensures that only the most recent object is allowed to move
        for i in range(number_of_objects-1):
            thinglist[i].draw(screen) ##Draws all objects that have been created
        thinglist[number_of_objects-1].draw(screen)

    pygame.display.update()


running=True
while running:
    
    if number_of_objects>=2:
        if thinglist[number_of_objects-1].collisioncheck():
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
                if event.key== pygame.K_SPACE:
                    placing_tile=not placing_tile
                    if placing_tile:
                        number_of_objects+=1
                    if not placing_tile and collision== False:

                        ##This if statement ensures that xposition is not recorded upon first space (which summons the tile)
                        ###Saves object onto nearest grid location
                        thinglist[number_of_objects-1].changex(round25(thinglist[number_of_objects-1].x))
                        thinglist[number_of_objects-1].changey(round25(thinglist[number_of_objects-1].y))
                        xpos.append(thinglist[number_of_objects-1].x)
                        ypos.append(thinglist[number_of_objects-1].y)
                        objectwidth.append(thinglist[number_of_objects-1].width)
                        objectheight.append(thinglist[number_of_objects-1].height)
                        
                    
                
        
    
    
    drawscreen() 
    

pygame.quit()