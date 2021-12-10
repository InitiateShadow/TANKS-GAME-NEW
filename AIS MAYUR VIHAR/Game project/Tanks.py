import pygame
import math as m
import time
import random
import sqlite3 as sq
import copy
pygame.init()

##############################################################################################################################################################################################
#building display
d_width=800
d_height=600
bg=pygame.transform.scale(pygame.image.load('bg1.png'),(d_width,d_height))
dg=pygame.transform.scale(pygame.image.load('bg2.png'),(d_width,d_height*7//60))
fps=30
# =============================================================================
# gunshot=pygame.mixer.Sound('gunshot.wav')
# explosion=pygame.mixer.Sound('explosion.wav')
# tankmove=pygame.mixer.Sound('tankmove.wav')
# =============================================================================
clock=pygame.time.Clock()
win=pygame.display.set_mode((d_width,d_height))
pygame.display.set_caption("Tanks")
game_icon=pygame.image.load('tankicon.png')
pygame.display.set_icon(pygame.transform.scale(game_icon,(32,32)))
exp=[]
door=pygame.transform.scale(pygame.image.load('door.jpg'),(d_width,d_height))
for i in range(1,16):
    exp.append(pygame.image.load('exp%d.png'%i))
tank_body=[pygame.image.load('t_body1.png'),pygame.image.load('t_body2.png'),pygame.image.load('t_body3.png'),pygame.image.load('t_body4.png'),pygame.image.load('t_body5.png')]
tank_turret=[pygame.image.load('t_turret1.png'),pygame.image.load('t_turret2.png'),pygame.image.load('t_turret3.png'),pygame.image.load('t_turret4.png'),pygame.image.load('t_turret5.png')]
##############################################################################################################################################################################################
#ALL CLASSES
class display(object):
    def msg_2_screen(msg,f_name,f_color,x_displace=0,y_displace=0,size=25,b=0,i=0,f_lcn=""):
        fonte=fontor(f_name,size,b,i,f_lcn)
        screen_text=fonte.render(msg,True,colour(f_color))
        win.blit(screen_text,
                 [(d_width/2)-screen_text.get_rect().width/2+x_displace,d_height/2+y_displace-screen_text.get_rect().height/2])
            
    def text_2_button(x,y,text,f_name,f_color,size=25,b=0,i=0,f_lcn=""):
        fonte=fontor(f_name,size,b,i,f_lcn)
        screen_text=fonte.render(text,True,colour(f_color))
        win.blit(screen_text,[x-screen_text.get_rect().width/2,y-screen_text.get_rect().height/2])
        
    def button(x,y,width,height,inactive,active,action=None,parameter=None):
        x=x-width/2
        y=y-height/2
        cur=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        if x<cur[0]<x+width and y<cur[1]<y+height:
            if parameter==None:
                pygame.draw.rect(win,colour(inactive),(x+3,y+3,width,height))
                pygame.draw.rect(win,colour(active),(x-3,y-3,width,height))
                if click[0]==1:
                    if click[0]==1 and action!=None:
                        if action=="quit":
                            1/0
                        elif action=="controls":
                            return "controls"
                        elif action=="play":
                            return "play"
                        elif action=="home":
                            return "home"
                        elif action=="scores":
                            return 'scores'
                        elif action=='next' or 'back':
                            return True
                        else:
                            pass      
        else:
            pygame.draw.rect(win,colour(active),(x,y,width,height))
        return None
    def button1(i,x,y,parameter=None,t=0):
         l_tank=['Prime','Demon','Dragon','Typhoon','Colossus']
         l_turret=['RZ156','VC918','CQ798','WB112','TZ553']
         cur=pygame.mouse.get_pos()
         click=pygame.mouse.get_pressed()
         if t==0:
             rect=tank_turret[i].get_rect()
             x=x-rect.width/2
             y=y-rect.height/2
             win.blit(tank_turret[i],(x,y))
             display.msg_2_screen(l_turret[i],'agencyfb',colour('black'),x-d_width//2+tank_turret[i].get_rect().width*70//200,y-d_height//2+tank_turret[i].get_rect().height*50//30,tank_turret[i].get_rect().height)
             if x<cur[0]<x+rect.width and y<cur[1]<y+rect.height:
                 pygame.draw.rect(win,colour('grey'),(x-5,y-5,rect.width+10,rect.height+10),2)
                 if click[0]:
                     return parameter
         elif t==1:
             rect=tank_body[i].get_rect()
             x=x-rect.width/2
             y=y-rect.height/2
             win.blit(tank_body[i],(x,y))
             display.msg_2_screen(l_tank[i],'agencyfb',colour('black'),x-d_width//2+tank_body[i].get_rect().width*80//140,y-d_height//2+tank_body[i].get_rect().height*3//2,tank_body[i].get_rect().height*3//4)
             if x<cur[0]<x+rect.width and y<cur[1]<y+rect.height:
                 pygame.draw.rect(win,colour('grey'),(x-5,y-5,rect.width+10,rect.height+10),2)
                 if click[0]:
                     return parameter

class player(object):
    def __init__(self,x,y,angle):
        self.x = x
        self.y = y
        self.angle=angle
        self.power=100
        self.health=100
    def draw(self,win,itur,ibod,x_barrier):
        self.hitbox=(self.x-2,self.y-20,4+tank_body[4].get_rect().width*9//14,tank_body[4].get_rect().height*3//2)
        Im=pygame.transform.scale(tank_turret[itur],(tank_turret[itur].get_rect().width//2,tank_turret[itur].get_rect().height*4//5))
        rot_tank_turret=pygame.transform.rotate(Im,self.angle)
        turret_rect_center=rot_tank_turret.get_rect().center
        pygame.draw.circle(win,(80,80,14),(int(self.x+Im.get_rect().center[0]),int(self.y)),Im.get_rect().width*18//100)
        display.msg_2_screen("POWER:"+str(self.power)+"%",'AgencyFB',colour('black'),0,-d_height//3,40)
        display.msg_2_screen("ANGLE:"+str(-self.angle),'AgencyFB',colour('black'),0,-d_height*4//15,40)
        win.blit(rot_tank_turret,(self.x+Im.get_rect().center[0]-turret_rect_center[0],self.y-5-turret_rect_center[1]))
        win.blit(pygame.transform.scale(tank_body[ibod],(int(tank_body[4].get_rect().width*9/14),int(tank_body[4].get_rect().height*0.8))),(self.x,self.y))
        pygame.draw.rect(win,colour('d_red'),(d_width*5//8,d_height//6,d_width//4,d_height//20))
        pygame.draw.rect(win,colour('green'),(d_width*5//8,d_height//6,self.health*2*d_width//800,d_height//20))
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT]==1:
            self.x-=3
        elif key[pygame.K_RIGHT]==1:
            self.x+=3
        elif key[pygame.K_UP]==1:
            self.angle-=1
        elif key[pygame.K_DOWN]==1:
            self.angle+=1
        elif key[pygame.K_a]==1:
            self.power-=1
        elif key[pygame.K_d]==1:
            self.power+=1
        if self.x<=x_barrier+20:
            self.x+=3
        elif self.x+90>d_width:
            self.x-=3
        if self.angle>5:
            self.angle-=1
        elif self.angle<-90:
            self.angle+=1
        if self.power==0:
            self.power+=1
        if self.power==101:
            self.power-=1
    def fire(self,x_barrier,y_barrier,itur,ibod):
        Im=pygame.transform.flip(pygame.transform.scale(tank_turret[itur],(100,24)),1,0)
        fire1=pygame.image.load('firecircle1.png')
        g=10
        v=m.sqrt(10*d_width)*self.power/100
        v_x=v*m.cos(-self.angle*m.pi/180)
        v_y=v*m.sin(-self.angle*m.pi/180)
        x=self.x+Im.get_rect().center[0]-Im.get_rect().center[0]*m.cos(self.angle*m.pi/180)
        y=self.y+Im.get_rect().center[0]*m.sin(self.angle*m.pi/180)-2
        fire=True
        display.msg_2_screen("POWER:"+str(self.power)+"%",'AgencyFB',colour('black'),0,-d_height//3,40)
        display.msg_2_screen("ANGLE:"+str(-self.angle),'AgencyFB',colour('black'),0,-d_height*4//15,40)
        self.draw(win,itur,ibod,x_barrier)
        enemy_tank.draw(win,x_barrier)
        c=0
        while fire:
                x=x-v_x/10
                v_y=v_y-g/10
                y=y-v_y/10
                win.blit(pygame.transform.scale(fire1,(6,6)),(int(x)-3,int(y)-3))
                clock.tick(fps*10)
                pygame.display.update()
                l=enemy_tank.hitbox
                if l[0]+l[2]>x>l[0] and l[1]+l[3]>y>l[1]:
                    c+=1
                if c==2:
                    win.blit(pygame.transform.scale(fire1,(60,60)),(x-30,y-30))
                    pygame.display.update()
                    fire=False
                    enemy_tank.health-=5
                    if enemy_tank.health==0:
                        for i in range(15):
                                time.sleep(0.03)
                                win.blit(bg,(0,0))
                                self.draw(win,itur,ibod,x_barrier)
                                if i>12:
                                    pass
                                else:
                                    enemy_tank.draw(win,x_barrier)
                                pygame.draw.rect(win,colour('d_red'),(d_width//8,d_height//6,d_width//4,d_height//20))
                                barriers(x_barrier,y_barrier)
                                win.blit(dg,(0,d_height-dg.get_rect().height))
                                win.blit(exp[i],(enemy_tank.x-100,enemy_tank.y-250))
                                pygame.display.update()
                                k=0
                                while k<100000:
                                    k+=1
                    time.sleep(0.4)
                if y>d_height*55//60-y_barrier and x_barrier<x<x_barrier+20:
                    win.blit(pygame.transform.scale(fire1,(60,60)),(x-30,y-30))
                    pygame.display.update()
                    time.sleep(0.4)
                    fire=False
                if y>d_height*54//60:
                    win.blit(pygame.transform.scale(fire1,(60,60)),(x-30,y-30))                    
                    pygame.display.update()
                    time.sleep(0.4)
                    fire=False

class enemy(object):
    def __init__(self,x,y,angle):
        self.x = 100
        self.y = y
        self.angle=angle
        self.health=100
        self.hit=0
    def rand(self):
        self.shift=random.randint(-d_width//10,d_width//10)
        self.angle_shift=random.randint(-3,3)
    def mind(self):
        R=tank.x+self.Im.get_rect().center[0]-(self.x+self.Im.get_rect().center[0]+self.Im.get_rect().center[0]*m.cos(self.angle*m.pi/180))
        self.exp_angle=(m.pi/2)-0.5*(m.asin(R*10/(self.v)**2))
        self.exp_angle=self.exp_angle*180/m.pi
    def draw(self,win,x_barrier):
        self.hitbox=(self.x-2,self.y-20,4+tank_body[4].get_rect().width*9//14,tank_body[4].get_rect().height*3//2)
        self.Im=pygame.transform.flip(pygame.transform.scale(tank_turret[4],(tank_turret[itur].get_rect().width//2,tank_turret[itur].get_rect().height*4//5)),1,0)
        rot_tank_turret=pygame.transform.rotate(self.Im,-self.angle)
        turret_rect_center=rot_tank_turret.get_rect().center
        pygame.draw.circle(win,(80,80,14),(int(self.x+self.Im.get_rect().center[0]*0.9),int(self.y)),18)
        win.blit(rot_tank_turret,(self.x+self.Im.get_rect().center[0]-turret_rect_center[0],self.y-5-turret_rect_center[1]))
        win.blit(pygame.transform.flip(pygame.transform.scale(tank_body[4],(int(tank_body[4].get_rect().width*9/14),int(tank_body[4].get_rect().height*0.8))),1,0),(self.x,self.y))
        pygame.draw.rect(win,colour('d_red'),(d_width//8,d_height//6,d_width//4,d_height//20))
        pygame.draw.rect(win,colour('green'),(d_width//8,d_height//6,self.health*2*d_width//800,d_height//20))
        if self.angle<-90:
            self.angle+=1
        elif self.angle>5:
            self.angle-=1
        if self.x<0:
            self.x+=3
        elif self.x+100>x_barrier:
            self.x-=3
    def fire(self,x_barrier,y_barrier):
        fire1=pygame.image.load('firecircle1.png')
        g=10
        self.v=m.sqrt(10*d_width)
        self.rand()
        if self.x<=10:
            self.shift=abs(self.shift)
        elif self.x>=x_barrier-10:
            self.shift=-abs(self.shift)
        else:
            pass
        while self.shift!=0:
            if self.x<0:
                break
            clock.tick(24)
            if self.shift<0:
                self.x-=3
                self.shift+=1
            else:
                self.x+=3
                self.shift-=1
            win.blit(bg,(0,0))
            self.draw(win,x_barrier)
            tank.draw(win,itur,ibod,x_barrier)
            barriers(x_barrier,y_barrier)
            win.blit(dg,(0,d_height-dg.get_rect().height))
            pygame.display.update()
        self.mind()
        t=int(-self.exp_angle)+self.angle_shift-self.angle
        while t!=0:
            if t<0:
                self.angle-=1
                t+=1
            else:
                self.angle+=1
                t-=1
            win.blit(bg,(0,0))
            self.draw(win,x_barrier)
            tank.draw(win,itur,ibod,x_barrier)
            barriers(x_barrier,y_barrier)
            win.blit(dg,(0,d_height-dg.get_rect().height))
            pygame.display.update()
        v_x=self.v*m.cos(-self.angle*m.pi/180)
        v_y=self.v*m.sin(-self.angle*m.pi/180)
        x=self.x+self.Im.get_rect().center[0]+self.Im.get_rect().center[0]*m.cos(self.angle*m.pi/180)
        y=self.y+self.Im.get_rect().center[0]*m.sin(self.angle*m.pi/180)-2
        win.blit(bg,(0,0))
        self.draw(win,x_barrier)
        tank.draw(win,itur,ibod,x_barrier)
        barriers(x_barrier,y_barrier)
        win.blit(dg,(0,d_height-dg.get_rect().height))
        fire=True
        c=0
        while fire:
            win.blit(pygame.transform.scale(fire1,(6,6)),(int(x)-3,int(y)-3))
            x=x+v_x/10
            v_y=v_y-g/10
            y=y-v_y/10
            clock.tick(fps*10)
            pygame.display.update()
            l=tank.hitbox
            if l[0]+l[2]>x>l[0] and l[1]+l[3]>y>l[1]:
                c+=1
            if c==2:
                fire=False
                tank.health-=5
                self.hit+=1
                if tank.health>0:
                    win.blit(pygame.transform.scale(fire1,(60,60)),(x-30,y-30))
                    pygame.display.update()
                if tank.health==0:
                        for i in range(15):
                                time.sleep(0.03)
                                win.blit(bg,(0,0))
                                self.draw(win,x_barrier)
                                if i>12:
                                    pass
                                else:
                                    tank.draw(win,itur,ibod,x_barrier)
                                display.msg_2_screen("POWER:"+str(tank.power)+"%",'AgencyFB',colour('black'),0,-200,40)
                                display.msg_2_screen("ANGLE:"+str(-tank.angle),'AgencyFB',colour('black'),0,-160,40)
                                pygame.draw.rect(win,colour('d_red'),(d_width*5//8,d_height//6,d_width//4,d_height//20))
                                barriers(x_barrier,y_barrier)
                                win.blit(dg,(0,d_height-dg.get_rect().height))
                                win.blit(exp[i],(tank.x-100,tank.y-250))
                                pygame.display.update()
                                k=0
                                while k<100000:
                                    k+=1
                time.sleep(0.4)
            if y>d_height*55//60-y_barrier and x_barrier<x<x_barrier+20:
                win.blit(pygame.transform.scale(fire1,(60,60)),(x-30,y-30))
                pygame.display.update()
                time.sleep(0.25)
                fire=False
            if y>d_height*54//60:
                win.blit(pygame.transform.scale(fire1,(60,60)),(x-30,y-30))
                pygame.display.update()
                time.sleep(0.25)
                fire=False
#############################################################################################################################################################################################
#ALL THE FUNCTIONS
def colour(colour):
    d_clr={"black":(0,0,0),
           "white":(255,255,255),
           "purple":(128,0,128),
           "green":(0,255,0),
           "cyan":(0,255,255),
           "yellow":(255,255,0),
           "magenta":(255,0,255),
           "red":(235,0,0),
           "b_green":(127,255,0),
           "lavender":(230,230,255),
           "orange":(255,127,80),
           "grey":(150,150,150),
           "blue":(0,0,255),
           "d_red":(175,0,0),
           "d_green":(0,150,0),
           "d_yellow":(175,175,0),
           "d_blue":(0,0,160),
           "d_grey":(100,100,100)}
    if type(colour)==tuple:
        return colour
    clr_code=d_clr[colour]
    return clr_code

def fontor(f_name="centurygothic",size=25,b=False,i=False,f_lcn=""):
    global font
    if len(f_lcn)==0:
        font=pygame.font.SysFont(str(f_name),size,b,i)
    else:
        f_lcn=f_lcn+"\\"+f_name
        font=pygame.font.Font(f_lcn,size,b,i)
    return font

def pause():
    i=1
    while i>0:
        display.msg_2_screen('PAUSED','arial',colour('black'),0,0,100,True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.display.quit()
            if event.type==pygame.KEYDOWN:
                i=-1

def game_intro():
    global intro,cmd
    intro=True
    cmd=None
    while intro:
        win.fill(colour("lavender"))
        display.msg_2_screen("TANKS!","calibri","d_green",0,-d_height*3//10,d_height//5,True,True)
        display.msg_2_screen("HS14","calibri","black",d_width*2//5,int(d_height*0.9),30,True,True)
        tank=pygame.transform.scale(pygame.image.load('tank.png'),(d_width*3//4,d_height//2))
        win.blit(tank,((d_width-tank.get_rect().width)//2,(d_height-tank.get_rect().height)//2))
        cmd=display.button(int(d_width/2),int(0.8*d_height),d_width/5,d_height/10,"d_red","red","controls")
        if cmd==None:
            cmd=display.button(int(d_width/4),int(0.8*d_height),d_width*3/20,d_height/10,"d_green","green","play")
        display.button(int(d_width*3/4),int(0.8*d_height),d_width*3/20,d_height/10,"grey","d_grey","quit")
        
        display.text_2_button(int(d_width/4),int(d_height*0.8),"PLAY","SakkalMajalla","purple",int(d_width/20),b=True)
        display.text_2_button(int(d_width/2),int(0.8*d_height),"CONTROLS","SakkalMajalla","orange",int(d_width/20),b=True)
        display.text_2_button(int(d_width*3/4),int(0.8*d_height),"QUIT","SakkalMajalla","black",int(d_width/20),b=True)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                1/0
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    1/0                    
                else:
                   pass
        if cmd!=None:
            intro=False
        pygame.display.update()

def controls():
    global g_cont,cmd
    g_cont=True
    cmd=None
    while g_cont:
        win.fill(colour('lavender'))
        display.msg_2_screen("Controls",'AgencyFB',colour('red'),0,-d_height//5,30*d_height//300)
        display.msg_2_screen("Pause:P",'calibri',colour('black'),0,-d_height//20,30*d_height//600)
        display.msg_2_screen("Move Turret:Up and Down key",'calibri',colour('black'),0,0,30*d_height//600)
        display.msg_2_screen("Move Tank: Left and Right key",'calibri',colour('black'),0,d_height//20,30*d_height//600)
        display.msg_2_screen("Alter Power: A and D key",'calibri',colour('black'),0,d_height//10,30*d_height//600)
        display.msg_2_screen("Shoot:SPACE",'calibri',colour('black'),0,d_height*3//20,30*d_height//600)

        cmd=display.button(int(d_width/4),int(0.8*d_height),d_width*3/20,d_height/10,colour('d_green'),colour('green'),"play")
        display.button(int(3*d_width/4),int(0.8*d_height),d_width*3/20,d_height/10,colour('d_red'),colour('red'),"quit")

        display.text_2_button(int(d_width/4),int(0.8*d_height),"PLAY","SakkalMajalla",colour("purple"),size=40,b=True)
        display.text_2_button(int(3*d_width/4),int(0.8*d_height),"QUIT","SakkalMajalla",colour("black"),size=40,b=True)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.display.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    1/0
                else:
                   pass 
        pygame.display.update()
        if cmd!=None:
            g_cont=False

def custom():
    tur=True
    bod=True
    l=[(d_width//2,d_height//2),(d_width//4,d_height//3),(d_width*3//4,d_height//3),(d_width//4,d_height*2//3),(d_width*3//4,d_height*2//3)]
    while tur:
        win.fill(colour('lavender'))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.display.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    1/0
                else:
                    pass
        display.msg_2_screen('CUSTOMIZE','AgencyFB',colour('purple'),0,-d_height*2//5,d_width//10,b=True)
        display.msg_2_screen('Choose Turret','AgencyFB',colour('red'),0,-d_height*3//10,d_width//20)
        i0=display.button1(0,l[0][0],l[0][1],0,0)
        i1=display.button1(1,l[1][0],l[1][1],1,0)
        i2=display.button1(2,l[2][0],l[2][1],2,0)
        i3=display.button1(3,l[3][0],l[3][1],3,0)
        i4=display.button1(4,l[4][0],l[4][1],4,0)
        if i0!=None or i1!=None or i2!=None or i3!=None or i4!=None:
            tur=False
        pygame.display.update()
    l1=[i0,i1,i2,i3,i4]
    time.sleep(0.15)
    for me in l1:
        if me!=None:
            i_turret=me
    while bod:
        win.fill(colour('lavender'))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.display.quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    1/0
                else:
                    pass
        display.msg_2_screen('CUSTOMIZE','AgencyFB',colour('purple'),0,-d_height*2//5,d_width//10,b=True)
        display.msg_2_screen('Choose Tank Body','AgencyFB',colour('red'),0,-d_height*3//10,d_width//20)
        i0=display.button1(0,l[0][0],l[0][1],0,1)
        i1=display.button1(1,l[1][0],l[1][1],1,1)
        i2=display.button1(2,l[2][0],l[2][1],2,1)
        i3=display.button1(3,l[3][0],l[3][1],3,1)
        i4=display.button1(4,l[4][0],l[4][1],4,1)
        if i0!=None or i1!=None or i2!=None or i3!=None or i4!=None:
            bod=False
        pygame.display.update()
    l1=[i0,i1,i2,i3,i4]
    for me in l1:
        if me!=None:
            i_body=me
    return i_turret,i_body

wall=pygame.transform.scale(pygame.image.load('wall.jpg'),(d_width//4,d_height//2))
def barriers(x,y):
    win.blit(wall,(x,(d_height*55//60)-y),(0,0,20,y))

def play(itur,ibod):
    p_cont=True
    x_barrier=random.randint(-d_width//20+d_width//2,d_width//20+d_width//2)
    y_barrier=random.randint(d_height//6,d_height//2)
    while p_cont:
        win.blit(bg,(0,0))
        if tank.health>0:
            tank.draw(win,itur,ibod,x_barrier)
        else:
            pygame.draw.rect(win,colour('d_red'),(d_width*5//8,d_height//6,d_width//4,d_height//20))
            display.msg_2_screen("POWER:"+str(tank.power)+"%",'AgencyFB',colour('black'),0,-d_height//3,40)
            display.msg_2_screen("ANGLE:"+str(-tank.angle),'AgencyFB',colour('black'),0,-d_height*4//15,40)
            p_cont=False
        if enemy_tank.health>0:
            enemy_tank.draw(win,x_barrier)
        else:
            pygame.draw.rect(win,colour('d_red'),(d_width//8,d_height//6,d_width//4,d_height//20))
            p_cont=False
        barriers(x_barrier,y_barrier)
        win.blit(dg,(0,d_height-dg.get_rect().height))
        pygame.display.update()
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    1/0
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_q:
                        1/0
                    elif event.key==pygame.K_SPACE:
                        if tank.health>0:
                            tank.fire(x_barrier,y_barrier,itur,ibod)
                        if enemy_tank.health>0:
                            enemy_tank.fire(x_barrier,y_barrier)
                    elif event.key==pygame.K_p:
                        pause()
                    else:
                       pass
        clock.tick(fps)

def end():
    time.sleep(1)
    for i in range(d_width//2):
        win.blit(door,(i-d_width//2+2,0),(0,0,d_width//2,d_height))
        win.blit(door,(d_width-i,0),(d_width//2,0,d_width//2,d_height))
        pygame.display.update()
        if i<d_width*2//3:
            clock.tick(fps*4)
        else:
            clock.tick(fps*2)
    if enemy_tank.health==0:
        display.msg_2_screen('YOU WON!','battlestar',colour('d_red'),30,0,120)
    else:
        display.msg_2_screen('YOU LOST!','battlestar',colour('d_red'),30,0,120)
    pygame.display.update()
    time.sleep(2)
    win.blit(door,(0,0))
    pygame.display.update()
    time.sleep(0.5)
    for i in range(d_width//2,0,-1):
        win.blit(door,(i-d_width//2,0),(0,0,d_width//2,d_height))
        win.blit(door,(d_width-i,0),(d_width//2,0,d_width//2,d_height))
        pygame.display.update()
        clock.tick(fps*4)
        
def aftergame():
    aft=True
    cmd=None
    while aft:
        win.fill(colour('lavender'))
        display.msg_2_screen('WELL PLAYED','agencyfb',colour('d_grey'),0,-d_height//3,80,True)
        display.msg_2_screen('What would you like to do?','timesnewroman',colour('d_red'),0,-d_height//12,50)
        cmd=display.button(int(d_width/4),int(0.7*d_height),d_width*3/20,d_height/10,"d_green","green","home")
        if cmd==None:
            cmd=display.button(int(d_width/2),int(0.7*d_height),d_width/5,d_height/10,"d_red","red","scores")
        display.button(int(d_width*3/4),int(0.7*d_height),d_width*3/20,d_height/10,"grey","d_grey","quit")
        display.text_2_button(int(d_width/4),int(d_height*0.7),"HOME","SakkalMajalla","purple",int(d_width/20),b=True)
        display.text_2_button(int(d_width/2),int(0.7*d_height),"SCORES","SakkalMajalla","orange",int(d_width/20),b=True)
        display.text_2_button(int(d_width*3/4),int(0.7*d_height),"QUIT","SakkalMajalla","black",int(d_width/20),b=True)
        if cmd!=None:
            aft=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                1/0
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_q:
                    1/0                    
                else:
                   pass
        pygame.display.update()
    return cmd

def enter_score():
    win.fill(colour('lavender'))
    display.msg_2_screen('ENTER SCORE','agencyfb',colour('purple'),0,-200,90,True)
    display.msg_2_screen('NAME','calibri',colour('d_blue'),-180,-40,60)
    display.msg_2_screen('HEALTH:','calibri',colour('d_blue'),-180,30,60)
    display.msg_2_screen('HITS:','calibri',colour('d_blue'),-180,100,60)
    display.msg_2_screen(str(tank.health),'calibri',colour('d_green'),0,30,60)
    display.msg_2_screen(str(enemy_tank.hit),'calibri',colour('d_green'),0,100,60)
    done=False
    clr=(240,240,240)
    name=''
    while not done:
        cur=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()
        pygame.draw.rect(win,clr,(320,235,200,40))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                1/0
            if 320<cur[0]<520 and 235<cur[1]<275:
                if click[0]==1:
                    clr=colour('white')
            if event.type==pygame.KEYDOWN and clr==colour('white'):
                if event.key==8:
                    name=name[:-1]
                elif len(name)<10:
                    name+=event.unicode
                else:
                    pass
            if event.type==pygame.KEYDOWN and clr!=colour('white'):
                if event.unicode=='q':
                    1/0
        if clr!=colour('white'):
            display.msg_2_screen('Click Here','calibri',(180,180,180),20,-45,35)
        display.msg_2_screen(name,'calibri',colour('black'),20,-45,35)
        done=display.button(int(d_width*3/4),int(0.8*d_height),d_width*3/20,d_height/10,"green","d_green","next")
        display.text_2_button(int(d_width*3/4),int(0.8*d_height),'NEXT','agencyfb',colour('d_red'),40)
        pygame.display.update()
    con,cur=scores_init(name)
    return con,cur

def scores_init(name):
    con=sq.connect('scores.db')
    cur=con.cursor()
    try:
        cur.execute('create table score(NAME text,HITS integer,TANKHEALTH integer)')
        con.commit()
    except:
        pass
    finally:
        if tank.health>0:
            cur.execute('insert into score values(\'{}\',\'{}\',\'{}\')'.format(name,enemy_tank.hit,tank.health))
            print('done')
            con.commit()
        cur.execute('select hits from score')
        r=cur.fetchall()
        ar=copy.copy(r)
        r.sort()
        if len(r)>5:
            r=r[:4]
        for i in range(len(ar)):
            if ar[i] in r:
                pass
            else:
                cur.execute('delete from score where hits=%s'%ar[i])
                con.commit()
        con.commit()
    return con,cur

def scores(con,cur):
    cur.execute('select * from score order by hits,tankhealth desc')
    record=cur.fetchall()
    win.fill(colour('lavender'))
    display.msg_2_screen('HIGH SCORES','agencyfb',colour('purple'),0,-250,80)
    done=False
    g_coord=[]
    for j in range(100,400,50):
        l=[]
        for i in (200,400,500):
            l.append((i,j))
        g_coord.append(l)
    for j in range(100,401,50):
        pygame.draw.line(win,colour('black'),(200,j),(600,j),5)
    for i in (200,400,500,600):
        pygame.draw.line(win,colour('black'),(i,100),(i,400),5)
    pygame.display.update()
    head_in=g_coord[0]
    g_coord=g_coord[1:]
    display.msg_2_screen('NAME','agencyfb',colour('black'),head_in[0][0]-d_width//2+100,head_in[0][1]-d_height//2+25,40)
    display.msg_2_screen('HITS','agencyfb',colour('black'),head_in[1][0]-d_width//2+50,head_in[1][1]-d_height//2+25,40)
    display.msg_2_screen('HEALTH','agencyfb',colour('black'),head_in[2][0]-d_width//2+50,head_in[2][1]-d_height//2+25,40)
    while not done:
        done=display.button(int(d_width*3/4),int(0.8*d_height),d_width*3/20,d_height/10,"red","d_red","back")
        display.text_2_button(int(d_width*3/4),int(0.8*d_height),'BACK','calibri',colour('orange'),40)
        try:
            for i in range(5):
                display.msg_2_screen(record[i][0],'calibri',colour('black'),g_coord[i][0][0]-d_width//2+100,g_coord[i][0][1]-d_height//2+25,30)
                display.msg_2_screen(str(record[i][1]),'calibri',colour('black'),g_coord[i][1][0]-d_width//2+50,g_coord[i][1][1]-d_height//2+25,30)
                display.msg_2_screen(str(record[i][2]),'calibri',colour('black'),g_coord[i][2][0]-d_width//2+50,g_coord[i][2][1]-d_height//2+25,30)
        except:
            pass
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                1/0
        pygame.display.update()
#############################################################################################################################################################################################
#final gameloop
tank=player(5*d_width/8,int(5.08*d_height/6),0)
enemy_tank=enemy(1*d_width/8,int(5.08*d_height/6),0)
try:
    c=True
    while c:
        game_intro()
        if cmd=='controls':
            controls()
        if cmd=='play':
            itur,ibod=custom()
            tank.health=100
            enemy_tank.health=100
            tank.angle=enemy_tank.angle=0
            tank.power=100
            play(itur,ibod)
            end()
            if tank.health>0:
                con,cur=enter_score()
            else:
                con=sq.connect('scores.db')
                cur=con.cursor()                
            while cmd!='home':
                cmd=aftergame()
                if cmd=='scores':
                    scores(con,cur)
except Exception as e:
    print(e)
    del font
    pygame.display.quit()
    pygame.quit()
    print('end')
##############END###########################END###########################END###########################END###########################END###########################END#####################