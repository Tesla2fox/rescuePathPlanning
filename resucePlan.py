# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 10:41:40 2018

@author: robot
"""


import readCfg.read_cfg as rd
import numpy as np


class ResucePlan:
    def __init__(self,cfgFileName = './/data//1_8_8_3_Cfg.dat'):
        
        readCfg = rd.Read_Cfg(cfgFileName)    
        data = []
        readCfg.get('row',data)
        self.row = int(data.pop())    
        readCfg.get('col',data)
        self.col = int(data.pop())            
        self.mat = np.zeros((self.row,self.col))
        
        self.obRowLst = []
        self.obColLst = []
        readCfg.get('obRow',self.obRowLst)
        readCfg.get('obCol',self.obColLst)
        
        for i in range(len(self.obRowLst)):
            obRow = int(self.obRowLst[i])
            obCol = int(self.obColLst[i])
            self.mat[obRow][obCol] = 1 
    
    
        self.robRowLst = []
        self.robColLst = []
        readCfg.get('robRow',self.robRowLst)
        readCfg.get('robCol',self.robColLst)
        
        self.proLevLst = []
        readCfg.get('proLevGrid',self.proLevLst)
        self.proLevNum = int(readCfg.getSingleVal('proLevNum'))        
        self.proMat = []
                
    
    
    
    
    

if __name__ == '__main__':
    print('wtf')
    resPlan = ResucePlan(cfgFileName = './/data//1_8_8_3_Cfg.dat')
    
