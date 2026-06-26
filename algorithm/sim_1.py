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



def trajectory(fS, tSim, profile = "start_and_settle", **kiwiArgs) :
  """
  Simulates the distance, speed and acceleration of a certain 
  trajectory using a profile descriptor:
  
  TYPE: "start_and_settle"
    Initial position      : 0
    Initial speed         : 0
    Initial acceleration  : 0
  
    Description:
    Speed increases and settles exponentially to a maximum speed.

  TYPE: "brake"
    Initial position      : 'd0' argument if specified, random otherwise
    Initial speed         : 'v0' argument if specified, random otherwise (10 km/h < v0 < 40 km/h)
    Initial acceleration  : 'a0' argument if specified, -50 km/h/s otherwise

    Description:
    Speed drops exponentially from some initial speed to 0.

  """

  nPts = round(tSim * fS)
  t = np.arange(nPts) / fS

  # ---------------------------------------------------------------------------
  # PROFILE: START_AND_SETTLE
  # ---------------------------------------------------------------------------
  if (profile.lower() == "start_and_settle") :

    if ("v0" not in kiwiArgs) :
      v0 = random.uniform(10, 40)/3.6

    if ("a0" not in kiwiArgs) :
      a0 = -50.0/3.6


  d = 0
  v = 0
  a = 0

  return (t, d, v, a)



# =============================================================================
# SIMULATOR
# =============================================================================

def run() :

  # Simulate the distance, speed and acceleration from a speed profile
  (t, d, v, a) = trajectory(fS, tSim, type = "high_settle")

  # Simulate the odometer output
  ticks = odometer(t, d)

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

