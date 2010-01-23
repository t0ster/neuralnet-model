#!/usr/bin/env python
'''
Created on Jan 22, 2010

@author: t0ster
'''
from PyQt4 import QtCore, QtGui
from ffnet import ffnet, mlgraph, savenet, loadnet
import numpy

class Cell(QtGui.QFrame):
    def __init__(self, filled=False):
        super(Cell, self).__init__()
        self.filled = filled
        
        self.set_attributes()
        self.set_color()
#        self.connect(self, QtCore.SIGNAL("clicked()"), self.change_color)

    def set_attributes(self):
        self.setMinimumSize(10, 10)
#        self.setFixedWidth(10)
#        self.setFixedHeight(10)
        self.setLineWidth(1)
        self.setAutoFillBackground(True)
        self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Plain)

        
    def mousePressEvent(self, mouse_event):
#        self.emit(QtCore.SIGNAL("clicked()"))
        self.change_color()
        
#    def resizeEvent(self, resize_event):
#        self.emit(QtCore.SIGNAL("resized()"))
        
    def set_color(self):
        p = QtGui.QPalette(self.palette())
        if self.filled:
            p.setColor(QtGui.QPalette.Background, QtGui.QColor('black'))
        else:
            p.setColor(QtGui.QPalette.Background, QtGui.QColor('white'))
        self.setPalette(p)
        
    def change_color(self):
        self.filled = not self.filled
        self.set_color()
        
    def resize1_1(self):
        self.setMinimumHeight(self.width())
        self.setMinimumHeight(10)
        
        
        
class Field(QtGui.QWidget):
    def __init__(self, x=20, y=20):
        super(Field, self).__init__()
        self.x = x
        self.y = y
        self.xy = {}
        
        grid = QtGui.QGridLayout()
        grid.setSpacing(0)
        for _x in range(x):
            for _y in range(y):
                self.xy[(_x,_y)] = c = Cell()
                grid.addWidget(c, _y, _x)
        self.setLayout(grid)
        
        
    def clear(self):
        for _x in range(self.x):
            for _y in range(self.y):
                self.xy[(_x,_y)].filled = False
                self.xy[(_x,_y)].set_color()
    
    
    def get_values(self):
        data = [0.0]*self.x*self.y
        
        def get_xy_minmax():
            x_min = self.x-1
            x_max = 0
            y_min = self.y-1
            y_max = 0
            for _x in range(self.x):
                for _y in range(self.y):
                    if self.xy[(_x,_y)].filled:
                        if _x < x_min:
                            x_min = _x
                        if _x > x_max:
                            x_max = _x
                        if _y < y_min:
                            y_min = _y
                        if _y > y_max:
                            y_max = _y
            return x_min, x_max, y_min, y_max
        x_min, x_max, y_min, y_max = get_xy_minmax()
                        
        i = 0
        for _x in range(x_min, x_max+1):
            for _y in range(y_min, y_max+1):
                data[i] = self.xy[(_x,_y)].filled and 1.0 or 0.0
                i += 1
#        print (x_min, x_max), (y_min, y_max) 
#        print data
        return data
    
    
class Main(QtGui.QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.field = Field(20, 20)
        
        self.outputs = []
        
        self.input = []
        self.target = []
        
        b = QtGui.QPushButton("Learn!")
        self.connect(b, QtCore.SIGNAL("clicked()"), self.learn_perceptron)
        
        self.outcomes_list = QtGui.QComboBox()
        self.add_output("Square")
        self.add_output("Triangle")
        self.add_output("Line")
        
        hpanel = QtGui.QHBoxLayout()
        hpanel.addWidget(self.outcomes_list)
        hpanel.addWidget(b)
        
        btn_classify = QtGui.QPushButton("Classify")
        self.connect(btn_classify, QtCore.SIGNAL("clicked()"), self.classify)
        
        btn_clear = QtGui.QPushButton("Clear")
        self.connect(btn_clear, QtCore.SIGNAL("clicked()"), self.clear)
        
        self.label_output = QtGui.QLabel()
        self.label_output.setMaximumHeight(20)
        
        vpanel = QtGui.QVBoxLayout()
        vpanel.addWidget(self.field)
        vpanel.addLayout(hpanel)
        vpanel.addWidget(self.label_output)
        vpanel.addWidget(btn_classify)
        vpanel.addWidget(btn_clear)
        
        self.setLayout(vpanel)
        
        try:
            self.net = loadnet("netdata.dat")
        except IOError:
            conec = mlgraph((self.field.x*self.field.y,10,10,3))
            self.net = ffnet(conec)
        
    
    def add_output(self, output):
        self.outputs.append(output)
        self.outcomes_list.addItem(output)
        
        
    def closeEvent(self, close_event):
        self.save_net()
        
        
    def learn_perceptron(self):
        self.input.append(self.field.get_values())
        
        a = [0.0]*3; a[self.outcomes_list.currentIndex()] = 1.0
        self.target.append(a)
#        print a
        
#        conec = mlgraph((self.field.x*self.field.y,10,10,3))
#        self.net = ffnet(conec)
        
#        self.net.train_tnc((self.field.get_values(),), (a,), maxfun = 2000, messages=1)
        self.net.train_tnc(numpy.array(self.input), numpy.array(self.target), maxfun = 2000, messages=1)
        
        
    def save_net(self):
        savenet(self.net, "netdata.dat")
        
        
    def classify(self):
        self.label_output.setText(self.outputs[self.net.call(numpy.array(self.field.get_values())).argmax()])
#        print self.net.derivative(numpy.array(self.field.get_values()))
        
        
    def clear(self):
        self.field.clear()    
                

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    m = Main()
#    app.connect(app, "lastWindowClosed()", m.save_net)
    m.show()
    
    sys.exit(app.exec_())