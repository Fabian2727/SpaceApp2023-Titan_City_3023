import pygame
import random
from queue import Queue
from pygame import mixer

pygame.init()

#Seleccionando el nivel
minigame=0

def display_text(surface, text, pos, font, color):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x,y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width , word_height = word_surface.get_size()
            if x + word_width >= 800:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_width + space
        x = pos[0]
        y += word_height

#Clase que nos permite dividir un spritesheet
class SpriteSheet():
	def __init__(self, image):
		self.sheet = image

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image

class button():
	def __init__(self,x,y,image,scale):
		width=image.get_width()
		height=image.get_height()
		self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
		self.rect=self.image.get_rect()
		self.rect.topleft=(x,y)
		self.clicked=False

	def draw(self,screen):
		action=False
		pos=pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
				action=True
				self.clicked=True
		
		if pygame.mouse.get_pressed()[0]==0:
				self.clicked=False

		screen.blit(self.image,(self.rect.x, self.rect.y))

		return action


#Clase que nos permite crear una animacion de un spritesheet
class animation():
	sprite_sheet=SpriteSheet
	def __init__(self,path,steps,cooldown,pwidth,pheight):
		sprite_sheet_path=pygame.image.load(path)
		self.sprite_sheet=SpriteSheet(sprite_sheet_path)
		self.animation_steps=steps
		self.animation_cooldown=cooldown
		self.width=pwidth
		self.height=pheight
		self.last_update=pygame.time.get_ticks()
		self.frame=0
		self.frames=[]
		self.cont=0
		self.pisadasWav=[pygame.mixer.Sound('assets\sounds\pisada1.wav'),pygame.mixer.Sound('assets\sounds\pisada2.wav')]
		self.tormentaWav=pygame.mixer.Sound('assets\sounds\\tormenta.wav')
		self.tormentaWav.set_volume(0.1)


	def make_animation(self, scale,colour):
		animation_list=[]
		for x in range(self.animation_steps):
			animation_list.append(self.sprite_sheet.get_image(x,self.width,self.height,scale,colour))
		return animation_list
	
	def update_animation(self,animation_list,anim):
		currentTime = pygame.time.get_ticks()
		if currentTime - self.last_update >= self.animation_cooldown:
			self.frame+=1
			self.last_update=currentTime
			if self.frame >= len(animation_list):
				self.frame=0
				self.cont=(self.cont+1)%2
				if anim==0:
					self.pisadasWav[self.cont].play()
				elif anim==1 and self.cont==1:
					self.tormentaWav.play()

#clase que permite jugar el juego de las teclas
class Keys_game():
	def __init__(self,path,steps,pwidth,pheight,scale):
		sprite_sheet_path=pygame.image.load(path)
		self.sprite_sheet=SpriteSheet(sprite_sheet_path)
		self.nkeys=steps
		self.width=pwidth
		self.height=pheight
		self.scale=scale
		self.frames=[]
		self.moves=Queue(maxsize=0)
	
	def random_keys_game(self, totalRand, colour):
		for x in range(totalRand):
			num=random.randint(0,3)
			self.frames.append(self.sprite_sheet.get_image(num ,self.width ,self.height ,self.scale,colour))
			match num:
				case 0:
					self.moves.put('w')
				case 1:
					self.moves.put('a')
				case 2:
					self.moves.put('s')
				case 3:
					self.moves.put('d')

class minigame1():
	def __init__(self):
		self.Astronaut=animation('assets\sprites\Minijuego1\AstronautaMin1.png',2,500,320,320)
		self.Astronaut_animation=self.Astronaut.make_animation(1,BLACK)
		self.Tornado=animation('assets\sprites\Minijuego1\TornadoMin1.png',3,500,400,640)
		self.Tornado_animation=self.Tornado.make_animation(1,BLACK)
		self.Tornado2=animation('assets\sprites\Minijuego1\TornadoMin1.png',3,500,400,640)
		self.Tornado_animation2=self.Tornado2.make_animation(1,BLACK)
		self.Teclas=Keys_game('assets\sprites\Minijuego1\TeclasMin1.png',4,240,240,0.4)
		self.Teclas.random_keys_game(4,BLACK)
		self.backG=pygame.image.load('assets\sprites\Minijuego1\FondoMin1.png').convert_alpha()
		self.backG=pygame.transform.scale(self.backG, (int(self.backG.get_width()*1.2),int(self.backG.get_height()*1.2)))
		self.gameOver=pygame.image.load('assets\sprites\Minijuego1\Game_over.png').convert_alpha()
		self.gameOver=pygame.transform.scale(self.gameOver, (int(self.gameOver.get_width()*0.2),int(self.gameOver.get_height()*0.2)))

		self.nubeimg=pygame.image.load('assets\sprites\Minijuego1\\NubeMin1.png').convert_alpha()
		self.nubeimg=pygame.transform.scale(self.nubeimg, (int(self.nubeimg.get_width()*2),int(self.nubeimg.get_height()*1)))
		self.A1=pygame.Rect(0,400,320,320)
		self.A2=pygame.Rect(-600,0,120,920)
		self.A3=pygame.Rect(-900,0,120,920)
		self.A4=pygame.Rect(-1500,-150,360,360)
		self.velAstro=1.8
		self.lose=0
		self.angle=0
		self.Astronaut_animation_rotated=pygame.image

	def load_minigame(self,screen,SCREEN_WIDTH,SCREEN_HEIGHT):
			
			screen.fill(BG)
			screen.blit(self.backG,(0,0))
			cont=1

			if pygame.Rect.colliderect(self.A1,self.A2):
				screen.blit(self.gameOver,(SCREEN_WIDTH/2-250,SCREEN_HEIGHT/2-200))
				pygame.display.update()
				pygame.time.wait(2000)
				return 1
			
			if self.A1.x>=SCREEN_WIDTH:
				return 1

			#Actualizar animacion
			self.Tornado.update_animation(self.Tornado_animation,1)
			self.Tornado2.update_animation(self.Tornado_animation2,1)

			#Dibujar imagen
			screen.blit(self.Tornado_animation[self.Tornado.frame], (self.A2.x, self.A2.y))
			screen.blit(self.Tornado_animation2[self.Tornado2.frame], (self.A3.x, self.A3.y))
			screen.blit(self.nubeimg,(self.A4.x,self.A4.y))

			if self.lose==0:
				screen.blit(self.Astronaut_animation[self.Astronaut.frame], (self.A1.x, self.A1.y))
				self.Astronaut.update_animation(self.Astronaut_animation,0)

				if len(self.Teclas.frames)==0:
					self.velAstro=4
					self.Astronaut.animation_cooldown=200

				#Dibujar teclas
				for x in range(len(self.Teclas.frames)):
					screen.blit(self.Teclas.frames[x], ((SCREEN_WIDTH/2-self.Teclas.width*self.Teclas.scale*len(self.Teclas.frames)/2)+(x*self.Teclas.width*self.Teclas.scale), SCREEN_HEIGHT-self.Teclas.frames[0].get_height()))
			else:
				self.velAstro=0
				if self.angle<90:
					self.Astronaut_animation_rotated=pygame.transform.rotate(self.Astronaut_animation[self.Astronaut.frame],self.angle).convert_alpha()
					self.angle+=1
					self.A1.y+=1

				screen.blit(self.Astronaut_animation_rotated, (self.A1.x, self.A1.y))

			#Movimiento de animacion
			self.A1.x+=self.velAstro
			self.A2.x+=3
			self.A3.x+=3
			self.A4.x+=3

			#El minijuego sigue funcionando
			return 2
	
	def key_inputs(self,event):
		if event.type == pygame.KEYDOWN and len(self.Teclas.frames)!=0:  
			if event.key == pygame.K_w and self.Teclas.moves.queue[0]=='w':
				self.Teclas.frames.pop(0)
				self.Teclas.moves.get()
			elif event.key == pygame.K_a and self.Teclas.moves.queue[0]=='a':
				self.Teclas.frames.pop(0)
				self.Teclas.moves.get()				
			elif event.key == pygame.K_s and self.Teclas.moves.queue[0]=='s':
				self.Teclas.frames.pop(0)
				self.Teclas.moves.get()				
			elif event.key == pygame.K_d and self.Teclas.moves.queue[0]=='d':
				self.Teclas.frames.pop(0)
				self.Teclas.moves.get()	
			else:
				self.lose=1

class menu():
	btStart=pygame.image
	tiStart=pygame.image
	bg=pygame.image
	btStartload=button
	def __init__(self):
		self.btStart=pygame.image.load('assets\sprites\MainMenu\Boton.png').convert_alpha()
		
		self.tiStart=pygame.image.load('assets\sprites\MainMenu\Titulo1.png').convert_alpha()
		self.tiStart=pygame.transform.scale(self.tiStart, (int(self.tiStart.get_width()*0.35),int(self.tiStart.get_height()*0.35)))
		self.bg=pygame.image.load('assets\sprites\MainMenu\\bg.png').convert_alpha()
		self.bg=pygame.transform.scale(self.bg,(int(self.bg.get_width()*0.4),int(self.bg.get_height()*0.4)))
		self.btStartload=button(400,580,self.btStart,0.3)

		self.MenuWav=pygame.mixer.Sound('assets\sounds\comandante.wav')
		self.MenuWav.set_volume(0.4)
	
	def menu_load(self,screen):
		minigame=0

		screen.blit(self.bg,(200,80))
		screen.blit(self.tiStart,(220,0))

		if self.btStartload.draw(screen):
			self.MenuWav.play()
			minigame=1
		
		return minigame
	
class Nave():
	def __init__(self):
		self.TxtBox=pygame.image.load('assets\sprites\Hub\TxtBox.png').convert_alpha()
		self.TxtBox=pygame.transform.scale(self.TxtBox,((int(self.TxtBox.get_width()*0.42),int(self.TxtBox.get_height()*0.18))))
		self.NaveIm=pygame.image.load('assets\sprites\Hub\RoomNave.png').convert_alpha()
		self.NaveIm=pygame.transform.scale(self.NaveIm,((int(self.NaveIm.get_width()*2.8),int(self.NaveIm.get_height()*2.2))))
		self.Comandante=pygame.image.load('assets\sprites\Hub\Comandante.png').convert_alpha()
		self.Comandante=button(0,370,self.Comandante,0.20)
		self.buttonimg=pygame.image.load('assets\sprites\Hub\HubNext.png').convert_alpha()
		self.Nextbttn=button(930,480,self.buttonimg,0.20)
		self.Chatbox=pygame.image.load('assets\sprites\Hub\input_box.png').convert_alpha()
		self.Chatbox=pygame.transform.scale(self.Chatbox,((int(self.Chatbox.get_width()*0.4),int(self.Chatbox.get_height()*0.2))))

		self.ComandanteWav=pygame.mixer.Sound('assets\sounds\comandante.wav')
		self.ComandanteWav.set_volume(0.4)

		self.fontObj = pygame.font.Font(None, 32)
		self.textCom=['Attention all ships! This is the Commander speaking. I have some urgent news. A massive methane storm is headed our way. It is expected to hit within the hour.','Methane is a greenhouse gas that is much more potent than carbon dioxide, so methane storms can be very dangerous.']
		self.chat=False
		self.usertxt=''
		self.userfont=pygame.font.Font(None,32)
		self.inputrect=pygame.Rect(600,30,140,32)
		self.inputActive=False
		self.showtext=False
		self.cont=-1

	def load_nave(self,screen):
		screen.blit(self.NaveIm,(0,0))
		screen.blit(self.Chatbox,(400,-100))
		if self.Nextbttn.draw(screen) and minigame==1:
			self.ComandanteWav.play()
			return 2

		if self.Comandante.draw(screen) and minigame==1:
			self.ComandanteWav.play()
			self.chat=True
			self.showtext=True
			if self.cont<1:
				self.cont+=1

		if self.chat:
			screen.blit(self.TxtBox,(120,300))

		if self.showtext:
			display_text(screen,self.textCom[self.cont],(440,370),self.fontObj,(200,100,0))

		display_text(screen,'Type here:',(438,40),self.fontObj,(10,20,200))
		text_surface = self.userfont.render(self.usertxt,True,(255,255,255))
		screen.blit(text_surface,(self.inputrect.x+5,self.inputrect.y+5))
		self.inputrect.w=max(100,text_surface.get_width()+10)

		return 1
	
	def inputbox(self,event):
		if event.type==pygame.MOUSEBUTTONDOWN:
			if self.inputrect.collidepoint(event.pos):
				self.ComandanteWav.play()
				self.inputActive=True
			else:
				self.inputActive=False

		if event.type == pygame.KEYDOWN:
			if self.inputActive:
				if event.key == pygame.K_BACKSPACE:
					self.usertxt=self.usertxt[:-1]
				else:
					self.usertxt+=event.unicode



SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Titan3023')

BG = (50, 50, 50)
BLACK = (0, 0, 0)
fps=60

menu_inst=menu()
minigame1_inst=minigame1()
Nave_inst=Nave()

backmusic=pygame.mixer.Sound('assets\sounds\SOUNDTRACK.wav')
backmusic.set_volume(0.3)
menu_music=False
musicPlaying=False

#Creando un clock para limitar los Fps
clock=pygame.time.Clock()
run = True
while run:
	clock.tick(fps)

	#update background
	screen.fill(BG)	

	if menu_music:
		backmusic.play()
		menu_music=False

	match minigame:
		case 0:
			if musicPlaying==False:
				menu_music=True
				musicPlaying=True
			minigame=menu_inst.menu_load(screen)
			if minigame!=0:
				musicPlaying=False
				backmusic.stop()
		case 1:
			minigame=Nave_inst.load_nave(screen)
			if minigame!=1:
				del Nave_inst
				Nave_inst=Nave()
		case 2:
			minigame=minigame1_inst.load_minigame(screen,SCREEN_WIDTH,SCREEN_HEIGHT)
			if(minigame!=2):
				del minigame1_inst
				minigame1_inst=minigame1()
				pygame.mixer.stop()



	pygame.display.update()

	for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False	
				if minigame==1:
					Nave_inst.inputbox(event)
				if minigame==2:
					minigame1_inst.key_inputs(event)

pygame.quit()