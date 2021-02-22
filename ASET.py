#!/usr/bin/python3

#Codelco - Nuevo Nivel Mina

#--------------------------------INPUTS-----------------------------------------

                            #Geometría del Túnel

X=9.4 #ancho tunel
Y=400 #largo del tunel
Z=6.0 #altura tunel
cx=0.2 #tamaño celda en x
cy=0.4 #tamaño celda en y
cz=0.25 #tamaño celda en z

#Curva para dibujar tunel - interpolación Excel con geometría AutoCad

def f(x):
    return -1*0.00037731654713724100*x**6 + 0.01064032662972640000*x**5 - 0.12023951690048300000*x**4 + 0.69353748265166400000*x**3 - 2.25803586101028000000*x**2 + 4.43075769525603000000*x**1 + 0.00018151820924572300

                            #Inputs Correa

b = 2 #ancho de correa
h = 1.3 #altura de la correa
x_correa = 2.5 #distancia desde pared del tunel

                            #Incendio de diseño (nada aún)

vel_viento = 0.7
spread_rate = 0.02


#----------------------------CÁLCULOS PREVIOS-----------------------------------
#Cálculos varios

n_x=X/cx #numero de celdas en X
n_y=Y/cy #numero de celdas en Y
n_z=Z/cz #numero de celdas en Z



#-------------------------EDITOR ARCHIVO FDS------------------------------------

Modelo = 'ASET.fds'
with open(Modelo,'w') as file_object:

#---------------------------GEOMETRY AND INITIAL PARAMETERS---------------------

    file_object.write("&HEAD CHID='ASET', TITLE='ASET'/ \n")
    file_object.write("\n")

    file_object.write("&MESH IJK="+str(n_x)+","+str(n_y)+","+str(n_z)+", XB=0.0"+","+str(X)+",0.0,"+str(Y)+",0.0,"+str(Z)+"/ \n")
    file_object.write("\n")

    file_object.write("&TIME T_END=1100. / \n")
    file_object.write("\n")

    file_object.write("&VENT XB=0.0,"+str(X)+", 0.0, 0.0, 0.0,"+str(Z)+", SURF_ID='WIND' /\n")
    file_object.write("&SURF ID = 'WIND', VEL=-"+str(vel_viento)+" / \n")
    file_object.write("&VENT MB='XMIN', SURF_ID='OPEN'/ \n")
    file_object.write("&VENT MB='XMAX', SURF_ID='OPEN'/ \n")
    file_object.write("&VENT MB='YMAX', SURF_ID='OPEN'/ \n")
    file_object.write("&VENT MB='ZMIN', SURF_ID='OPEN'/ \n")
    file_object.write("&VENT MB='ZMAX', SURF_ID='OPEN'/ \n")
    file_object.write("\n")

    file_object.write("Suelo tunel \n")
    file_object.write("\n")
    file_object.write("&OBST XB=0,"+str(X)+",0,"+str(Y)+",0,0 SURF_ID='CONCRETE SURFACE' / \n")
    file_object.write("\n")

    file_object.write("Paredes tunel \n")
    file_object.write("\n")
    file_object.write("&OBST XB=0,0,0,"+str(Y)+","+str(Z)+" SURF_ID='CONCRETE SURFACE'/ \n")
    file_object.write("&OBST XB=9.4,9.4,0,"+str(Y)+","+str(Z)+" SURF_ID='CONCRETE SURFACE'/ \n")
    file_object.write("\n")

    file_object.write("Techo tunel \n")
    file_object.write("\n")
    file_object.write("&OBST XB=0,"+str(X)+",0,"+str(Y)+","+str(Z)+","+str(Z)+" SURF_ID='CONCRETE SURFACE' / \n")
    file_object.write("\n")

    file_object.write("Correa \n")
    file_object.write("\n")
    file_object.write("&OBST XB="+str(x_correa)+","+str(x_correa+b)+",0,"+str(Y)+",0,"+str(h)+" / \n") #Obstaculo para correa
    file_object.write("\n")
    n=1
    dx=cx
    while n<=47:
        file_object.write("&OBST XB="+str((n-1)*dx)+","+str(n*dx)+",0,"+str(Y)+","+str(1.4+f(n*dx))+",6 SURF_ID='CONCRETE SURFACE' / \n") #Para dibujar forma del túnel
        n+=1

    file_object.write("\n")
    file_object.write("&SURF ID = 'CONCRETE SURFACE', MATL_ID = 'CONCRETE', RGB = 128,128,128, THICKNESS = 0.4/ \n")
    file_object.write("&MATL ID = 'CONCRETE', SPECIFIC_HEAT = 0.88, DENSITY = 2100., CONDUCTIVITY = 1.0 / \n")
    file_object.write("\n")

#---------------------------DESIGN FIRE-----------------------------------------

    file_object.write("&VENT XB=2.5,2.7,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=2.6,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("&VENT XB=2.7,2.9,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=2.8,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("&VENT XB=2.9,3.1,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=2.8,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("&VENT XB=3.1,3.3,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=3.2,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("&VENT XB=3.3,3.5,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=3.4,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("&VENT XB=3.5,3.7,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=3.6,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("&VENT XB=3.7,3.9,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=3.8,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("&VENT XB=3.9,4.1,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=4.0,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("&VENT XB=4.1,4.3,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=4.2,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("&VENT XB=4.3,4.5,0,"+str(Y)+",1.3,1.3 SURF_ID='FIRE', XYZ=4.4,0.0,1.3, SPREAD_RATE ="+str(spread_rate)+ "/ \n")
    file_object.write("\n")

    file_object.write("&REAC FUEL = 'PROPANE', SOOT_YIELD = 0.11, CO_YIELD = 0.16, HEAT_OF_COMBUSTION = 30000. / \n")
    file_object.write("&SPEC ID='PROPANE', MASS_EXTINCTION_COEFFICIENT = 8700. / \n")
    file_object.write("&SURF ID = 'FIRE', HRRPUA =500.  / \n")
    file_object.write("\n")

#-------------------------OUTPUTS & DEVICES-------------------------------------
    file_object.write("//=========================================================================  \n")
    file_object.write("// OUTPUT  \n")
    file_object.write("//=========================================================================  \n")
    file_object.write("\n")

    file_object.write("&DEVC XB=7,7,1,"+str(Y)+",1.5,1.5, QUANTITY='VOLUME FRACTION', SPEC_ID='CARBON MONOXIDE', ID='CO_7',POINTS=200, TIME_HISTORY=.TRUE. / \n") #Medición lado derecho correa
    file_object.write("&DEVC XB=7,7,1,"+str(Y)+",1.5,1.5, QUANTITY='VOLUME FRACTION', SPEC_ID='CARBON DIOXIDE', ID='CO2_7',POINTS=200, TIME_HISTORY=.TRUE. / \n")
    file_object.write("&DEVC XB=7,7,1,"+str(Y)+",1.5,1.5, QUANTITY='VOLUME FRACTION', SPEC_ID='OXYGEN', ID='O2_7',POINTS=200, TIME_HISTORY=.TRUE. / \n")
    file_object.write("&DEVC XB=7,7,1,"+str(Y)+",1.5,1.5, QUANTITY='VISIBILITY', ID='VIS_7',POINTS=200, TIME_HISTORY=.TRUE. / \n")
    file_object.write("&DEVC XB=7,7,1,"+str(Y)+",1.5,1.5, QUANTITY='TEMPERATURE', ID='TEMP_7',POINTS=200, TIME_HISTORY=.TRUE. / \n")
    file_object.write("&DEVC XYZ=7,100,1.5, QUANTITY='FED', ID='FED_7'/ \n")
    file_object.write("\n")

    file_object.write("&SLCF PBX=7, QUANTITY='TEMPERATURE'/ \n")
    file_object.write("&SLCF PBX=7, QUANTITY='VISIBILITY'/ \n\n")

    file_object.write("&DEVC XB=1.2,1.2,1,"+str(Y)+",1.5,1.5, QUANTITY='VOLUME FRACTION', SPEC_ID='CARBON MONOXIDE', ID='CO_1.2',POINTS=200, TIME_HISTORY=.TRUE. / \n") #Medición lado isquierdo correa
    file_object.write("&DEVC XB=1.2,1.2,1,"+str(Y)+",1.5,1.5, QUANTITY='VOLUME FRACTION', SPEC_ID='CARBON DIOXIDE', ID='CO2_1.2',POINTS=200, TIME_HISTORY=.TRUE. / \n")
    file_object.write("&DEVC XB=1.2,1.2,1,"+str(Y)+",1.5,1.5, QUANTITY='VOLUME FRACTION', SPEC_ID='OXYGEN', ID='O2_1.2',POINTS=200, TIME_HISTORY=.TRUE. / \n")
    file_object.write("&DEVC XB=1.2,1.2,1,"+str(Y)+",1.5,1.5, QUANTITY='VISIBILITY', ID='VIS_1.2',POINTS=200, TIME_HISTORY=.TRUE. / \n")
    file_object.write("&DEVC XB=1.2,1.2,1,"+str(Y)+",1.5,1.5, QUANTITY='TEMPERATURE', ID='TEMP_1.2',POINTS=200, TIME_HISTORY=.TRUE. / \n")
    file_object.write("&DEVC XYZ=1.2,100,1.5, QUANTITY='FED', ID='FED_1.2'/ \n")
    file_object.write("\n")

    file_object.write("&SLCF PBX=1.2, QUANTITY='TEMPERATURE'/ \n")
    file_object.write("&SLCF PBX=1.2, QUANTITY='VISIBILITY'/ \n\n")


    file_object.write("&SLCF PBZ=3, QUANTITY='VELOCITY', VECTOR=.TRUE. /  \n") #Slices sobre correa
    file_object.write("&SLCF PBX=3.5, QUANTITY='TEMPERATURE'/ \n")
    file_object.write("&SLCF PBX=3.5, QUANTITY='VISIBILITY'/ \n")
