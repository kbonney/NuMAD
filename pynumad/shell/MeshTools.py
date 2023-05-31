import numpy as np
import plotly.graph_objects as go
from pynumad.shell.SpatialGridList2DClass import *
from pynumad.shell.SpatialGridList3DClass import *

## - Convert list of mesh objects into a single merged mesh, returning sets representing the elements/nodes from the original meshes     
def mergeDuplicateNodes(meshData):
    allNds = meshData['nodes']
    allEls = meshData['elements']
    totNds = len(allNds)
    spaceDim = len(allNds[0])
    totEls = len(allEls)
    elDim = len(allEls[0])

    maxX = np.amax(allNds[:,0])
    minX = np.amin(allNds[:,0])
    maxY = np.amax(allNds[:,1])
    minY = np.amin(allNds[:,1])
    nto1_2 = np.power(totNds,0.5)
    nto1_3 = np.power(totNds,0.3333333)
    nto1_4 = np.power(totNds,0.25)
    if(spaceDim == 3):
        maxZ = np.amax(allNds[:,2])
        minZ = np.amin(allNds[:,2])
        dimVec = np.array([(maxX-minX),(maxY-minY),(maxZ-minZ)])
        meshDim = np.linalg.norm(dimVec)
        maxX = maxX + 0.01*meshDim
        minX = minX - 0.01*meshDim
        maxY = maxY + 0.01*meshDim
        minY = minY - 0.01*meshDim
        maxZ = maxZ + 0.01*meshDim
        minZ = minZ - 0.01*meshDim
        xSpacing = 0.5*(maxX - minX)/nto1_3
        ySpacing = 0.5*(maxY - minY)/nto1_3
        zSpacing = 0.5*(maxZ - minZ)/nto1_3
        nodeGL = SpatialGridList3D(minX,maxX,minY,maxY,minZ,maxZ,xSpacing,ySpacing,zSpacing)
        tol = 1.0e-6*meshDim/nto1_3
    else:
        dimVec = np.array([(maxX-minX),(maxY-minY)])
        meshDim = np.linalg.norm(dimVec)
        maxX = maxX + 0.01*meshDim
        minX = minX - 0.01*meshDim
        maxY = maxY + 0.01*meshDim
        minY = minY - 0.01*meshDim
        xSpacing = 0.5*(maxX - minX)/nto1_3
        ySpacing = 0.5*(maxY - minY)/nto1_3
        nodeGL = SpatialGridList2D(minX,maxX,minY,maxY,xSpacing,ySpacing)
        tol = 1.0e-6*meshDim/nto1_2
        
    i = 0
    for nd in allNds:
        nodeGL.addEntry(i,nd)
        i = i + 1
    
    ndElim = -np.ones(totNds,dtype=int)
    ndNewInd = -np.ones(totNds,dtype=int)
    for n1i in range(0,totNds):
        if(ndElim[n1i] == -1):
            nearNds = nodeGL.findInRadius(allNds[n1i],tol)
            for n2i in nearNds:
                if(n2i > n1i and ndElim[n2i] == -1):
                    proj = allNds[n2i] - allNds[n1i]
                    dist = np.linalg.norm(proj)
                    if(dist < tol):
                        ndElim[n2i] = n1i
    ndi = 0
    nodesFinal = list()
    for n1i in range(0,totNds):
        if(ndElim[n1i] == -1):
            nodesFinal.append(allNds[n1i])
            ndNewInd[n1i] = ndi
            ndi = ndi + 1
    nodesFinal = np.array(nodesFinal)
    for eli in range(0,totEls):
        for j in range(0,elDim):
            nd = allEls[eli,j]
            if(nd != -1):
                if(ndElim[nd] == -1):
                    allEls[eli,j] = ndNewInd[nd]
                else:
                    allEls[eli,j] = ndNewInd[ndElim[nd]]
    
    meshData['nodes'] = nodesFinal
    meshData['elements'] = allEls
    
    return meshData
    
def make3D(meshData):
    numNodes = len(meshData['nodes'])
    nodes3D = np.zeros((numNodes,3))
    nodes3D[:,0:2] = meshData['nodes']
    dataOut = dict()
    dataOut['nodes'] = nodes3D
    dataOut['elements'] = meshData['elements']
    return dataOut
 