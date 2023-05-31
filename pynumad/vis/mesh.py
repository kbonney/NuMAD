import plotly     


def plot2DMesh(self):
        xLst = self.nodes[0:self.numNodes,0]
        yLst = self.nodes[0:self.numNodes,1]
        zLst = np.zeros(self.numNodes)
        value = list()
        v1 = list()
        v2 = list()
        v3 = list()
        for i in range(0,self.numTriEls):
            v1.append(self.triElements[i,0])
            v2.append(self.triElements[i,1])
            v3.append(self.triElements[i,2])
            value.append(np.sin(i))
        for i in range(0,self.numQuadEls):
            v1.append(self.quadElements[i,0])
            v2.append(self.quadElements[i,1])
            v3.append(self.quadElements[i,2])
            value.append(np.sin(i))
            v1.append(self.quadElements[i,0])
            v2.append(self.quadElements[i,2])
            v3.append(self.quadElements[i,3])
            value.append(np.sin(i))
        fig = plotly.Figure(data=[
            plotly.Mesh3d(
                x=xLst,
                y=yLst,
                z=zLst,
                colorbar_title = '',
                colorscale=[[0.0, 'blue'],
                            [0.5, 'yellow'],
                            [1.0, 'red']],
                intensity=value,
                intensitymode='cell',
                i=v1,
                j=v2,
                k=v3,
                name='',
                showscale=True
            )
        ])

        fig.show()


def plotShellMesh(meshData):
    xLst = meshData['nodes'][:,0]
    yLst = meshData['nodes'][:,1]
    try:
        zLst = meshData['nodes'][:,2]
    except:
        zLst = np.zeros(len(xLst))
    value = list()
    v1 = list()
    v2 = list()
    v3 = list()
    i = 0
    for el in meshData['elements']:
        v1.append(el[0])
        v2.append(el[1])
        v3.append(el[2])
        value.append(np.sin(i))
        if(el[3] != -1):
            v1.append(el[0])
            v2.append(el[2])
            v3.append(el[3])
            value.append(np.sin(i))
        i = i + 1
    fig = plotly.Figure(data=[
        plotly.Mesh3d(
            x=xLst,
            y=yLst,
            z=zLst,
            colorbar_title = '',
            colorscale=[[0.0, 'white'],
                        [0.5, 'gray'],
                        [1.0, 'black']],
            intensity=value,
            intensitymode='cell',
            i=v1,
            j=v2,
            k=v3,
            name='',
            showscale=True
        )
    ])

    fig.show()
    
def plotSolidMesh(meshData):
    xLst = meshData['nodes'][:,0]
    yLst = meshData['nodes'][:,1]
    zLst = meshData['nodes'][:,2]
    value = list()
    v1 = list()
    v2 = list()
    v3 = list()
    i = 0
    for el in meshData['elements']:
        si = np.sin(i)
        if(el[4] == -1):
            v1.append(el[0])
            v2.append(el[1])
            v3.append(el[2])
            value.append(si)
            v1.append(el[0])
            v2.append(el[1])
            v3.append(el[3])
            value.append(si)
            v1.append(el[0])
            v2.append(el[2])
            v3.append(el[3])
            value.append(si)
            v1.append(el[1])
            v2.append(el[2])
            v3.append(el[3])
            value.append(si)
        elif(el[6] == -1):
            v1.append(el[0])
            v2.append(el[1])
            v3.append(el[2])
            value.append(si)
            v1.append(el[3])
            v2.append(el[4])
            v3.append(el[5])
            value.append(si)
            v1.append(el[0])
            v2.append(el[1])
            v3.append(el[3])
            value.append(si)
            v1.append(el[1])
            v2.append(el[3])
            v3.append(el[4])
            value.append(si)
            
            v1.append(el[0])
            v2.append(el[2])
            v3.append(el[3])
            value.append(si)
            v1.append(el[2])
            v2.append(el[3])
            v3.append(el[5])
            value.append(si)
            v1.append(el[1])
            v2.append(el[2])
            v3.append(el[4])
            value.append(si)
            v1.append(el[2])
            v2.append(el[4])
            v3.append(el[5])
            value.append(si)
        else:
            v1.append(el[0])
            v2.append(el[3])
            v3.append(el[4])
            value.append(si)
            v1.append(el[3])
            v2.append(el[4])
            v3.append(el[7])
            value.append(si)
            v1.append(el[1])
            v2.append(el[2])
            v3.append(el[5])
            value.append(si)
            v1.append(el[2])
            v2.append(el[5])
            v3.append(el[6])
            value.append(si)
            
            v1.append(el[0])
            v2.append(el[1])
            v3.append(el[4])
            value.append(si)
            v1.append(el[1])
            v2.append(el[4])
            v3.append(el[5])
            value.append(si)
            v1.append(el[2])
            v2.append(el[3])
            v3.append(el[6])
            value.append(si)
            v1.append(el[3])
            v2.append(el[6])
            v3.append(el[7])
            value.append(si)
            
            v1.append(el[0])
            v2.append(el[1])
            v3.append(el[2])
            value.append(si)
            v1.append(el[0])
            v2.append(el[2])
            v3.append(el[3])
            value.append(si)
            v1.append(el[4])
            v2.append(el[5])
            v3.append(el[6])
            value.append(si)
            v1.append(el[4])
            v2.append(el[6])
            v3.append(el[7])
            value.append(si)
        i = i + 1
    fig = plotly.Figure(data=[
        plotly.Mesh3d(
            x=xLst,
            y=yLst,
            z=zLst,
            colorbar_title = '',
            colorscale=[[0.0, 'white'],
                        [0.5, 'gray'],
                        [1.0, 'black']],
            intensity=value,
            intensitymode='cell',
            i=v1,
            j=v2,
            k=v3,
            name='',
            showscale=True
        )
    ])

    fig.show()
