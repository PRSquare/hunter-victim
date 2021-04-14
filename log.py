import numpy as np
import pyqtgraph.opengl as gl
import random

# 3D object class
class THDobject:
    def __init__(self, filename, color):
        self.color = color
        self.cords = []
        self.pos = [0, 0, 0]
        self.objParser(filename) # Parsing .obj file
        self.mesh = gl.GLMeshItem(vertexes=np.array(self.cords), drawEdges=True, color=self.color) # Creating mesh
    
    # Parsin .obj file
    def objParser(self, filename):
        inFile = open(filename, 'r')
        vertexes = []
        uvCords = []
        normals = []

        for line in inFile:
            # Vertexes
            if "v " in line:
                vLine = line.split(" ")
                vertexes.append([float(vLine[1]), float(vLine[2]), float(vLine[3])])
            # UV cords
            if "vt " in line:
                vtLine = line.split(" ")
                uvCords.append([float(vtLine[1]), float(vtLine[2])])
            # Normale vertexes
            if "vn " in line:
                vnLine = line.split(" ")
                normals.append([float(vnLine[1]), float(vnLine[2]), float(vnLine[3])])
            # Indexes
            if "f " in line:
                inLine = line.split(" ")
                a = inLine[1].split("/")
                b = inLine[2].split("/")
                c = inLine[3].split("/")
                fv = vertexes[int(a[0])-1]
                sv = vertexes[int(b[0])-1]
                tv = vertexes[int(c[0])-1]
                self.cords.append([fv, sv, tv])
        
    def update(self):
        newCords = []
        for b in self.cords:
            nc = []
            for a in b:
                nc.append( [a[0] + self.pos[0], a[1] + self.pos[1], a[2] + self.pos[2] ])
            newCords.append(nc)
        self.mesh.setMeshData(vertexes=np.array(newCords), drawEdges=True, color=self.color)
    
    def move(self, pos):
        self.pos = pos
        self.update()
                
    def rotate(self, a):
        rotMatX = np.mat([
            [np.cos(a), -np.sin(a), 0],
            [np.sin(a), np.cos(a), 0],
            [0, 0, 1]
            ])
        newCords = []
        for a in self.cords:
            a = a*rotMatX
            newCords.append( np.asarray(a) )
        
        self.cords = newCords
        self.update()
        
    def scale(self, sv):
        newCords = []
        for a in self.cords:
            nc = []
            for b in a:
                b *= sv
                nc.append(b)
            newCords.append(nc)
        
        self.cords = newCords
        self.update()
 

# Getting rand value
mrand = lambda maxval: random.random()*maxval*2 - maxval
# Changing value to simulate mutation
genMutation = lambda gen, rng: gen + random.random()*rng*2 - rng
# Length between two points
pathL = lambda pos1, pos2: np.sqrt((pos2[0]-pos1[0])*(pos2[0]-pos1[0]) + (pos2[1]-pos1[1])*(pos2[1]-pos1[1]))

def col (pos1, pos2, rad = 5): # Colision check
    return abs(pos1[0] - pos2[0]) <= rad and abs(pos1[1] - pos2[1]) <= rad

# Default size of landscape
landSize = 100

# Base class for animals (fox/bunny)
class alive(THDobject):
    def __init__(self, name, color, mHunger, prodTime, srchRadius, spd, strvLvl, prdLvl):
        super().__init__(name, color)
        self.natureColor = color
        self.maxHunger = mHunger
        self.hunger = self.maxHunger/2
        self.produceTime = prodTime
        self.pTimer = 0
        self.momy = False
        self.speed = spd
        self.search_radius = srchRadius
        self.starvationStart = strvLvl
        self.prodStart = prdLvl
        self.cosA = 0
        self.sinA = 0
        self.moveDir = [0, 0]
        self.changeDirection(mrand(landSize), mrand(landSize))
        self.steps = 0
        self.bussy = False
        self.isAlive = True
        self.maxSteps=50
        self.curFPL = self.search_radius
        
        self.selectedFood = bush()
        self.selectedPartner = 0
        self.preg = False
        self.inProcess = False
    
    def death(self):
        self.isAlive = False
    
    def eat(self):
        self.hunger = 0
        self.color = self.natureColor
        self.bussy = False
        self.curFPL = self.search_radius
        self.steps = self.maxSteps
    
    def produce(self):
        self.pTimer = 0
        self.color = self.natureColor
        self.momy = False
        self.bussy = False
        self.inProcess = False
        self.steps = self.maxSteps
     
    def changeDirection(self, x = mrand(landSize), y = mrand(landSize)):
        self.moveDir = [x, y]
        pathLength = pathL(self.pos, self.moveDir)
        a = x - self.pos[0]
        b = y - self.pos[1]
        if pathLength != 0:
            self.mvVector = [a/pathLength, b/pathLength]
        
    def log_update(self): 
        self.walking()
        self.hunger += 1
        self.pTimer += 1
        
        if(self.hunger > self.maxHunger):
            self.isAlive = False
            
        if self.inProcess == False and self.bussy == False and self.steps > self.maxSteps:
            self.steps = 0
            self.changeDirection(mrand(landSize*2), mrand(landSize*2))
        
    def walking(self):
        mx = self.pos[0]
        my = self.pos[1]
        
        if col(self.pos, self.moveDir, 0.4) == False:
            if self.pos[0] < landSize and self.pos[0] > -landSize :
                mx = self.pos[0] + self.speed *self.mvVector[0]
            else:
                if self.pos[0] >= landSize:
                    mx = self.pos[0]-1
                else:
                    mx = self.pos[0]+1
                self.changeDirection(mrand(landSize*2), mrand(landSize*2))
                
            if self.pos[1] < landSize and self.pos[1] > -landSize:
                my = self.pos[1] + self.speed *self.mvVector[1]
            else:
                if self.pos[1] >= landSize:
                    my = self.pos[1]-1
                else:
                    my = self.pos[1]+1
                self.changeDirection(mrand(landSize*2), mrand(landSize*2))
                   
        self.move([mx, my, 1])
        
        self.steps += 1
        

class landsacpe(THDobject):
    def __init__(self):
        super().__init__("landscape.obj", (0, 1, 0.1, 1))
        
class bush(THDobject):
    def __init__(self):
        super().__init__("bush.obj", (0, 0.7, 0.5, 1))
        self.exist = True
        
class bunny(alive):
    def __init__(self, mHunger = 200, prodTime = 100, srchRadius = 30, spd = 1.5, strvLvl=30, prdLvl = 40):
        super().__init__("bunny.obj", (0.2, 0.2, 0.2, 1), mHunger, prodTime, srchRadius, spd, strvLvl, prdLvl)
    
    def hunt(self, food):
        if self.selectedFood.exist == False:
            self.curFPL = self.search_radius
            self.bussy = False
        curPL = pathL(self.pos, food.pos)
        if curPL < 0.5:
            self.eat()
            return True
        if curPL < self.search_radius:
            if curPL < self.curFPL:
                self.selectedFood = food
                self.curFPL = curPL
                self.changeDirection(food.pos[0], food.pos[1])
                self.bussy = True
        return False

class fox(alive):
    def __init__(self, mHunger = 100, prodTime = 150, srchRadius = 40, spd = 2, strvLvl=30, prdLvl = 50):
        super().__init__("fox.obj", (1, 0.4, 0, 1), mHunger, prodTime, srchRadius, spd, strvLvl, prdLvl)
        
    def hunt(self, bunny):
        if bunny.isAlive == False:
            self.bussy = False
            return
        curPL = pathL(self.pos, bunny.pos)
        if curPL > self.curFPL:
            return
        self.changeDirection(bunny.pos[0], bunny.pos[1])
        self.bussy = True
        if col(bunny.pos, self.pos):
            bunny.death()
            self.eat()

# Class that consist all information about current world 
class world:
    def __init__(self, window, worldSize = 1, bPopulation=10, fPopulation=3, foodCount=10, 
                 foodProdSpeed=10, bunnyDefHunger = 200, foxDefHunger=100):
        self.foodSpeed = foodProdSpeed
        self.nowFoodState = 0
        self.gr = landsacpe()
        self.gr.rotate(0)
        self.gr.scale(worldSize)
        global landSize
        landSize = 100*worldSize
        self.window = window
        window.addItem(self.gr.mesh)
        random.seed()
        
        self.bPop = []
        self.fPop = []
        self.bushes = []
        for a in range(bPopulation):
            pt = genMutation(100, 5) 
            sp = genMutation(1.2, 0.1) 
            newBunny = bunny(mHunger=bunnyDefHunger, prodTime=pt, spd = sp)
            newBunny.move((mrand(landSize), mrand(landSize), 1))
            self.bPop.append(newBunny)
            
        for a in range(fPopulation):
            pt = genMutation(100, 5) 
            sp = genMutation(1.8, 0.1)
            newFox = fox(mHunger=foxDefHunger, prodTime=pt, spd = sp) 
            newFox.move((mrand(landSize), mrand(landSize), 1))
            self.fPop.append(newFox)
            
        for a in range(foodCount):
            newBush = bush()
            newBush.move((mrand(landSize), mrand(landSize), 1))
            self.bushes.append(newBush)
            
        for a in self.bPop:
            window.addItem(a.mesh)
        for a in self.fPop:
            window.addItem(a.mesh)
        for a in self.bushes:
            window.addItem(a.mesh)
    
    def update(self):
        # Creating new bushes
        if self.nowFoodState > self.foodSpeed:
            self.nowFoodState = 0
            newBush = bush()
            newBush.move((mrand(landSize), mrand(landSize), 1))
            self.window.addItem(newBush.mesh)
            self.bushes.append(newBush)
        
        self.nowFoodState += 1

        # Values, that will be updated
        nbGen = self.bPop
        nfGen = self.fPop
        nbushes = self.bushes
        
        # Deleting bush if it is eaten
        for a in self.bushes:
            if a.exist == False:
                nbushes.remove(a)
                self.window.removeItem(a.mesh)
        
        # Deleting bunny if it is dead
        for a in self.bPop:
            a.log_update()
            if a.isAlive==False:
                self.window.removeItem(a.mesh)
                nbGen.remove(a)
                
        # ============================================== BUNNIES LOGIC ==============================================
        for a in self.bPop:
            # Skip, if it is dead
            if a.isAlive == False:
                continue
            # Hunger check
            if a.inProcess == False and a.hunger > a.maxHunger*(a.starvationStart/100):
                for b in self.bushes:
                    if(a.hunt(b)):
                        b.exist = False
                        break
            # Selecting a partner
            if a.inProcess == False and a.bussy == False and a.pTimer > a.produceTime and a.hunger < a.maxHunger*(a.prodStart/100):
                for b in nbGen:
                    if a == b:
                        continue
                    if col(b.pos, a.pos, a.search_radius*2) and b.bussy == False and b.isAlive == True and b.inProcess == False and b.hunger < b.maxHunger*(b.prodStart/100):
                        a.inProcess = True
                        b.inProcess = True
                        b.momy = True
                        a.changeDirection(b.pos[0], b.pos[1])
                        b.changeDirection(a.pos[0], a.pos[1])
                        r = random.random()
                        g = random.random()
                        bb = random.random()
                        a.color=(r, g, bb, 1)
                        b.color=(r, g, bb, 1)
                        a.selectedPartner = b
                        b.selectedPartner = a
                        break
            # Reproduction
            if a.inProcess == True:
                # Death of partner
                if a.selectedPartner.isAlive == False:
                    a.inProcess = False
                    a.color = a.natureColor
                    print("Partner is dead!")
                # Borning
                if a.momy == True:
                    if col(a.pos, a.selectedPartner.pos):
                        a.produce()
                        a.selectedPartner.produce()
                        mh = genMutation(a.maxHunger, 5)
                        pt = genMutation(a.produceTime, 5) 
                        sp = genMutation(a.speed, 0.1) 
                        newBunny = bunny(mHunger=mh, prodTime=pt, spd = sp)
                        newBunny.move(a.pos)
                        nbGen.append(newBunny)
                        self.window.addItem(newBunny.mesh)
        # ============================================================================================

        # ============================================== FOXES LOGIC ==============================================
        for a in self.fPop:
            a.log_update()
            # Delete, if it is dead
            if(a.isAlive==False):
                self.window.removeItem(a.mesh)
                nfGen.remove(a)

        for a in self.fPop:
            # Hunger check
            if a.inProcess == False and a.hunger > a.maxHunger*(a.starvationStart/100):
                for b in nbGen:
                    if col(a.pos, b.pos, a.search_radius):
                        a.hunt(b)
            # Selecting a partner
            if a.inProcess == False and a.bussy == False and a.pTimer > a.produceTime and a.hunger < a.maxHunger*(a.prodStart/100):
                for b in nfGen:
                    if a == b:
                        continue
                    if col(b.pos, a.pos, a.search_radius*2) and b.bussy == False and b.isAlive == True and b.inProcess == False and b.hunger < b.maxHunger*(b.prodStart/100):
                        a.inProcess = True
                        b.inProcess = True
                        b.momy = True
                        a.changeDirection(b.pos[0], b.pos[1])
                        b.changeDirection(a.pos[0], a.pos[1])
                        r = random.random()
                        g = random.random()
                        bb = random.random()
                        a.color=(r, g, bb, 1)
                        b.color=(r, g, bb, 1)
                        a.selectedPartner = b
                        b.selectedPartner = a
                        break
            # Reproduction
            if a.inProcess == True:
                # Death of partner
                if a.selectedPartner.isAlive == False:
                    a.inProcess = False
                    a.color = a.natureColor
                    print("Partner is dead!")
                # Borning
                if a.momy == True:
                    if col(a.pos, a.selectedPartner.pos):
                        a.produce()
                        a.selectedPartner.produce()
                        mh = genMutation(a.maxHunger, 5)
                        pt = genMutation(a.produceTime, 5) 
                        sp = genMutation(a.speed, 0.1) 
                        newFox = fox(mHunger=mh, prodTime=pt, spd = sp)
                        newFox.move(a.pos)
                        nfGen.append(newFox)
                        self.window.addItem(newFox.mesh)
        # ============================================================================================

        # Taking information about generation after update
        self.bPop = nbGen
        self.fPop = nfGen
        self.bushes = nbushes
        
    def delete(self):
        self.window.removeItem(self.gr.mesh)
        for a in self.bPop:
            self.window.removeItem(a.mesh)
        for a in self.fPop:
            self.window.removeItem(a.mesh)
        for a in self.bushes:
            self.window.removeItem(a.mesh)
        
        
        
        
        
