#usr/bin/python3
from pygame import *
from random import randint
import json as js

init()
window = display.set_mode((500, 500))

font.init()
fonte = font.Font("PixelOperator-Bold.ttf", 28)

class button:
    def __init__(self, x, y, width, height, text, execute=None):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.font = font.Font(None, 30)
        self.color = (200, 200, 200)
        self.hover_color = (200, 150, 150)
        self.command = execute

    def draw(self):
        mouse_pos = mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color
        draw.rect(window, color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        window.blit(text_surface, (self.rect.x + self.rect.width // 2 - text_surface.get_rect().width // 2, self.rect.y + self.rect.height // 2 - text_surface.get_rect().height // 2))

    def hovers(self):
        if self.rect.collidepoint(mouse.get_pos()):
            return True
        return False

class slider():
	def __init__(self, x, y, width, height, max_volume, radius):
		self.rect = Rect(x, y, width, height)
		self.circle = Rect(x + radius//2, y + height//2, radius, radius)
		self.radius = radius
		self.onevalue = width/int(max_volume)
    
	def hovers(self):
		if self.rect.collidepoint(mouse.get_pos()):
			return True
		return False
    
	def slide(self):
		self.circle.x = mouse.get_pos()[0] - self.circle.width // 2
    
	def getvalue(self):
		return int((self.circle.x + self.circle.width//2 - self.rect.x) / self.onevalue)
	
	def setvalue(self, value):
		self.circle.x = value * self.onevalue + self.rect.x - self.circle.width//2

	def draw(self):
		draw.rect(window, (200, 200, 200), self.rect)
		draw.rect(window, (200, 0, 0), Rect(self.rect.x, self.rect.y, self.circle.x - self.rect.x + self.circle.width//2, self.rect.height))
		draw.circle(window, (100, 100, 100), (self.circle.x, self.circle.y), self.radius)

class hitbox():
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.rect = Rect(self.x, self.y, self.width, self.height)

	def drawhitbox(self):
		draw.rect(window, (0, 0, 0), self.rect, 2)

	def collides(self, otherself):
		return otherself.rect.colliderect(self.rect)

	def update(self):
		self.rect = Rect(self.x, self.y, self.width, self.height)

class textboxME:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.font = font.Font(None, 30)
        self.color = (200, 200, 200)
        self.active = False

    def draw(self, text):
        draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(text, True, (0, 0, 0))
        window.blit(text_surface, (self.rect.x + self.rect.width // 2 - text_surface.get_rect().width // 2, self.rect.y + self.rect.height // 2 - text_surface.get_rect().height // 2))

class Spritesheet:
	def __init__(self, filename, cols, rows, frame_width, frame_height, frame_transform_width, frame_transform_height,
		         spacing=0, border=0):
		self.sheet = image.load(filename).convert_alpha()
		self.cols = cols
		self.rows = rows
		self.frame_width = frame_width
		self.frame_height = frame_height
		self.spacing = spacing
		self.border = border
		self.frames = self._split_frames(frame_transform_width, frame_transform_height)

	def _split_frames(self, width, height):
		frames = []
		for row in range(self.rows):
			for col in range(self.cols):
				x = self.border + col * (self.frame_width + self.spacing)
				y = self.border + row * (self.frame_height + self.spacing)
				frame = transform.scale(self.sheet.subsurface(Rect(x, y, self.frame_width, self.frame_height)),
					                        (width, height))
				frames.append(frame)
		return frames

class Camera:
    def __init__(self, xonmap, yonmap):
        self.coords = {"x": xonmap, "y": yonmap}

    def __getitem__(self, key):
            return self.coords[key]
    
    def __setitem__(self, key, value):
            self.coords[key] = value

    def blitwith(self, Objx, Objy, Objimg):
        window.blit(Objimg, (Objx - self["x"], Objy - self["y"]))

class tilemap():
	class block(hitbox):
		def __init__(self, x, y, width, height, tilemap, tilenumber, hitboxe):
			self.tilemapx = x * width
			self.tilemapy = y * height
			self.id = 0
			self.hitboxe = hitboxe
			self.RDR = Rect(self.tilemapx + width + 1, self.tilemapy + 1, 2 if hitboxe else 0, height-1 if hitboxe else 0)
			self.RDL = Rect(self.tilemapx-2, self.tilemapy+1, 2 if hitboxe else 0, height-1 if hitboxe else 0)
			self.RDD = Rect(self.tilemapx, self.tilemapy+height, width if hitboxe else 0, 1 if hitboxe else 0)
			super().__init__(self.tilemapx, self.tilemapy, width if hitboxe else 0, height if hitboxe else 0)
			self.tiletexture = tilemap.frames[tilenumber]

		def update(self):
			global camerax, cameray
			self.rect = Rect(self.tilemapx, self.tilemapy, self.width, self.height)
			self.RDR = Rect(self.tilemapx + self.width + 1, self.tilemapy + 1, 2 if self.hitboxe else 0, self.height-1 if self.hitboxe else 0)
			self.RDL = Rect(self.tilemapx-2, self.tilemapy+1, 2 if self.hitboxe else 0, self.height-1 if self.hitboxe else 0)
			self.RDD = Rect(self.tilemapx, self.tilemapy+self.height, self.width if self.hitboxe else 0, 1 if self.hitboxe else 0)

		def draw(self):
			global camerax, cameray
			self.update()
			sam.blitwith(self.tilemapx, self.tilemapy, self.tiletexture)

	class door(block):
		def __init__(self, x, y, width, height, tilemap, tilenumber, hitboxe, indexroomnew):
			self.room = indexroomnew
			super().__init__(x, y, width, height, tilemap, tilenumber, hitboxe)
			self.id = 1

		def activate(self, player):
			global indexroom, camerax
			indexroom = self.room
			camerax = -camerax
	
	class ground(block):
		def __init__(self, x, y, width, height, tilemap, tilenumbers, hitboxe, tilenumbercomp):
			self.id = 2
			self.sprite = Surface((25, 25))
			self.sprite.blit(tilenumbercomp[0][tilenumbers[0]], (0, 0))
			self.sprite.blit(tilenumbercomp[1][tilenumbers[1]], (12, 0))
			self.sprite.blit(tilenumbercomp[2][tilenumbers[2]], (0, 12))
			self.sprite.blit(tilenumbercomp[3][tilenumbers[3]], (12, 12))
			self.sprite = transform.scale(self.sprite, (width, height))
			super().__init__(x, y, width, height, tilemap, 0, hitboxe)
		
		def draw(self):
			global camerax, cameray
			self.update()
			sam.blitwith(self.tilemapx, self.tilemapy, self.sprite)

	def __init__(self, filename, cols, rows, frame_width, frame_height, frame_transform_width, frame_transform_height,
		         spacing=0, border=0):
		self.width = frame_transform_width
		self.height = frame_transform_height
		self.tilemap = Spritesheet(filename, cols, rows, frame_width, frame_height, frame_transform_width,
			                       frame_transform_height, spacing, border)
		
	def maptoroom(self, map):
		room = []
		for i in range(len(map)):
			room.append([])
			for j in range(len(map[i])):
				if map[i][j][1][2] == 0:
					room[i].append(self.block(map[i][j][0][0], map[i][j][0][1], self.width, self.height, self.tilemap, map[i][j][1][0], map[i][j][1][1]))
				elif map[i][j][1][2] == 1:
					room[i].append(self.door(map[i][j][0][0], map[i][j][0][1], self.width, self.height, self.tilemap, map[i][j][1][0], map[i][j][1][1], map[i][j][1][3]))
				elif map[i][j][1][2] == 2:
					room[i].append(self.ground(map[i][j][0][0], map[i][j][0][1], self.width, self.height, self.tilemap, map[i][j][2], map[i][j][1][1], groundsprites if map[i][j][1][0] == "ground" else mosssprites if map[i][j][1][0] == "moss" else []))	 
		return room


class Player(hitbox):
	def __init__(self, x, y, infosheet_sr, infosheet_sl, infosheet_wr, infosheet_wl, D):
		self.check = [0, 0]
		self.wl = infosheet_wl
		self.wr = infosheet_wr
		self.sl = infosheet_sl
		self.sr = infosheet_sr
		self.fallspeed = 0
		self.grounded = False
		self.run = False
		self.inventar = [None, None, None, None, None, None, None, None, None, None]
		self.interacted = 0
		self.d = D
		self.counter = 0
		self.IShRN = self.sr if D else self.sl
		super().__init__(x, y, self.IShRN["hitbox"][0][0], self.IShRN["hitbox"][0][1])

	def move(self, speed, room):
		global camerax, cameray
		right = False
		left = False
		rightid = 0.5
		leftid = 0.5

		for block in room:
			if self.rect.colliderect(block.RDR):
				right = True
				rightid = block.id
				break
		for block in room:
			if self.rect.colliderect(block.RDL):
				left = True
				leftid = block.id
				break
		

		keys = key.get_pressed()
		if keys[K_d]:
			if (not left) or leftid != 0:
				self.check[1] = 2
				if self.check[0] != self.check[1]:
					self.resetCounter()
					self.check[0] = self.check[1]
				self.d = 1
				self.IShRN = self.wr
				self.x += speed * 2 if self.run else speed

		if keys[K_a]:
			if not right or rightid != 0:
				self.check[1] = 0
				if self.check[0] != self.check[1]:
					self.resetCounter()
					self.check[0] = self.check[1]
				self.d = 0
				self.IShRN = self.wl
				self.x -= speed * 2 if self.run else speed
		if not keys[K_d] and not keys[K_a]:
			self.check[1] = 1
			if self.check[0] != self.check[1]:
				self.resetCounter()
				self.check[0] = self.check[1]
			self.IShRN = self.sr if self.d else self.sl
		if (keys[K_w] or keys[K_SPACE]) and self.grounded:
			self.fallspeed = -10

		self.gravitate(room)
		self.interact(room)
		self.interacted = False
		self.updatehitboxes()
	

	
	def gravitate(self, room):
		global cameray, camerax
		self.grounded = False
		for block in room:
			if self.collides(block) and block.id != 1:
				if not self.rect.colliderect(block.RDD):
					self.grounded = True
					self.y = block.tilemapy - player.height + 1
					self.update()
					break
				elif self.fallspeed < 0:
					self.fallspeed = 0

	
		if not self.grounded or self.fallspeed < 0:
			self.fallspeed += 1
			self.y += self.fallspeed
		else:
			self.fallspeed = 0

	def interact(self, room):
		for block in room:
			if block.id == 1 and self.collides(block):
				if self.interacted == True:
					block.activate(self)
				window.blit(image.load("animations/arrow.png"), (250 if self.d == 1 else 249, 250 - image.load("animations/arrow.png").get_height() - 10))



	def resetCounter(self):
		self.counter = 0

	def updatehitboxes(self):
		bottom = self.y + self.height
		frame_idx = int(self.counter) % len(self.IShRN["hitbox"])
		self.width = self.IShRN["hitbox"][frame_idx][0]
		self.height = self.IShRN["hitbox"][frame_idx][1]
		self.y = bottom - self.height
		super().update()

	def draw(self, r, l):
		frame = int(self.counter) % len(self.IShRN["sprite"])
		offset = -r if self.d == 1 else -l if self.d == 0 else 0
		sam.blitwith(self.x + offset, self.y, self.IShRN["sprite"][frame])

	def incrementCounter(self, by):
		self.counter += by * 2 if self.run else by
		if self.counter >= len(self.IShRN["hitbox"]):
			self.counter = 0

class textbox:
	def __init__(self, x, y, w, h, font, maincolor, textcolor, bordercolor):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.font = font
		self.maincolor = maincolor
		self.bordercolor = bordercolor
		self.textcolor = textcolor

	def draw(self, text, name):
		draw.rect(window, self.maincolor, Rect(self.x, self.y, self.w, self.h))
		draw.rect(window, self.bordercolor, Rect(self.x, self.y, self.w, self.h), 2)
		window.blit(self.font.render(text, False, self.textcolor), (self.x+10, self.y+5))
		draw.polygon(window, self.maincolor, [[self.x, self.y],
											 [self.x + self.font.render(name, False, self.textcolor).get_width()+20, self.y],
											 [self.x+self.font.render(name, False, self.textcolor).get_width()+10, self.y-30],
											 [self.x+10, self.y-30]])
		draw.polygon(window, self.bordercolor, [[self.x, self.y],
											 [self.x + self.font.render(name, False, self.textcolor).get_width()+20, self.y],
											 [self.x+self.font.render(name, False, self.textcolor).get_width()+10, self.y-30],
											 [self.x+10, self.y-30]], 2)
		window.blit(self.font.render(name, False, self.textcolor), (self.x+10, self.y-30))

		

def randomchance(a):
	DL = lambda liste, by: [liste[i:i+by] for i in range(0, len(liste), by)]
	
	if len(a)%2>0:
		raise ValueError('number of elements must be even')
	
	b = DL(a, 2)
	loo = sum(i[1] for i in b)
		
	if loo != 100:
		raise ValueError('chances must add up to 100')
	
	r = randint(1, 100)
	cumulative = 0
	
	for item, chance in b:
		cumulative += chance
		if r <= cumulative:
			return item
		
def save(filename, levels):
    with open(filename, "w") as f:
        f.write(js.dumps(levels, indent=4))

def load(filename):
    try:
        with open(filename, "r") as f:
            data = f.read().replace("\n", "")
        return js.loads(data)
    except FileNotFoundError:
        return [] 

def unpause():
	global ismenue, issettings
	ismenue = False
	issettings = False

def GTS():
	global issettings
	issettings = True

def GTM():
	global issettings
	issettings = False

def Menu():
	global ismenue, issettings
	ismenue = True
	issettings = False

def stop():
	global ran
	ran = 0

fps = 60
ran = 1

player_infosheets = {
	'sr': {'hitbox': [[9 * 3 + 3, 29 * 3], [9 * 3 + 3, 28 * 3]],
	       "sprite": Spritesheet("animations/Demeanor_sr.png", 2, 1, 18, 30, 54, 90).frames},
	'sl': {'hitbox': [[9 * 3+1, 29 * 3], [9 * 3+1, 28 * 3]],
	       "sprite": Spritesheet("animations/Demeanor_sl.png", 2, 1, 18, 30, 54, 90).frames},
	'wr': {'hitbox': [[9 * 3+3, 29 * 3], [9*3+3, 29 * 3], [9 * 3+3, 29 * 3], [9 * 3+3, 29 * 3]],
	       "sprite": Spritesheet("animations/Demeanor_wr.png", 4, 1, 18, 30, 54, 90).frames},
	'wl': {'hitbox': [[9 * 3+1, 29 * 3], [9*3+1, 29 * 3], [9 * 3+1, 29 * 3], [9 * 3+1, 29 * 3]],
	       "sprite": Spritesheet("animations/Demeanor_wl.png", 4, 1, 18, 30, 54, 90).frames}
}

player = Player(250, 250, player_infosheets['sr'], player_infosheets['sl'], player_infosheets['wr'],
	            player_infosheets['wl'], 1)
background = transform.scale(image.load("animations/sky.jpg"), (500, 500))
cavebackgrounds = [[Surface(((15+1)*50, 2*50)), (7*50, 35*50)], [Surface((8*50, 50)), (11*50, 34*50)]]
purplestonebackgrounds = [[Surface((10*50, 5*50)), (30*50, 30*50)]]
for i in range(len(cavebackgrounds)):
	for j in range(int(cavebackgrounds[i][0].get_width()//500+1 - (cavebackgrounds[i][0].get_width()//500+1) % 1) if cavebackgrounds[i][0].get_width()/500 % 500 > 0 else int(cavebackgrounds[i][0].get_width()/500 - (cavebackgrounds[i][0].get_width()/500) % 1)):
		for g in range(int(cavebackgrounds[i][0].get_height()//500+1 - (cavebackgrounds[i][0].get_height()//500+1) % 1) if cavebackgrounds[i][0].get_height()/500 % 500 > 0 else int(cavebackgrounds[i][0].get_height()/500 - (cavebackgrounds[i][0].get_height()/500) % 1)):
			cavebackgrounds[i][0].blit(transform.scale(image.load("animations/cave.png"), (500, 500)), (j*500,g*5000))

for i in range(len(purplestonebackgrounds)):
	for j in range(int(purplestonebackgrounds[i][0].get_width()//500+1 - (purplestonebackgrounds[i][0].get_width()//500+1) % 1) if purplestonebackgrounds[i][0].get_width()/500 % 500 > 0 else int(purplestonebackgrounds[i][0].get_width()/500 - (purplestonebackgrounds[i][0].get_width()/500) % 1)):
		for g in range(int(purplestonebackgrounds[i][0].get_height()//500+1 - (purplestonebackgrounds[i][0].get_height()//500+1) % 1) if purplestonebackgrounds[i][0].get_height()/500 % 500 > 0 else int(purplestonebackgrounds[i][0].get_height()/500 - (purplestonebackgrounds[i][0].get_height()/500) % 1)):
			print("done")
			purplestonebackgrounds[i][0].blit(transform.scale(image.load("animations/purplestone.png"), (500, 500)), (j*500,g*500))

maintextbox = textbox(62, 500-150, 500-124, 100, fonte, (0,0,0), (255, 255, 255), (150, 150, 150))
sam = Camera(0, 0)
itemsprites = Spritesheet("animations/rubiesc.png", 17, 3, 9, 9, 18, 18, 1, 1).frames

tilemape = tilemap("Sprite-0004.png", 4, 8, 25, 25, 50, 50, 0, 0)
groundsprites = [
				Spritesheet("animations/dirtparts UL.png", 5, 1, 12, 12, 12, 12, 1, 1).frames,
				Spritesheet("animations/dirtparts UR.png", 5, 1, 13, 12, 13, 12, 1, 1).frames,
				Spritesheet("animations/dirtparts DL.png", 5, 1, 12, 13, 12, 13, 1, 1).frames,
				Spritesheet("animations/dirtparts DR.png", 5, 1, 13, 13, 13, 13, 1, 1).frames
				]


mosssprites = [
				Spritesheet("animations/mossparts UL.png", 5, 1, 12, 12, 12, 12, 1, 1).frames,
				Spritesheet("animations/mossparts UR.png", 5, 1, 13, 12, 13, 12, 1, 1).frames,
				Spritesheet("animations/mossparts DL.png", 5, 1, 12, 13, 12, 13, 1, 1).frames,
				Spritesheet("animations/mossparts DR.png", 5, 1, 13, 13, 13, 13, 1, 1).frames
			  ]

file = load("rooms.json")

rooms = tilemape.maptoroom(file)
indexroom = 0

inventarslot = transform.scale(image.load("animations/itemframe.png"), (27, 27))
inventarslotselected = transform.scale(image.load("animations/itemframeselected.png"), (27, 27))
menubutton = transform.scale(image.load("animations/menu button.png"), (27, 27))
ismenue = False
issettings = False
menubuttonbutton = button(27*10+6, 4, menubutton.get_width(), menubutton.get_height(), "", Menu)
menubuttons = [
				button(135, 30, 230, 100, "Continue", unpause),
				button(135, 140, 230, 100, "Save", lambda:print("not implememnted yet")),
				button(135, 250, 230, 100, "Settings", GTS),
				button(135, 360, 230, 100, "Exit", stop),
			  ]
settingbuttons = [
					button(11, 30, 477, 100, "Close", GTM)
				 ]
settingsliders = [
					slider(11, 140, 477, 10, 100, 7)
				 ]
settingstextboxes = [
						textboxME(11, 160, 477, 100)
					]

settingsliders[0].setvalue(30)

inventory = [41, None, None, None, None, None, None, None, None, None]
itemselected = 0
names = [i.replace("⌂", " ") for i in open("item/liberte", 'r').read().replace("/ ", "⌂").split(" ")]
Items = {i: [itemsprites[i], names[i]] for i in range(len(itemsprites))}
camerax = 0
cameray = 0

mixer.music.load("background.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(loops=-1)
q = 0
Clock = time.Clock()
while ran:
	q=+1
	window.fill((255, 255, 255))
	window.blit(background, (0,0))
	if indexroom == 0:
		for i in cavebackgrounds:
			sam.blitwith(i[1][0], i[1][1], i[0])
	if indexroom == 1:
		for i in purplestonebackgrounds:
			sam.blitwith(i[1][0], i[1][1], i[0])
	for i in rooms[indexroom]:
		i.draw()

	for e in event.get():
		if e.type == QUIT:
			ran = 0
		if e.type == MOUSEBUTTONDOWN and  getattr(e, "button", None) == 1:
			if ismenue:
				if not issettings:
					for btn in menubuttons:
						if btn.hovers():
							btn.command()
				else:
					for btn in settingbuttons:
						if btn.hovers():
							btn.command()
			else:
				if menubuttonbutton.hovers():
					menubuttonbutton.command()
		if e.type == MOUSEWHEEL:
			if not ismenue:
				if e.y > 0:
					itemselected -= 1
					if itemselected < 0:
						itemselected = 9
				else:
					itemselected += 1
					if itemselected > 9:
						itemselected = 0
			
		if e.type == KEYDOWN:
			if not ismenue:
				if e.key == K_s:
					player.run = True
				if e.key == K_x:
					player.interacted = True
				if e.key == K_1:
					itemselected = 0
				if e.key == K_2:
					itemselected = 1
				if e.key == K_3:
					itemselected = 2
				if e.key == K_4:
					itemselected = 3
				if e.key == K_5:
					itemselected = 4
				if e.key == K_6:
					itemselected = 5
				if e.key == K_7:
					itemselected = 6
				if e.key == K_8:
					itemselected = 7
				if e.key == K_9:
					itemselected = 8
				if e.key == K_0:
					itemselected = 9
			if e.key == K_ESCAPE:
				ismenue = not ismenue
				issettings = False
		if e.type == KEYUP:
			if not ismenue:
				if e.key == K_s:
					player.run = False
		if settingsliders[0].hovers() and mouse.get_pressed()[0]:
			settingsliders[0].slide()
			mixer.music.set_volume(settingsliders[0].getvalue()/100)
		
	if not ismenue:
		draw.rect(window, (75, 75, 75), Rect(2, 2, 27*10+6, 31), border_radius=3)
		for i in range(10):	
			window.blit(inventarslotselected if itemselected == i else inventarslot, (27*i+4, 4))
			if inventory[i] != None:
				window.blit(Items[inventory[i]][0], (36*i+4+5, 4+6))
		window.blit(menubutton, (27*10+6, 4))
		if mouse.get_pos()[0] < 276 and mouse.get_pos()[1] < 35 and mouse.get_pos()[0] > 4 and mouse.get_pos()[1] > 4:
			if inventory[(mouse.get_pos()[0]-4)//27 if (mouse.get_pos()[0]-4)//27 < 10 else 0] != None:
				texttodisplay = Items[inventory[(mouse.get_pos()[0]-4)//27 if (mouse.get_pos()[0]-4)//27 < 10 else 0]][1]
			else:
				texttodisplay = "Empty Slot"
			text = fonte.render(texttodisplay, False, (255, 255, 255))
			window.blit(text, (4, 30))
		#maintextbox.draw("Ugh, where am i?", "Demeanor")

	if not ismenue:
		player.incrementCounter(0.1)
		player.move(2, rooms[indexroom])
		sam["x"] = player.x-250
		sam["y"] = player.y-250
	player.draw(10, 14)

	if ismenue:
		if not issettings:
			draw.rect(window, (75, 75, 75), Rect(125, 1, 250, 498), border_radius=15)
			draw.rect(window, (50, 50, 50), Rect(125, 1, 250, 498), border_radius=15, width=3)
			for btn in menubuttons:
				btn.draw()
		else:
			draw.rect(window, (75, 75, 75), Rect(1, 1, 498, 498), border_radius=15)
			draw.rect(window, (50, 50, 50), Rect(1, 1, 498, 498), border_radius=15, width=3)
			for btn in settingbuttons:
				btn.draw()
			for sldr in settingsliders:
				sldr.draw()
			for tbx in settingstextboxes:
				tbx.draw(f"Music Value : {settingsliders[0].getvalue()}%")

	display.update()
	Clock.tick(fps)

quit()