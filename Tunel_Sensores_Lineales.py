#!/usr/bin/python3

#Codelco - Nuevo Nivel Mina

#--------------------------------INPUTS-----------------------------------------

                            #Geometría del Túnel

X=9.4 #ancho tunel
Y=5 #largo del tunel
Z=4.8 #altura tunel
cx=0.1 #tamaño celda en x
cy=0.1 #tamaño celda en y
cz=0.1 #tamaño celda en z

#Curva para dibujar tunel - interpolación Excel con geometría AutoCad

def f(x):
    return -1*0.00037731654713724100*x**6 + 0.01064032662972640000*x**5 - 0.12023951690048300000*x**4 + 0.69353748265166400000*x**3 - 2.25803586101028000000*x**2 + 4.43075769525603000000*x**1 + 0.00018151820924572300

                            #Inputs Correa

b = 2 #ancho de correa
h = 0.1 #altura de la correa
x_correa = 2.5 #distancia desde pared del tunel

                            #Incendio de diseño (nada aún)

vel_viento = 2.0
spread_rate = 0.02

#----------------------------CÁLCULOS PREVIOS-----------------------------------
#Cálculos varios

n_x1=8 #numero de celdas en X malla 1
n_y1=25 #numero de celdas en Y malla 1
n_z1=5 #numero de celdas en Z malla 1
n_x2=80 #numero de celdas en X malla 2
n_y2=100 #numero de celdas en Y malla 2
n_z2=20 #numero de celdas en Z malla 2
n_x3=19 #numero de celdas en X malla 3
n_y3=25 #numero de celdas en Y malla 3
n_z3=5 #numero de celdas en Z malla 3
n_x4=47 #numero de celdas en X malla 4
n_y4=25 #numero de celdas en Y malla 4
n_z4=19 #numero de celdas en Z malla 4



#-----------------------------EDITOR FDS----------------------------------------
Tunel = 'Tunel3.fds'
with open(Tunel,'w') as file_object:

    file_object.write("&HEAD CHID='Tunel', TITLE='Tunel'/ \n")
    file_object.write("\n")

    file_object.write("&MESH IJK="+str(n_x1)+","+str(n_y1)+","+str(n_z1)+", XB=0.0,1.6,0.0,5,0,1/ \n")
    file_object.write("&MESH IJK="+str(n_x2)+","+str(n_y2)+","+str(n_z2)+", XB=1.6,5.6,0.0,5,0,1/ \n")
    file_object.write("&MESH IJK="+str(n_x3)+","+str(n_y3)+","+str(n_z3)+", XB=5.6,9.4,0.0,5,0,1/ \n")
    file_object.write("&MESH IJK="+str(n_x4)+","+str(n_y4)+","+str(n_z4)+", XB=0,9.4,0.0,5,1,4.8/ \n")

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
    file_object.write("&OBST XB="+str(x_correa)+","+str(x_correa+b)+",0,"+str(Y)+",0,0.1 / \n") #Obstaculo para correa
    file_object.write("\n")

    n=1
    dx=cx
    while n<=94:
        file_object.write("&OBST XB="+str((n-1)*dx)+","+str(n*dx)+",0,"+str(Y)+","+str(0.2+f(n*dx))+",4.8 SURF_ID='CONCRETE SURFACE' / \n") #Para dibujar forma del túnel
        n+=1

    file_object.write("\n")
    file_object.write("&SURF ID = 'CONCRETE SURFACE', MATL_ID = 'CONCRETE', RGB = 128,128,128, THICKNESS = 0.4/ \n")
    file_object.write("&MATL ID = 'CONCRETE', SPECIFIC_HEAT = 0.88, DENSITY = 2100., CONDUCTIVITY = 1.0 / \n")
    file_object.write("\n")

                #INCENDIO DE DISEÑO

    file_object.write("&VENT XB=2.5,2.7,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=2.6,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("&VENT XB=2.7,2.9,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=2.8,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("&VENT XB=2.9,3.1,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=3.0,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("&VENT XB=3.1,3.3,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=3.2,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("&VENT XB=3.3,3.5,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=3.4,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("&VENT XB=3.5,3.7,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=3.6,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("&VENT XB=3.7,3.9,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=3.8,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("&VENT XB=3.9,4.1,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=4.0,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("&VENT XB=4.1,4.3,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=4.2,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("&VENT XB=4.3,4.5,5,30,0.1,0.1 SURF_ID='FIRE', XYZ=4.4,5.0,0.1, SPREAD_RATE = 0.02 /   \n")
    file_object.write("\n")

    file_object.write("&REAC FUEL = 'PROPANE', SOOT_YIELD = 0.15, CO_YIELD = 0.06, HEAT_OF_COMBUSTION = 30000. /  \n")
    file_object.write("&SPEC ID='PROPANE', MASS_EXTINCTION_COEFFICIENT = 8700. / \n")
    file_object.write("&SURF ID = 'FIRE', HRRPUA =500., / \n")
    file_object.write("\n")

                #DEVICES

    i=1
    div = Y/cy
    while i<=div:
        file_object.write("&DEVC ID='HD"+str(i)+"', XYZ="+str(x_correa)+","+str(i*(0.1))+",0.2, PROP_ID='Acme Heat', / \n")
        i+=1

    j=1
    div = Y/cy
    while j<=div:
        file_object.write("&DEVC ID='HD"+str(j)+"', XYZ="+str(x_correa+b)+","+str(j*(0.1))+",0.2, PROP_ID='Acme Heat', / \n")
        j+=1

    file_object.write("&PROP ID='Acme Heat', QUANTITY='LINK TEMPERATURE', RTI=66., ACTIVATION_TEMPERATURE=68. / \n") #heat detectors
    file_object.write("\n")
    file_object.write("&SLCF PBX=4.7, QUANTITY='TEMPERATURE'/ \n") #Slice mitad del túnel
