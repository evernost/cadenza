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
# EXTERNALS
# =============================================================================
import numpy as np
import matplotlib.pyplot as plt



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



# =============================================================================
# SIMULATOR
# =============================================================================

def runSim() :

  nPts = round(tSim * fS)

  # Time vector
  t = np.arange(nPts) / fS

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

