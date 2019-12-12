from tkinter import *
import time, random, numpy, math

root = Tk()
color = ("red", "blue", "yellow", "green")
foodList = list()
eList=list()

# code
def distance(x1, x2, y1, y2):
    xer = (x2 - x1) ** 2
    xeq = (y2 - y1) ** 2
    d = math.sqrt(xer + xeq)
    return d


class Food:
    def __init__(self, canvas, tc):
        self.canvas = canvas
        self.mass = 7
        self.x = random.randint(0, 750)
        self.y = random.randint(0, 750)
        self.radius = 7
        self.tc = tc
        self.id = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius,
                                     self.y + self.radius, fill=random.choice(color), tag='food' + str(tc))

    def getCoords(self):
        return canvas.coords(self.id)


tc = 0


def spawn_cells(numOfCells):
    for i in range(numOfCells):
        global f
        global tc
        tc += 1
        f = Food(canvas, tc)
        foodList.append(f)


class Hero:
    def __init__(self, canvas):
        self.x = 250
        self.y = 450
        self.canvas = canvas
        self.endgame = False
        self.radius = 15
        self.speed = 10
        self.direction = -90

        self.hero = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius,
                                       self.y + self.radius, fill=random.choice(color),tag='r')

    def coords(self):
        return self.canvas.coords(self.hero)
    def get_bigger(self, size):
        self.canvas.coords(self.hero,self.coords()[0],self.coords()[1],self.coords()[2]+size,self.coords()[3]+size)

    def mouseCoords(self):
        rawMouseX, rawMouseY = root.winfo_pointerx(), root.winfo_pointery()
        self.mousecoords = rawMouseX - root.winfo_rootx(), rawMouseY - root.winfo_rooty()
        return self.mousecoords

    def moveTowardMouse(self):  # Problem function?
        ## Use center of the of the oval/player as selfx, selfy
        selfx, selfy = (self.coords()[0] + self.coords()[2]) / 2, (self.coords()[1] + self.coords()[3]) / 2
        mousex, mousey = self.mousecoords
        movex = (mousex - selfx)
        movey = (mousey - selfy)
        theta = math.atan2(movey, movex)  ## angle between player and mouse position, relative to positive x

        ## Player speed in terms of x and y coordinates

        x = self.speed * math.cos(theta)
        y = self.speed * math.sin(theta)
        self.canvas.move(self.hero, x, y)


    def collisionDetection(self):
        for c in range(len(eList)):
            try:
                ex = eList[c].coords()[0]
                ey = eList[c].coords()[1]
                xxx = self.coords()[0] + self.radius
                yyy = self.coords()[1] + self.radius
                xx = ex + 15
                yy = ey + 15

                if distance(xx, xxx, yy, yyy) <= self.radius:
                    self.speed*=.9999999999999
                    player.get_bigger(15)
                    print("m")
                    canvas.delete('e' + str(eList[c].ti))
                    del eList[c]
                    canvas.update()
                    root.update()
            except:
                pass
        for f in range(len(foodList)):
            try:
                foodx = foodList[f].getCoords()[0]
                foody = foodList[f].getCoords()[1]
                xxx = self.coords()[0] + self.radius
                yyy = self.coords()[1] + self.radius
                xx = foodx + 7
                yy = foody + 7

                if distance(xx, xxx, yy, yyy) <= self.radius:
                    self.speed*=.9999999999999
                    player.get_bigger(1)
                    print("com")
                    canvas.delete('food' + str(foodList[f].tc))
                    del foodList[f]
                    canvas.update()
                    root.update()
            except:
                pass


class Ai:
    def __init__(self, canvas,ti):
        self.x = random.randint(250, 350)
        self.y = random.randint(450, 600)
        self.canvas = canvas
        self.endgame = False
        self.radius = 15
        self.speed = 10
        self.ti=ti
        self.direction = random.randint(-180,180)
        self.ai = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius,self.y + self.radius, fill=random.choice(color),tag='e' + str(ti))
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
    def coords(self):
        return self.canvas.coords(self.ai)
    def rad(self):
        return self.radius
    def get_bigger(self, size):
        self.canvas.coords(self.ai,self.coords()[0],self.coords()[1],self.coords()[2]+size,self.coords()[3]+size)

    def moveTowardRandom(self):
        selfx, selfy = (self.coords()[0] + self.coords()[2]) / 2, (self.coords()[1] + self.coords()[3]) / 2

        theta = math.atan2(selfy, selfx)  ## angle between player and mouse position, relative to positive x

        ## Player speed in terms of x and y coordinates

        sx = self.speed * math.cos(self.direction)
        sy = self.speed * math.sin(self.direction)
        self.canvas.move(self.ai, sx, sy)
        root.update()
        canvas.update()
    def collisionDetection(self):
        for f in range(len(foodList)):
            try:
                foodx = foodList[f].getCoords()[0]
                foody = foodList[f].getCoords()[1]
                xxx = self.coords()[0] + self.radius
                yyy = self.coords()[1] + self.radius
                xx = foodx + 7
                yy = foody + 7

                if distance(xx, xxx, yy, yyy) <= self.radius:
                    self.speed*=.999
                    self.get_bigger(1)
                    print("com")
                    canvas.delete('food' + str(foodList[f].tc))
                    del foodList[f]
                    canvas.update()
                    root.update()
            except:
                pass
ti = 0

def spawn_enimy(numOfenimy):
    for i in range(numOfenimy):
        global c
        global ti
        ti += 1
        c = Ai(canvas, ti)
        eList.append(c)

# vew
canvas = Canvas(root, width=750, height=750)
center = (canvas.winfo_reqwidth() / 2), (canvas.winfo_reqheight() / 2)
canvas.pack()
def create_grid(event=None):
    w = canvas.winfo_width() # Get current width of canvas
    h = canvas.winfo_height() # Get current height of canvas
    canvas.delete('grid_line') # Will only remove the grid_line

    # Creates all vertical lines at intevals of 100
    for i in range(0, w, 100):
        canvas.create_line([(i, 0), (i, h)], tag='grid_line')

    # Creates all horizontal lines at intevals of 100
    for i in range(0, h, 100):
        canvas.create_line([(0, i), (w, i)], tag='grid_line')
canvas.bind('<Configure>', create_grid)

player = Hero(canvas)


player.mouseCoords()
spawn_enimy(5)
spawn_cells(100)

while player.endgame == False:
    try:
        player.moveTowardMouse()
        player.mouseCoords()
        player.collisionDetection()
        root.update_idletasks()
        root.update()
        time.sleep(.005)
    except:  # KeyboardInterrupt:
        print('CRL-C recieved, quitting')
        root.quit()
        break
root.mainloop()