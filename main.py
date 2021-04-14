import log
import sys
import pyqtgraph.opengl as gl
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg

# Main window class
class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
    	# Window inicialisation
        super(Ui_MainWindow, self).__init__()
        self.resize(1000, 800)

        # Is world already created
        self.worldCreated = False
        # Stop the world after all foxes/bunnies are dead
        self.stopWorld = False
        # If True, the world will be paused
        self.updateWorld = False


        self.graph = pg.PlotWidget(self) #graphic of population
        self.lbl = []
        # Text inicialisation
        self.addLineNames()
        
        # CheckBox to stop world after all foxes/bunnies are dead
        self.cbStopWorld = QtWidgets.QCheckBox("Остановить мир после смерти всех Лис/Зайцев", self)
        self.cbStopWorld.move(600, 470)
        self.cbStopWorld.stateChanged.connect(self.changeStopWorld)
        
        # 3D widget
        self.widget = gl.GLViewWidget(self)
        
        # 3D widget inicialisation
        self.widget.setBackgroundColor('#adf')
        self.widget.setGeometry(0, 0, 1000, 450)  
        self.widget.opts['distance'] = 200
        
        # Count of bunnies abd foxes
        self.bcords = []
        self.fcords = []
        
        self.bCount = 0
        self.fCount = 0
        self.bcords.append(self.bCount)
        self.fcords.append(self.fCount)
        
        
        # Default range of graphic
        self.graph.setYRange(0, 100)
        self.graph.setGeometry(10, 490, 300, 300) 

        self.button_new = QtWidgets.QPushButton('New', self)		# Button to create new world
        self.button_pause = QtWidgets.QPushButton('Pause', self)	# Button to pause the world
        self.button_start = QtWidgets.QPushButton('Start', self)	# Button to start the world
        
        self.inLines = []
        for i in range(7):
            self.inLines.append(QtWidgets.QLineEdit(self)) 
            self.inLines[i].move(800, 500 + i*40)
        
        # Inicialisation of buttons
        self.button_new.clicked.connect(self.createWorld)
        self.button_pause.clicked.connect(self.pause)
        self.button_start.clicked.connect(self.start)
        
        # Setting positions of buttons
        self.button_new.move(500, 500)
        self.button_pause.move(500, 550)
        self.button_start.move(500, 600)
     

    # Function, that changes world state
    def changeStopWorld(self):
        if self.stopWorld == True:
            self.stopWorld = False
        else:
            self.stopWorld = True
    
    # Inicialisation of line names  
    def addLineNames(self):
        self.lbl.append(QtWidgets.QLabel("Размер Мира [1]", self))
        self.lbl[0].move(650, 500)
        self.lbl.append(QtWidgets.QLabel("Популяция Зайцев [20]", self))
        self.lbl[1].move(650, 540)
        self.lbl.append(QtWidgets.QLabel("Популяция Лис [4]", self))
        self.lbl[2].move(650, 580)
        self.lbl.append(QtWidgets.QLabel("Кол-во Еды [20]", self))
        self.lbl[3].move(650, 620)
        self.lbl.append(QtWidgets.QLabel("Темп Роста Еды [10]", self))
        self.lbl[4].move(650, 660)
        self.lbl.append(QtWidgets.QLabel("Запас Еды Зайцев [200]", self))
        self.lbl[5].move(650, 700)
        self.lbl.append(QtWidgets.QLabel("Запас Еды Лис [100]", self))
        self.lbl[6].move(650, 740)
        

    # Creating new world
    def createWorld(self):
        # Getting inic values
        inputs = []
        for i in range(7):
            inputs.append( self.inLines[i].text() )
            inputs[i] =  abs(int(inputs[i])) if inputs[i].isdigit() and inputs[i] != '0' else 1
        
        # Deleting old world 
        if(self.worldCreated == True):
            self.myWorld.delete()
        
        # Inicialisation of a new world 
        self.myWorld = log.world(self.widget, inputs[0], bPopulation=inputs[1], fPopulation=inputs[2], 
                                 foodCount=inputs[3], foodProdSpeed=inputs[4], bunnyDefHunger=inputs[5], 
                                 foxDefHunger=inputs[6])
        self.worldCreated = True
        
        # Clearing graphics
        self.bcords.clear()
        self.fcords.clear()
        
        # New values for graphic
        self.bCount = len(self.myWorld.bPop)
        self.fCount = len(self.myWorld.fPop)
        self.bcords.append(self.bCount)
        self.fcords.append(self.fCount)
        
        self.updateWorld = True
        
    def pause(self):
        self.updateWorld = False
    def start(self):
        self.updateWorld = True
     
    # Update func
    def update(self):
    	# Exitin if world is on pause
        if self.updateWorld == False:
            return
        
        # Updating count of bunnies/foxes
        bLen= len(self.myWorld.bPop)
        fLen= len(self.myWorld.fPop)
        
        # Exiting, if all foxes/bunnies are dead and stop world after it optinon is active
        if self.stopWorld == True:
            if bLen == 0 or fLen == 0:
                return
        
        # Updating 
        self.bCount = len(self.myWorld.bPop)
        self.fCount = len(self.myWorld.fPop)
        self.myWorld.update()					# Updating the world
        self.bcords.append(self.bCount)			# Updating bunnies graphic
        self.fcords.append(self.fCount)			# Updating foxes graphic
        self.graph.setTitle("Model")
        self.graph.plot(self.bcords, clear=True, pen='b')
        self.graph.plot(self.fcords, clear=False, pen='r')
        

        
        
    
if __name__ == '__main__':    
    
    # Creating window
    app = QtWidgets.QApplication(sys.argv)    
    Form = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(Form) 
    
    # Show window
    ui.show()
    
    # Creating timer
    t=QtCore.QTimer()
    t.timeout.connect( ui.update ) # Connecting timer to update
    t.start(100) 

    # Exit
    sys.exit(app.exec_())
