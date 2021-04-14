import log
import sys
import pyqtgraph.opengl as gl
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__()
        self.resize(1000, 800)
        
        self.worldCreated = False

        self.graph = pg.PlotWidget(self)
        #self.statGraph = pg.PlotWidget(self)
        self.lbl = []
        self.addLineNames()
        
        self.stopWorld = False
        self.cbStopWorld = QtWidgets.QCheckBox("Остановить мир после смерти всех Лис/Зайцев", self)
        self.cbStopWorld.move(600, 470)
        self.cbStopWorld.stateChanged.connect(self.changeStopWorld)
        
        self.widget = gl.GLViewWidget(self)
        
        
        self.widget.setBackgroundColor('#adf')
        self.widget.setGeometry(0, 0, 1000, 450)  
        self.widget.opts['distance'] = 200
        
        
        self.updateWorld = False
        self.bcords = []
        self.fcords = []
        
        self.bCount = 0
        self.fCount = 0
        self.bcords.append(self.bCount)
        self.fcords.append(self.fCount)
        
        
        #self.statGraph.setGeometry(400, 500, 200, 200) 
        
        self.graph.setYRange(0, 100)
        self.graph.setGeometry(10, 490, 300, 300) 

        self.button_new = QtWidgets.QPushButton('New', self)
        self.button_pause = QtWidgets.QPushButton('Pause', self)
        self.button_start = QtWidgets.QPushButton('Start', self)
        
        self.inLines = []
        for i in range(7):
            self.inLines.append(QtWidgets.QLineEdit(self)) 
            self.inLines[i].move(800, 500 + i*40)
        
        self.button_new.clicked.connect(self.createWorld)
        self.button_pause.clicked.connect(self.pause)
        self.button_start.clicked.connect(self.start)
        
        self.button_new.move(500, 500)
        self.button_pause.move(500, 550)
        self.button_start.move(500, 600)
        
        self.mh = []
        self.prT = []
        self.spd = [] 
      
    def changeStopWorld(self):
        if self.stopWorld == True:
            self.stopWorld = False
        else:
            self.stopWorld = True
      
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
        
        
    def createWorld(self):
        inputs = []
        for i in range(7):
            inputs.append( self.inLines[i].text() )
            inputs[i] =  abs(int(inputs[i])) if inputs[i].isdigit() and inputs[i] != '0' else 1
        
        
        if(self.worldCreated == True):
            self.myWorld.delete()
        
        self.myWorld = log.world(self.widget, inputs[0], bPopulation=inputs[1], fPopulation=inputs[2], 
                                 foodCount=inputs[3], foodProdSpeed=inputs[4], bunnyDefHunger=inputs[5], 
                                 foxDefHunger=inputs[6])
        self.worldCreated = True
        
        self.bcords.clear()
        self.fcords.clear()
        
        self.bCount = len(self.myWorld.bPop)
        self.fCount = len(self.myWorld.fPop)
        self.bcords.append(self.bCount)
        self.fcords.append(self.fCount)
        
        self.updateWorld = True
        
    def pause(self):
        self.updateWorld = False
    def start(self):
        self.updateWorld = True
     
    def update(self):
        if self.updateWorld == False:
            return
        
        bLen= len(self.myWorld.bPop)
        fLen= len(self.myWorld.fPop)
        
        if self.stopWorld == True:
            if bLen == 0 or fLen == 0:
                return
        
        # mh = 0
        # for i in self.myWorld.bPop:
            # mh += i.maxHunger
        # mh /= bLen
        # self.mh.append(mh)
        #
        # prT = 0
        # for i in self.myWorld.bPop:
            # prT += i.produceTime
        # prT /= bLen
        # self.prT.append(prT)
        #
        # spd = 0
        # for i in self.myWorld.bPop:
            # spd += i.speed*10
        # spd /= bLen
        # self.spd.append(spd)
        #
        # self.statGraph.plot(self.mh, clear=True, pen='r')
        # self.statGraph.plot(self.prT, clear=False, pen='g')
        # self.statGraph.plot(self.spd, clear=False, pen='b')
        
        self.bCount = len(self.myWorld.bPop)
        self.fCount = len(self.myWorld.fPop)
        self.myWorld.update()
        self.bcords.append(self.bCount)
        self.fcords.append(self.fCount)
        self.graph.setTitle("Model")
        self.graph.plot(self.bcords, clear=True, pen='b')
        self.graph.plot(self.fcords, clear=False, pen='r')
        

        
        
    
if __name__ == '__main__':    
    
    app = QtWidgets.QApplication(sys.argv)    
    Form = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(Form) 
    
    ui.show()
    
    t=QtCore.QTimer()
    t.timeout.connect( ui.update )
    t.start(100) 
    sys.exit(app.exec_())
