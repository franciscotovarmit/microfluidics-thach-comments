
#######################################
# Resistance

import numpy as np
import math


def calculate_resistance_diam_hyd(L,W,H):
    # L: Length of channel
    # W: width of channel (design)
    # H: height given by Photoresist
    #-------------------
    #     8   mu  L
    # R =---------------
    #      Pi   R^4
    #------------------
    mu = 8.9e-4 #viscosity #Pa s  #water
    Area = W*H  #length * width
    Perimeter = 2*(W+H)
    dH =  4* Area / Perimeter    #hydraulic diam
    R = 0.5*dH
    Resistance = 8*mu*L/(math.pi*math.pow(R,4))
    return Resistance


def calculate_resistance(L,W,H):
    # L: Length of channel
    # W: width of channel (design)
    # H: height given by Photoresist
    #-------------------
    #     12   mu  L
    # R =---------------
    #      W H^3 * (1-0.63 H/W)
    #------------------
    mu = 8.9e-4 #viscosity #Pa s  #water
    Resistance = 12*mu*L/(W*math.pow(H,3)*(1-0.63*H/W))
    return Resistance

def convertFlowRateuLminTom3s(Q):
    Q = Q/(60*1e9)
    return Q

def convertFlowRatem3sTouLmin(Q):
    Q = Q*(60*1e9)
    return Q

def calculate_pressure_drop(Res,Q=1.666667e-10):
    #Q=1.666667e-10   m3/s   10uL/min
    PressureDrop = Res*Q
    return PressureDrop

def velocityCFD(Q,width, height):
    Area = width*height  #length * width
    Perimeter = 2*(width+height)
    dH =  4* Area / Perimeter    #hydraulic diam
    Ah =  0.25*math.pi*pow(dH,2)  # hydraulic area
    #velocity = Q/(Ah)
    velocity = Q/(Area)
    return velocity

if __name__ == "__main__":
    print "This is not the main file. Run 'execute.py' in the same folder"
    #from microfluidics_ipkiss3.technology import *
    length = 1000e-6
    width =  100e-6
    height =  20e-6
    QuLmin = 10
    Q =convertFlowRateuLminTom3s(QuLmin)
    Qm3s = convertFlowRatem3sTouLmin(1.66666658246e-10) #(3.81971844122e-10)

    vel = velocityCFD(Q,width, height)
    R = calculate_resistance(length,width, height)
    P = calculate_pressure_drop(R,Q)
    print 'Q', Q
    print 'vel: ', vel
    print 'Pressure drop', P
    print 'Resistance', R
    print 'Qm3s', Qm3s