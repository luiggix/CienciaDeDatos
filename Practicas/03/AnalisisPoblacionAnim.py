#!/usr/bin/env python
# coding: utf-8
"""
Created on Tue Apr 28 16:10:45 2020

@author: luiggi
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
#
# El módulo utils contiene las funciones que se usarán en esta práctica.
#
from utils import maxminTicks, inicializaGrafica, graficaFR, graficaFR_Pais
#
# Para la animación necesitamos: FuncAnimation
# y writers es para guardar la animación en un archivo.
#
from matplotlib.animation import FuncAnimation, writers
#
# Función que se usa para modificar los valores de la curva que se va a animar.
#
def dibuja(i, ax, linea, linea_glow, texto, x, y):
    """
    Modifica los valores de la curva que se va a animar.
    
    También modifica los títulos y algunos textos que se ponen sobre la gráfica.

    Parameters
    ----------
    i : int
        Indica el cuadro en el que va la animación.
    ax : Axes
        Ejes de la gráfica.
    linea : Line2D
        Línea base de la curva del país que se va a animar.
    linea_glow : Line2D
        Línea para el glow de la curva del país que se va a animar.
    texto : Annotation
        Texto sobre la curva.
    x : Serie
        Datos de los años.
    y : Serie
        Datos de la fertilidad.
    """
    #
    # Este límite permite definir hasta que punto se dibuja la curva.
    #
    limit = 14 - (i + 1)
    #
    # Se actualizan los datos de las curvas, la base y el glow.
    #
    linea.set_data(x[limit:14], y[limit:14])
    linea_glow.set_data(x[limit:14], y[limit:14])
    #
    # Se actualiza el título de la gráfica con la info de los años.
    #
    title_graf = x.iloc[limit]
    ax.set_title(title_graf)
    #
    # Se actualiza el texto que va sobre la curva.
    #
    xt = x.iloc[limit]
    yt = y.iloc[limit]
    texto.set_position( (xt,yt) )
    texto.set_text('México {:3.2f}'.format(y.iloc[limit]))
    
#
# Cambiamos el estilo de los gráficos:
#
#plt.style.use("seaborn-white")
plt.style.use('Solarize_Light2')

#
# Obtenemos la información, que es la misma de la práctica 1.
#
FR = pd.read_csv('../01/UNdata_Export_20211021_200853345.zip')
#
# Se agrupa por país 
#
paises = FR.groupby('Country or Area')
#
# Calculamos el máximo en el eje `y` para definir los `yticks`.
#
p_max, y_max, p_min, y_min, yticks = maxminTicks(FR)
print('Máximo = {}, \t País : {}'.format(y_max, p_max))
print('Mínimo = {}, \t País : {}'.format(y_min, p_min))
print('yticks : {}'.format(yticks))
#
# Hacemos la gráfica base
#
fig, ejes = inicializaGrafica(y_max, yticks)
graficaFR(paises, {'lw':0.5, 'c':'#AAAAAA'})
#
# Definimos un conjunto de países a ser graficados y sus colores correspondientes. 
# 
paises_colores = {
    p_max                      : 'red',      
    'United States of America' : 'mediumblue',
    'Japan'                    : mcolors.TABLEAU_COLORS['tab:green'],
    'Germany'                  : 'maroon',
    p_min                      : '#0099FF',
    'Egypt'                    : 'darkorange',
    'Argentina'                : 'darkviolet',
    'Nigeria'                  : 'forestgreen',
    'World'                    : mcolors.BASE_COLORS['k']
}
#
# Realizamos las gráficas de los países elegidos.
#
for p, c in paises_colores.items():
    par = {'lw':2.0, 'c':c, 'marker':''}
    graficaFR_Pais(paises, p, 0, par)
#
# Dibujamos el primer dato de México
#
mex_color = '#002241'                         # Color
par = {'lw':3.0, 'c':mex_color, 'marker':'o'} # Parámetro de la curva
par_glow = {'alpha':0.4, 'c':mex_color}       # Parámetros para el 'glow'
#
# Se hace la gráfica de México desde el lugar 13 hasta el 14.
# En l, lg y t1 tendremos la líneas y el texto que se modificarán durante
# la animación.
#
l, lg, t1 = graficaFR_Pais(paises, 'Mexico', 13, par, par_glow, 3) 
#
# Definimos el país a animar y realizamos la animación
#
mexico = paises.get_group('Mexico')

anim = FuncAnimation(fig,     # La figura donde se hace la animación
                      dibuja,  # la función que actualiza la info que se dibuja
                      fargs=(ejes, l, lg, t1,   # Argumentos para la función
                            mexico['Year(s)'], # dibuja()
                            mexico['Value'], ),
                      interval=500,  # Tiempo en milisegundos entre cada cuadro.
                      frames=14,     # Número de iteraciones (Cuadros)
                      repeat=True)   # Permite poner la animación en un ciclo 

# Lo siguiente es para guardar la animación en un archivo en formato MP4.

Writer = writers['ffmpeg']
writer = Writer(fps=3, metadata=dict(artist='Me'), bitrate=1800)
anim.save('fert.mp4', writer=writer)

# También es posible guardar el video en un GIF como sigue

anim.save('fert.gif', writer='imagemagick', fps=3)

plt.show()
