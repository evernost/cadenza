# -*- coding: utf-8 -*-
# =============================================================================
# Project       : cadenza
# Module name   : -
# File name     : sim_1.py
# File type     : Python script (Python 3)
# Purpose       : simulation of the speed estimator
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Wednesday, 24 June 2026 (under heatwave, 36C at 23:30)
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# DESCRIPTION
# =============================================================================
# This script:
# - simulates a bike travelling with a given speed profile, 
# - derives the travelled distance 
# - derives the odometer sensor output
# - simulates the speed estimator from that output
# - compares the speed estimator output from the ground truth.



# =============================================================================
# EXTERNALS
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt
import random



# =============================================================================
# SETTINGS
# =============================================================================

# Diameter of the wheel (in inches)
D = 28

# Simulation time
tSim = 10.0
fS = 10e3



# =============================================================================
# KERNEL MODEL
# =============================================================================

def kernel(dt, speed) :
  """
  A kernel is the interpolating function used to model the distance between
  2 acquistion 'tops' from the wheel.
  """

  return 0



def trajectory(f_s, t_sim, profile = "start_and_settle", **kiwiArgs) :
  """
  Simulates the distance, speed and acceleration of a certain 
  trajectory using a profile descriptor:
  
  TYPE: "start_and_settle"
    Initial position      : 'd0' argument if specified (in meters), random otherwise
    Initial speed         : 0 km/h
    Final speed           : 'vInf' argument if specified (in km/h), random otherwise (10 km/h < v0 < 40 km/h)
    Initial acceleration  : 'a0' argument if specified (in km/h/s), 0 km/h/s otherwise
  
    Description:
    Speed increases and settles exponentially to a maximum speed.

  TYPE: "brake"
    Initial position      : 'd0' argument if specified (in meters), random otherwise
    Initial speed         : 'v0' argument if specified (in km/h), random otherwise (10 km/h < v0 < 40 km/h)
    Initial acceleration  : 'a0' argument if specified (in km/h/s), -10 km/h/s otherwise

    Description:
    Speed drops exponentially from some initial speed to 0.

  TYPE: "acceleration"
    Initial position      : 'd0' argument if specified (in meters), random otherwise
    Initial speed         : 'v0' argument if specified (in km/h), random otherwise (10 km/h < v0 < 40 km/h)
    Final speed           : 'vInf' argument if specified (in km/h), random otherwise (10 km/h < v0 < 40 km/h)
    Initial acceleration  : 'a0' argument if specified (in km/h/s), +10 km/h/s otherwise

    Description:
    Speed drops exponentially from some initial speed to 0.


  All profiles accept arguments 'r1' and 'r2' that describe the 'nervosity' of the system.
  The higher the value, the higher the power and therefore acceleration capacity.

  The model uses a double exponential for the speed.
  The distance and acceleration are directly derived from it.
  """

  nPts = round(t_sim * f_s)
  t = np.arange(nPts) / f_s

  r1 = kiwiArgs.get("r1", 2.0)
  r2 = kiwiArgs.get("r2", 3.0)

  # ---------------------------------------------------------------------------
  # PROFILE: START_AND_SETTLE
  # ---------------------------------------------------------------------------
  if (profile.lower() == "start_and_settle") :

    d0    = kiwiArgs.get("d0",    0.0)
    v0    = kiwiArgs.get("v0",    0.0)/3.6
    vLim  = kiwiArgs.get("vLim",  random.uniform(10, 40))/3.6
    a0    = kiwiArgs.get("a0",    0.0)/3.6

    A =  (r2*(vLim - v0) - a0)/(r1 - r2)
    B = -(r1*(vLim - v0) + a0)/(r1 - r2)
    C = vLim

    d = d0 + (C*t) - A*np.exp(-r1*t)/r1 - B*np.exp(-r2*t)/r2
    v = A*np.exp(-r1*t) + B*np.exp(-r2*t) + C
    a = -r1*A*np.exp(-r1*t) - r2*B*np.exp(-r2*t)



  # ---------------------------------------------------------------------------
  # PROFILE: BRAKE
  # ---------------------------------------------------------------------------
  elif (profile.lower() == "brake") :

    d0    = kiwiArgs.get("d0",    random.uniform(0, 1000))
    v0    = kiwiArgs.get("v0",    random.uniform(10, 40))/3.6
    vLim  = kiwiArgs.get("vLim",  0.0)/3.6
    a0    = kiwiArgs.get("a0",    -10.0)/3.6

    A =  (r2*(vLim - v0) - a0)/(r1 - r2)
    B = -(r1*(vLim - v0) + a0)/(r1 - r2)
    C = vLim

    d = d0 + (C*t) - A*np.exp(-r1*t)/r1 - B*np.exp(-r2*t)/r2
    v = A*np.exp(-r1*t) + B*np.exp(-r2*t) + C
    a = -r1*A*np.exp(-r1*t) - r2*B*np.exp(-r2*t)


  return (t, d, v, a)



# =============================================================================
# SIMULATOR
# =============================================================================

def run(f_s, t_sim) :

  # Simulate the distance, speed and acceleration from a speed profile
  (t, d, v, a) = trajectory(f_s, t_sim, type = "start_and_settle")

  # Simulate the odometer output
  ticks = odometer(t, d, diameter = 28)

  # Estimate the distance, speed and acceleration using the kernel
  (dEst, vEst, aEst) = estimator(t, ticks, d)



  

  # Distance
  d = 1 - np.cos(2 * np.pi * 1.1 * t) + 10 * t

  # Speed (derivative of d)
  v = 2 * np.pi * 1.1 * np.sin(2 * np.pi * 1.1 * t) + 10

  # Plot
  plt.plot(t, d, label='distance')
  plt.plot(t, v, label='speed')
  plt.xlabel('time')
  plt.ylabel('distance')
  plt.legend()
  plt.title('reference speed profile')
  plt.grid(True)
  plt.show()



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  f_s = 100e3
  t_sim = 20

  (t, d, v, a) = trajectory(f_s, t_sim, type = "start_and_settle")

  plt.plot(t, d, label = 'distance')
  plt.plot(t, v, label = 'speed')
  plt.xlabel("time (s)")
  plt.ylabel("distance (km)")
  plt.legend()
  plt.title("reference speed profile")
  plt.grid(True)
  plt.show()
