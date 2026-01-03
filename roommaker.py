from pygame import *
import json as js

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

class block:
    def __init__(self, x, y, width, height, tile, tilemape):
        self.x = x * width
        self.y = y * height
        self.tile = tile
        self.tilemape = tilemape

    def draw(self):
        window.blit(self.tilemape.frames[self.tile], (self.x - camerax, self.y - cameray))
class ground(block):
    def __init__(self, x, y, width, height, preset, conf):
        global groundsprites
        super().__init__(x, y, width, height, [], [])
        self.preset = preset
        if conf == "ground":
            self.conf = groundsprites
        elif conf == "moss":
            self.conf = mosssprites
    def draw(self):
        surfacea = Surface((25, 25))
        surfacea.blit(self.conf[0][self.preset[0]], (0, 0))
        surfacea.blit(self.conf[1][self.preset[1]], (12, 0))
        surfacea.blit(self.conf[2][self.preset[2]], (0, 12))
        surfacea.blit(self.conf[3][self.preset[3]], (12, 12))
        window.blit(transform.scale(surfacea, (50, 50)), (self.x - camerax, self.y - cameray))

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

class dropdown:
    def __init__(self, x, y, width, height, options, option_height):
        self.rect = Rect(x, y, width, height)
        self.options = options
        self.selected = 0
        self.font = font.Font(None, 30)
        self.color = (200, 200, 200)
        self.option_height = option_height
        self.active = False

    def hovers(self):
        if self.rect.collidepoint(mouse.get_pos()):
            return True
        return False
    
    def command(self):
        self.active = not self.active

    def draw(self):
        draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(self.options[self.selected], True, (0, 0, 0))
        V = self.font.render( "V", True, (0, 0, 0))
        window.blit(text_surface, (self.rect.x + 5, self.rect.y + self.rect.height // 2 - text_surface.get_rect().height // 2))
        window.blit(V, (self.rect.x + self.rect.width - V.get_width() - 10, self.rect.y + self.rect.height // 2 - text_surface.get_rect().height // 2))
        if self.active:
            for i, option in enumerate(self.options):
                option_rect = Rect(self.rect.x, self.rect.y + (i + 1) * self.option_height, self.rect.width, self.option_height)
                draw.rect(window, (150, 150, 150), option_rect)
                option_text_surface = self.font.render(option, True, (0, 0, 0))
                window.blit(option_text_surface, (option_rect.x + 5, option_rect.y + 5))
                if option_rect.collidepoint(mouse.get_pos()):
                    if mouse.get_pressed()[0]:
                        self.selected = i
                        self.active = False

class textbox:
    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)
        self.font = font.Font(None, 30)
        self.color = (200, 200, 200)
        self.active = False

    def draw(self, text):
        draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(text, True, (0, 0, 0))
        window.blit(text_surface, (self.rect.x + self.rect.width // 2 - text_surface.get_rect().width // 2, self.rect.y + self.rect.height // 2 - text_surface.get_rect().height // 2))

class checkbox:
    def __init__(self, x, y, width, height, text):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.font = font.Font(None, 30)
        self.checked = True

    def hovers(self):
        if self.rect.collidepoint(mouse.get_pos()):
            return True
        return False

    def draw(self):
        draw.rect(window, (200, 200, 200), self.rect)
        if self.checked:
            draw.line(window, (0, 0, 0), (self.rect.x + 5, self.rect.y + 5), (self.rect.x + self.rect.width - 5, self.rect.y + self.rect.height - 5), 2)
            draw.line(window, (0, 0, 0), (self.rect.x + self.rect.width - 5, self.rect.y + 5), (self.rect.x + 5, self.rect.y + self.rect.height - 5), 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        window.blit(text_surface, (self.rect.x + self.rect.width + 10, self.rect.y + self.rect.height // 2 - text_surface.get_rect().height // 2))

    def command(self):
        self.checked = not self.checked

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

def back():
    global roomindex
    if roomindex > 0:
        roomindex -= 1

def forward():
    global roomindex
    if roomindex < len(map_data) - 1:
        roomindex += 1

def add_room():
    global map_data, roomindex
    map_data.append([])
    roomindex = len(map_data) - 1

def remove_room():
    global map_data, roomindex
    if len(map_data) > 1:
        map_data.pop(roomindex)
        if roomindex >= len(map_data):
            roomindex = len(map_data) - 1

def spriteforward():
    global spritee
    if spritee < len(tilemape.frames) - 1:
        spritee += 1

def spriteback():
    global spritee
    if spritee > 0:
        spritee -= 1

def roomtoforward():
    global roomto
    if roomto < len(map_data) - 1:
        roomto += 1

def roomtoback():
    global roomto
    if roomto > 0:
        roomto -= 1

def increaseselect():
    global selectedpresetindex
    selectedpresetindex = (selectedpresetindex + 1) % len(groundsprites)

def selecta():
    global preset, selectedpresetindex
    preset[selectedpresetindex] = 0
    increaseselect()
def selectb():
    global preset, selectedpresetindex
    preset[selectedpresetindex] = 1
    increaseselect()
def selectc():
    global preset, selectedpresetindex
    preset[selectedpresetindex] = 2
    increaseselect()
def selectd():
    global preset, selectedpresetindex
    preset[selectedpresetindex] = 3
    increaseselect()
def selecte():
    global preset, selectedpresetindex
    preset[selectedpresetindex] = 4
    increaseselect()

# Initialize pygame
init()

# Set up display
ww, wh = 500, 600
window = display.set_mode((ww, wh))
display.set_caption("Room Maker")
tilemape = Spritesheet("Sprite-0004.png", 4, 8, 25, 25, 50, 50, 0, 0)
map_data = load("rooms.json")
roomindex = 0
buttons = [
            button(10, 10, 60, 79, "save", lambda: save("rooms.json", map_data)),
            button(80, 10, 50, 35, "<", back),
            button(210, 10, 50, 35, ">", forward),
            button(80, 54, 85, 35, "-", remove_room),
            button(175, 54, 85, 35, "+", add_room),
            dropdown(270, 10, 100, 35, ["block", "door", "ground"], 30),
            checkbox(380, 10, 20, 35, ""),
            button(480, 10, 15, 35, ">", spriteforward),
            button(405, 10, 15, 35, "<", spriteback)
          ]

textbox1 = textbox(140, 10, 60, 35)

doorbuttons = [
                button(365, 54, 15, 35, ">", roomtoforward),
                button(270, 54, 15, 35, "<", roomtoback),
              ]
groundbuttons = [
                    dropdown(270, 54, 100, 35, ["ground", "moss"], 30),
                    button(380, 63, 26, 26, "a", lambda: selecta()),
                    button(410, 63, 26, 26, "b", lambda: selectb()),
                    button(440, 63, 26, 26, "c", lambda: selectc()),
                    button(470, 63, 26, 26, "d", lambda: selectd()),
                    button(480, 48, 12, 12, "e", lambda: selecte())
                ]
preset = [0,0,0,0]
selectedpresetindex = 0
conf = ""
doorbuttonstextbox = textbox(295, 54, 60, 35)

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
blocksurfaceground = Surface((25, 25))
clock = time.Clock()

camerax = 0
cameray = 0
speed = 5

hitbox = True
spritee = 0
blocktype = "block"
roomto = 0

# Main loop
running = True
while running:
    blocktype = buttons[5].options[buttons[5].selected]
    hitbox = buttons[6].checked
    window.fill((30, 30, 30))  # Fill the window with a dark gray color
    blocksurfaceground.fill((0, 0, 0, 0))
    if groundbuttons[0].selected == 0:
        blocksurfaceground.blit(groundsprites[0][preset[0]], (0, 0))
        blocksurfaceground.blit(groundsprites[1][preset[1]], (12, 0))
        blocksurfaceground.blit(groundsprites[2][preset[2]], (0, 12))
        blocksurfaceground.blit(groundsprites[3][preset[3]], (12, 12))
    elif groundbuttons[0].selected == 1:
        blocksurfaceground.blit(mosssprites[0][preset[0]], (0, 0))
        blocksurfaceground.blit(mosssprites[1][preset[1]], (12, 0))
        blocksurfaceground.blit(mosssprites[2][preset[2]], (0, 12))
        blocksurfaceground.blit(mosssprites[3][preset[3]], (12, 12))
    for i in range(ww-100 // 50):
        draw.line(window, (255, 255, 255), (i * 50 - camerax % 50, 0), (i * 50 - camerax % 50, wh))
    draw.line(window, (255, 255, 255), (ww-1, 0), (ww-1, wh))
    for i in range(wh-200 // 50):
        draw.line(window, (255, 255, 255), (0, i * 50 - cameray % 50), (ww, i * 50 - cameray % 50))
    draw.line(window, (255, 255, 255), (0, wh-1), (ww, wh-1))

    draw.line(window, (255, 255, 255), (250 - camerax, 0 - cameray +100), (250 - camerax, wh - cameray), 5)
    draw.line(window, (255, 255, 255), (0 - camerax, 250 - cameray +100), (ww - camerax, 250 - cameray +100), 5) 

    for j in [block(i[0][0], i[0][1] + 2, 50, 50, i[1][0], tilemape) if i[1][2] != 2 else ground(i[0][0], i[0][1] +2, 50, 50, i[2], i[1][0]) for i in map_data[roomindex]]:
        j.draw()

    draw.rect(window, (255, 255, 255), (0, 0, ww, 99))  # Draw the top bar
    
    if blocktype == "door":
        doorbuttonstextbox.draw(str(roomto+1))

    if blocktype == "door":
        for b in doorbuttons:
            b.draw()
    if blocktype == "ground":
        for b in groundbuttons:
            b.draw()
        if groundbuttons[0].selected == 0:
            window.blit(transform.scale(groundsprites[selectedpresetindex][0], (24 if selectedpresetindex %2 == 0 else 26, 24 if selectedpresetindex//2<1 else 26)), (groundbuttons[1].rect.x, groundbuttons[1].rect.y))
            window.blit(transform.scale(groundsprites[selectedpresetindex][1], (24 if selectedpresetindex %2 == 0 else 26, 24 if selectedpresetindex//2<1 else 26)), (groundbuttons[2].rect.x, groundbuttons[2].rect.y))
            window.blit(transform.scale(groundsprites[selectedpresetindex][2], (24 if selectedpresetindex %2 == 0 else 26, 24 if selectedpresetindex//2<1 else 26)), (groundbuttons[3].rect.x, groundbuttons[3].rect.y))
            window.blit(transform.scale(groundsprites[selectedpresetindex][3], (24 if selectedpresetindex %2 == 0 else 26, 24 if selectedpresetindex//2<1 else 26)), (groundbuttons[4].rect.x, groundbuttons[4].rect.y))
            window.blit(transform.scale(groundsprites[selectedpresetindex][4], (12 if selectedpresetindex %2 == 0 else 13, 12 if selectedpresetindex//2<1 else 13)), (groundbuttons[5].rect.x, groundbuttons[5].rect.y))
        elif groundbuttons[0].selected == 1:
            window.blit(transform.scale(mosssprites[selectedpresetindex][0], (24 if selectedpresetindex %2 == 0 else 26, 24 if selectedpresetindex//2<1 else 26)), (groundbuttons[1].rect.x, groundbuttons[1].rect.y))
            window.blit(transform.scale(mosssprites[selectedpresetindex][1], (24 if selectedpresetindex %2 == 0 else 26, 24 if selectedpresetindex//2<1 else 26)), (groundbuttons[2].rect.x, groundbuttons[2].rect.y))
            window.blit(transform.scale(mosssprites[selectedpresetindex][2], (24 if selectedpresetindex %2 == 0 else 26, 24 if selectedpresetindex//2<1 else 26)), (groundbuttons[3].rect.x, groundbuttons[3].rect.y))
            window.blit(transform.scale(mosssprites[selectedpresetindex][3], (24 if selectedpresetindex %2 == 0 else 26, 24 if selectedpresetindex//2<1 else 26)), (groundbuttons[4].rect.x, groundbuttons[4].rect.y))
            window.blit(transform.scale(mosssprites[selectedpresetindex][4], (12 if selectedpresetindex %2 == 0 else 13, 12 if selectedpresetindex//2<1 else 13)), (groundbuttons[5].rect.x, groundbuttons[5].rect.y))            
    conf = groundbuttons[0].options[groundbuttons[0].selected]

    for b in buttons:
        b.draw()
    textbox1.draw(str(roomindex+1))
    if blocktype != "ground":
        window.blit(tilemape.frames[spritee], (425, 10))  # Draw the selected sprite
    else:
        window.blit(transform.scale(blocksurfaceground, (50, 50)), (425, 10))

    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_f:
                mode = not mode
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                if mouse.get_pos()[1] > 100:
                    x, y = mouse.get_pos()
                    x = (x + camerax) // 50
                    y = (y + cameray - 100) // 50
                    for i in map_data[roomindex]:
                        if i[0][0] == x and i[0][1] == y:
                            map_data[roomindex].remove(i)
                            break
                    else:
                        match blocktype:
                            case "block":
                                map_data[roomindex].append([[x, y], [spritee, hitbox, 0]])
                            case "door":
                                map_data[roomindex].append([[x, y], [spritee, hitbox, 1, roomto]])
                            case "ground":
                                map_data[roomindex].append([[x, y], [conf, hitbox, 2], preset.copy()])
                else:
                    for b in buttons:
                        if b.hovers():
                                b.command()
                    if blocktype == "door":
                        for b in doorbuttons:
                            if b.hovers():
                                b.command()
                    if blocktype == "ground":
                        for b in groundbuttons:
                            if b.hovers():
                                b.command()             

    keys = key.get_pressed()
    if keys[K_LEFT]:
        camerax -= speed
    if keys[K_RIGHT]:
        camerax += speed
    if keys[K_UP]:
        cameray -= speed
    if keys[K_DOWN]:
        cameray += speed

    clock.tick(60)
    display.update()

quit()
