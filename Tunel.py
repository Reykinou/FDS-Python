#!/usr/bin/python3

#Codelco - Nuevo Nivel Mina

#--------------------------------INPUTS-----------------------------------------

                            #Geometría del Túnel

X=9.4 #ancho tunel
Y=80.0 #largo del tunel
Z=6.0 #altura tunel
cx=0.2 #tamaño celda en x
cy=0.3 #tamaño celda en y
cz=0.2 #tamaño celda en z

#Curva para dibujar tunel - interpolación Excel con geometría AutoCad

def f(x):
    return -1*0.00037731654713724100*x**6 + 0.01064032662972640000*x**5 - 0.12023951690048300000*x**4 + 0.69353748265166400000*x**3 - 2.25803586101028000000*x**2 + 4.43075769525603000000*x**1 + 0.00018151820924572300

                            #Inputs Correa

b = 2 #ancho de correa
h = 1.3 #altura de la correa
x_correa = 2.5 #distancia desde pared del tunel

                            #Incendio de diseño (nada aún)

vel_viento = 2.0
spread_rate = 0.02

#----------------------------CÁLCULOS PREVIOS-----------------------------------
#Cálculos varios

n_x=X/cx #numero de celdas en X
n_y=Y/cy #numero de celdas en Y
n_z=Z/cz #numero de celdas en Z



#-----------------------------EDITOR FDS----------------------------------------
Tunel = 'Tunel3.fds'
with open(Tunel,'w') as file_object:

    file_object.write("&HEAD CHID='Tunel', TITLE='Tunel'/ \n")
    file_object.write("\n")

    file_object.write("&MESH IJK="+str(n_x)+","+str(n_y)+","+str(n_z)+", XB=0.0"+","+str(X)+",0.0,"+str(Y)+",0.0,"+str(Z)+"/ \n")
    file_object.write("\n")

    file_object.write("&TIME T_END=0. / \n")
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
    file_object.write("&OBST XB=0,0,0,"+str(Y)+"0,"+str(Z)+" SURF_ID='CONCRETE SURFACE'/ \n")
    file_object.write("&OBST XB=9.4,9.4,0,"+str(Y)+"0,"+str(Z)+" SURF_ID='CONCRETE SURFACE'/ \n")
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

    # file_object.write("\n")
    # file_object.write("&WIND V0=8.0/ \n") #VIENTO - NO SÉ SI DEFINIRLO ASÍ

    file_object.write("\n")
    file_object.write("&SURF ID = 'CONCRETE SURFACE', MATL_ID = 'CONCRETE', RGB = 128,128,128, THICKNESS = 0.4/ \n")
    file_object.write("&MATL ID = 'CONCRETE', SPECIFIC_HEAT = 0.88, DENSITY = 2100., CONDUCTIVITY = 1.0 / \n")
    file_object.write("\n")

                #INCENDIO SOLO PARA PROBAR - NO ES EL DE DISEÑO

    file_object.write("&VENT XB=2.5,4.5,5.0,30.0,1.3,1.3 SURF_ID='FIRE' / \n") #Área de 2x2 sbre la correa
    file_object.write("&REAC FUEL = 'PROPANE', SOOT_YIELD = 0.15, CO_YIELD = 0.06, HEAT_OF_COMBUSTION = 30000. / \n")
    file_object.write("&SPEC ID='PROPANE', MASS_EXTINCTION_COEFFICIENT = 8700. / \n")
    file_object.write("&SURF ID = 'FIRE', HRRPUA =500./, XYZ=3.5,5.0,1.3, SPREAD_RATE = "+str(spread_rate)+" \n")
    file_object.write("\n")

    i=1
    while i<=Y:
        file_object.write("&DEVC ID='HD"+str(i)+"', XYZ=4.7,"+str(i)+",5.9, PROP_ID='Acme Heat', / \n")
        i+=1

    file_object.write("&PROP ID='Acme Heat', QUANTITY='LINK TEMPERATURE', RTI=50., ACTIVATION_TEMPERATURE=74. / \n") #heat detectors
    file_object.write("\n")
    file_object.write("&SLCF PBX=4.7, QUANTITY='TEMPERATURE'/ \n") #Slice mitad del túnel
