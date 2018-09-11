# -*- coding: utf-8 -*-
"""
Created on Sat Sep  8 16:04:50 2018

@author: robot
"""

import numpy as np
import random 
import networkx as nx
import matplotlib.pyplot as plt
import datetime
import readCfg.read_cfg as rd 
import math 
import copy as cp

def getNeighbor(envMat,lst = (0,0),row =20, col =20):
    resLst = []
    #left
    lstLeft = (lst[0]-1,lst[1])
    if(lstLeft[0]>=0):
        if(envMat[lstLeft[0]][lstLeft[1]]==1):
            resLst.append(lstLeft)
    #right
    lstRight = (lst[0]+1,lst[1])
    if(lstRight[0]<row):
        if(envMat[lstRight[0]][lstRight[1]]==1):
            resLst.append(lstRight)    
    #top
    lstTop = (lst[0],lst[1]+1)
    if(lstTop[1]<col):
        if(envMat[lstTop[0]][lstTop[1]]==1):
            resLst.append(lstTop)    
    #bottom    
    lstBottom = (lst[0],lst[1]-1)
    if(lstBottom[1]>=0):
        if(envMat[lstBottom[0]][lstBottom[1]]==1):
            resLst.append(lstBottom)
    
    return resLst



if __name__ == '__main__':
#    print('wtf')
    row = 8
    col = 8
    
    mat = np.zeros((row,col),dtype=int)
    for i in range(row):
        for j in range(col):
            mat[i][j] = 1
# zero means the obstacle pnt
# one means the way pnt
    
    robNum = 1
    obNum  = 3
    random.seed(10)
    
    
    obRowLst = []
    obColLst = []
    while len(obRowLst)<obNum :
        obRow = random.randint(0,row - 1)
        obCol = random.randint(0,col - 1)
        reasonable = True
        for i in range(len(obRowLst)):
            if obRow == obRowLst[i] and obCol == obColLst[i]:
                reasonable = False
                break
        if reasonable:
            mat[obRow][obCol] = 0
            obRowLst.append(obRow)
            obColLst.append(obCol)
            
    robRowLst = []
    robColLst = []
    while len(robRowLst)<robNum:
        robRow = random.randint(0,row - 1)
        robCol = random.randint(0,col - 1)
        reasonable = True
        for i in range(len(robRowLst)):
            if robRow == robRowLst[i] and robCol == robColLst[i]:
                reasonable = False
                break
        for i in range(len(obRowLst)):
            if robRow == obRowLst[i] and robCol == obColLst[i]:
                reasonable = False
                break
        if reasonable:
            robRowLst.append(robRow)
            robColLst.append(robCol)
            

    
#    testNei = getNeighbor(envMat =mat,lst = [0,0],row =row,col=col)
#    print(testNei)
    
    sPntx = []
    sPnty = []
    tPntx = []
    tPnty = []
    G = nx.Graph()
    for i in range(row):
        for j in range(col):
            centre = (i,j)
            G.add_node((i,j))
            if(mat[i][j] == 0):
                continue            
            neiLst =getNeighbor(envMat = mat, lst = centre,row = row, col =col)
            for unit in neiLst:
#                print('')
                sPntx.append(i + 0.5)
                sPnty.append(j + 0.5)
                tPntx.append(unit[0] + 0.5)
                tPnty.append(unit[1] + 0.5)
                G.add_edge(centre,unit)
#    component2 = nx.connected_components(G)
#    print(component2)
    component = list(nx.connected_components(G))
#    print(component)
    reachComponentLst = []
    unReachCompLst = [n for n in range(len(component))]
    for i in range(robNum):
        for j in range(len(component)):
            if(reachComponentLst.count(j) !=1):
                if((robRowLst[i],robColLst[i]) in component[j]):
                    reachComponentLst.append(j)
                    unReachCompLst.remove(j)
#                    print(reachComponentLst)            
    

    robReachRowLst = []
    robReachColLst = []
    for unit in reachComponentLst:
        for gridUnit in component[unit]:
            robReachRowLst.append(gridUnit[0])
            robReachColLst.append(gridUnit[1])    

#    print(len(robReachRowLst))
    robUnReachRowLst = []
    robUnReachColLst = []
    for unit in unReachCompLst:
        for gridUnit in component[unit]:
            robUnReachRowLst.append(gridUnit[0])
            robUnReachColLst.append(gridUnit[1])
                            
    obRowLst = robUnReachRowLst
    obColLst = robUnReachColLst 
    
    obLst = []
    for i in range(len(obRowLst)):
        obLst.append((obRowLst[i],obColLst[i]))
    
#    print(obLst)
    proMat = np.zeros((row,col))

    for i in range(row):
        for  j in range(col):
            if (i,j) not in obLst:                
                proMat[i][j] = random.random()
    proSum = np.sum(proMat)
    proMax = np.max(proMat)
#    print(proSum)
#    print(proMax)
    for i,j in np.ndindex(proMat.shape):
        proMat[i][j] = proMat[i][j]/proSum

    proSum = np.sum(proMat)
    proMax = np.max(proMat)
    proLevNum = 4
    proLevLst = [0]*(proLevNum+1)
    proUnit  = proMax/proLevNum


    for i,j in np.ndindex(proMat.shape):        
        proMat[i][j] = math.ceil(proMat[i][j]/proUnit)
        proLevLst[int(proMat[i][j])] += 1

    proUnitNum = 0
    count = 0
    for i in range(len(proLevLst)):
        proUnitNum += i*proLevLst[i]
    
    proLevMat = cp.deepcopy(proMat)
#    print(proLevMat)
    proUnit = 1/proUnitNum 
    for i,j in np.ndindex(proMat.shape):
        proMat[i][j] *= proUnit
        if proMat[i][j] == 0:
            count += 1
    proSum = np.sum(proMat)
    
            
    conFileDir = './/data//'
    conFileCfg = conFileDir + str(robNum)+'_'+str(row)+'_'+str(col)+'_'+str(obNum)+'_Cfg.dat'
    f_con = open(conFileCfg , 'w')
    
#    print(conFileCfg)
    
    f_con.write('time '+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'\n')
    rd.writeConf(f_con,'row',[row])
    rd.writeConf(f_con,'col',[col])
    rd.writeConf(f_con,'robRow',robRowLst)
    rd.writeConf(f_con,'robCol',robColLst)
    rd.writeConf(f_con,'robReachRowLst',robReachRowLst)
    rd.writeConf(f_con,'robReachColLst',robReachColLst)

    
    rd.writeConf(f_con,'robUnReachRowLst',robUnReachRowLst)
    rd.writeConf(f_con,'robUnReachColLst',robUnReachColLst)
    
    grid = []    
    for x,y in np.ndindex(mat.shape):
        grid.append(int(mat[x][y]))
    rd.writeConf(f_con,'grid',grid)
        
    rd.writeConf(f_con,'obRow',obRowLst)
    rd.writeConf(f_con,'obCol',obColLst)
    proGrid = []
    for i,j in np.ndindex(proMat.shape):
        proGrid.append(proMat[i][j])
    rd.writeConf(f_con,'proGrid',proGrid)
    rd.writeConf(f_con,'proLevNum',[proLevNum])   
    proLevGrid = []
    for i,j in np.ndindex(proLevMat.shape):
        proLevGrid.append(int(proLevMat[i][j]))
    rd.writeConf(f_con,'proLevGrid',proLevGrid)
    rd.writeConf(f_con,'proUnit',[proUnit])
            
    f_con.close()
    