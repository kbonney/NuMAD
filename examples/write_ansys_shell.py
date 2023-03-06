import numpy as np
from os.path import join

from pynumad.io.ansys import writeANSYSshellModel
from pynumad.objects.Blade import Blade


yamlpath = join("..","data","blade_yamls","myBlade.yaml")
blade = Blade(yamlpath)
blade.mesh = 0.2

adhes = 1

meshData = blade.getShellMesh(includeAdhesive=adhes)
config = {}
config["BoundaryCondition"] = 'cantilevered'
config["elementType"] = '181'
config["MultipleLayerBehavior"] = 'multiply'
config["dbgen"] = 1
config["dbname"] = 'master'

filename = "myblade_ansys.src"
includeAdhesive = 1

writeANSYSshellModel(blade,filename,meshData,config,includeAdhesive)