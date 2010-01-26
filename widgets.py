'''
Created on 26.01.2010

@author: t0ster
'''
from PyQt4 import QtGui

class Cell(QtGui.QFrame):
    def __init__(self, filled=False):
        super(Cell, self).__init__()
        self.filled = filled
        
        self.set_attributes()
        self.set_color()


    def set_attributes(self):
        self.setMinimumSize(10, 10)
        self.setLineWidth(1)
        self.setAutoFillBackground(True)
        self.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Plain)


    def mousePressEvent(self, mouse_event):
        self.change_color()        
        
    
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
    
        
    def resize1_1(self): # not used
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
        return data