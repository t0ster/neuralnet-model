#!/usr/bin/env python
'''
Created on Jan 22, 2010

@author: t0ster
'''
from PyQt4 import QtCore, QtGui
from widgets import Field
from ffnet import ffnet, mlgraph, savenet, loadnet
import numpy


class NeuralNetwork(QtGui.QWidget):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.field = Field(20, 20)
        
        self.outputs = []
        
        self.input = []
        self.target = []
        
        b = QtGui.QPushButton("Learn!")
        self.connect(b, QtCore.SIGNAL("clicked()"), self.learn)
        
        self.outcomes_list = QtGui.QComboBox()
        self._add_output("Square")
        self._add_output("Triangle")
        self._add_output("Line")
        
        hpanel = QtGui.QHBoxLayout()
        hpanel.addWidget(self.outcomes_list)
        hpanel.addWidget(b)
        
        btn_classify = QtGui.QPushButton("Classify")
        self.connect(btn_classify, QtCore.SIGNAL("clicked()"), self.classify)
        
        btn_clear = QtGui.QPushButton("Clear")
        self.connect(btn_clear, QtCore.SIGNAL("clicked()"), self.clear)
        
        self.label_output = QtGui.QLabel()
        self.label_output.setMaximumHeight(20)
        
        self.label_epoch = QtGui.QLabel()
        self.label_epoch.setMaximumHeight(20)
        
        vpanel = QtGui.QVBoxLayout()
        vpanel.addWidget(self.field)
        vpanel.addLayout(hpanel)
        vpanel.addWidget(self.label_output)
        vpanel.addWidget(self.label_epoch)
        vpanel.addWidget(btn_classify)
        vpanel.addWidget(btn_clear)
        
        self.setLayout(vpanel)
        
        try:
            self.net, self.epoch = loadnet("netdata.dat")
        except IOError:
            conec = mlgraph((self.field.x*self.field.y, 10, 10, 3))
            self.net = ffnet(conec)
            self.epoch = 0
        
    
    def _add_output(self, output):
        self.outputs.append(output)
        self.outcomes_list.addItem(output)
        
        
    def closeEvent(self, close_event):
        self.save_net()
        
        
    def learn(self):
        self.epoch += 1
        self.input.append(self.field.get_values())
        
        a = [0.0]*3; a[self.outcomes_list.currentIndex()] = 1.0
        self.target.append(a)

        self.net.train_tnc(numpy.array(self.input), numpy.array(self.target), maxfun = 2000, messages=1)
        
        
    def save_net(self):
        savenet((self.net, self.epoch), "netdata.dat")
        
        
    def classify(self):
        res_array = self.net.call(numpy.array(self.field.get_values()))
        print (res_array)
        res_arg = res_array.argmax()
        res_value = res_array[res_arg]
        self.label_output.setText("%s (%s)" % (self.outputs[res_arg], res_value) )
        self.label_epoch.setText("Epoch: %s" % self.epoch)
        
        
    def clear(self):
        self.field.clear()    
                


if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    m = NeuralNetwork()
    m.show()
    
    sys.exit(app.exec_())