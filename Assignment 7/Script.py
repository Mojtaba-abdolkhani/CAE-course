from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
#input
width_1, height_1, radius_1 = getInputs(fields=(('Width:', '16'),('height:','10'), ('radius:', '3')),
	label='Specify block dimensions:',
	dialogTitle='Create Block', )
    
width_val=float(width_1)
height_val=float(height_1)
radius_val=float(radius_1)
elem_size=width_val/100 

traction = float(getInput('Enter Uniform traction:','0.16'))
traction=float(traction)
Mdb()
#creating part
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=2*width_val)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(point1=(radius_val, 0.0), point2=(width_val/2, 0.0))
s.HorizontalConstraint(entity=g[2], addUndoState=False)
s.Line(point1=(width_val/2, 0.0), point2=(width_val/2, height_val/2))
s.VerticalConstraint(entity=g[3], addUndoState=False)
s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
s.Line(point1=(width_val/2, height_val/2), point2=(0.0, height_val/2))
s.HorizontalConstraint(entity=g[4], addUndoState=False)
s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
s.Line(point1=(0.0, height_val/2), point2=(0.0, radius_val))
s.VerticalConstraint(entity=g[5], addUndoState=False)
s.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
s.ArcByCenterEnds(center=(0.0, 0.0), point1=(0.0, radius_val), point2=(radius_val, 0.0), 
    direction=CLOCKWISE)
p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['Part-1']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
p = mdb.models['Model-1'].parts['Part-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['Model-1'].sketches['__profile__']
#creating material
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((200000.0, 0.3), 
    ))
#creating section
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
    material='Material-1', thickness=None)
#assigning section
p = mdb.models['Model-1'].parts['Part-1']
f = p.faces
x_middle=radius_val+(((width_val/2)-radius_val)/2)
y_middle=radius_val+(((height_val/2)-radius_val)/2)
faces = f.findAt(((x_middle, y_middle, 0.0), ))
region = p.Set(faces=faces, name='Set-1')
p = mdb.models['Model-1'].parts['Part-1']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
#assembly
a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-1']
a1.Instance(name='Part-1-1', part=p, dependent=OFF)
#step
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
#BC-left
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['Part-1-1'].edges
edges1 = e1.findAt(((0.0,y_middle , 0.0), ))
region = a.Set(edges=edges1, name='Set-2')
mdb.models['Model-1'].XsymmBC(name='BC-1', createStepName='Initial', 
    region=region, localCsys=None)
#BC-bot
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['Part-1-1'].edges
edges1 = e1.findAt(((x_middle, 0.0, 0.0), ))
region = a.Set(edges=edges1, name='Set-3')
mdb.models['Model-1'].YsymmBC(name='BC-2', createStepName='Initial', 
    region=region, localCsys=None)
#LOAD
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['Part-1-1'].edges
side1Edges1 = s1.findAt(((width_val/4, height_val/2, 0.0), ))
region = a.Surface(side1Edges=side1Edges1, name='Surf-1')
mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=-traction, 
    amplitude=UNSET)
#mesh
import mesh
a = mdb.models['Model-1'].rootAssembly
partInstances =(a.instances['Part-1-1'], )
a.seedPartInstance(regions=partInstances, size=elem_size, deviationFactor=0.1, 
    minSizeFactor=0.1)
elemType1 = mesh.ElemType(elemCode=CPE4R, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, hourglassControl=DEFAULT, 
    distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=CPE3, elemLibrary=STANDARD)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['Part-1-1'].faces
faces1 = f1.findAt(((x_middle, y_middle, 0.0), ))
pickedRegions =(faces1, )
a.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
a = mdb.models['Model-1'].rootAssembly
partInstances =(a.instances['Part-1-1'], )
a.generateMesh(regions=partInstances)
#creating job
mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)
#submit
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
mdb.jobs['Job-1'].waitForCompletion()
#OUTPUT VISUAL
o3 = session.openOdb(name='Job-1.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
#output
import os 
dirpath = os.getcwd()

o3 = session.openOdb(
    name=dirpath +'/Job-1.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o3)

odb=o3	
s_num=len(odb.steps['Step-1'].frames[1].fieldOutputs['S'].values)
a=[0]*s_num
j=0
while j< s_num:
	a[j]=(odb.steps['Step-1'].frames[1].fieldOutputs['S'].values[j].data[1])
	j=j+1

max_s= max(a)
print 'max stress in y direction=',max_s
Kt=max_s/traction
print 'Stress Concentration factor=',Kt































