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

    

  TYPE: "pace_increase"
    Initial position      : 'd0' argument if specified (in meters), random otherwise
    Initial speed         : 'v0' argument if specified (in km/h), random otherwise (10 km/h < v0 < 40 km/h)
    Final speed           : 'vInf' argument if specified (in km/h), random otherwise (10 km/h < v0 < 40 km/h)
    Initial acceleration  : 'a0' argument if specified (in km/h/s), +10 km/h/s otherwise

    Description:
    Speed increases smoothly and settles.

    

  TYPE: "pace_decrease"
    Initial position      : 'd0' argument if specified (in meters), random otherwise
    Initial speed         : 'v0' argument if specified (in km/h), random otherwise (10 km/h < v0 < 40 km/h)
    Final speed           : 'vInf' argument if specified (in km/h), random otherwise (10 km/h < v0 < 40 km/h)
    Initial acceleration  : 'a0' argument if specified (in km/h/s), +10 km/h/s otherwise

    Description:
    Speed decreases smoothly and settles.


  All profiles accept arguments 'r1' and 'r2' that describe the 'nervosity' of the system.
  The higher the value, the higher the power and therefore acceleration capacity.

  The model uses a double exponential for the speed.
  The distance and acceleration are directly derived from it.
  """

  nPts = round(t_sim * f_s)
  t = np.arange(nPts) / f_s

  r1 = kiwiArgs.get("r1", 0.5)
  r2 = kiwiArgs.get("r2", 0.6)

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

    d = d0 + (A/r1) + (B/r2) + (C*t) - A*np.exp(-r1*t)/r1 - B*np.exp(-r2*t)/r2
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

    d = d0 + (A/r1) + (B/r2) + (C*t) - A*np.exp(-r1*t)/r1 - B*np.exp(-r2*t)/r2
    v = A*np.exp(-r1*t) + B*np.exp(-r2*t) + C
    a = -r1*A*np.exp(-r1*t) - r2*B*np.exp(-r2*t)


  return (t, d, v, a)



def odometer(t, d, diameter) :
  """
  Returns the list of time instants the odometer sensor will 'tick'.
  
  Arguments:
  - t         : time vector
  - d         : distance travelled at the time indicated by the time vector
                i.e. d[i] = travelled distance at time t = t[i]
                Distance is expressed in meters.
  - diameter  : diameter of the wheel (in inches)
  """

  N = len(t)
  ticks = [t[0]]
  p = np.pi * diameter * 2.54 / 100

  if (N == 1) :
    return ticks

  dLast = d[0]
  eMax = -1
  for n in range(N) :
    if (d[n] >= (dLast + p)) :
      
      # Interpolation (interesting for low sample rates)
      dRes = d[n] % p
      tTick = t[n] - ((t[n] - t[n-1])/(d[n] - d[n-1]))*dRes

      if (np.abs(tTick - t[n]) > eMax) :
        eMax = np.abs(tTick - t[n])

      dLast = d[n]
      ticks.append(tTick)
      
  print(f"Max error = {eMax*100} cm")

  return ticks





def estimator(t, ticks, diameter) :
  """
  Description is TODO.
  """


  
  nPts = len(t)
  d_est = np.zeros((nPts,))
  v_est = np.zeros((nPts,))
  a_est = np.zeros((nPts,))
  nTick = 1
  status = []
  for n in range(nPts) :
    
    # No estimation is available before the second tick occured.
    if (nTick == 1) :
      if (t[n] < ticks[1]) :
        d_est[n] = 0.0
        status.append("not available before second tick")
      else :
        nTick += 1
        deltaT = ticks[1] - ticks[0]
        d_est[n] = np.pi * (1 + (2*t[n]/deltaT) + (t[n]/deltaT)**2)
        
    else :
      if (t[n] < ticks[nTick]) :
        deltaT = ticks[nTick-1] - ticks[nTick-2]
        d_est[n] = np.pi * (1 + (2*t[n]/deltaT) + (t[n]/deltaT)**2)
      else :
        nTick += 1


    

  



  return (d_est, v_est, a_est, status)








# =============================================================================
# SIMULATOR
# =============================================================================

def run(f_s, t_sim) :

  # Simulate the distance, speed and acceleration from a speed profile
  (t, d, v, a) = trajectory(f_s, t_sim, type = "start_and_settle")

  # Simulate the odometer output
  ticks = odometer(t, d, diameter = 28)

  # Estimate the distance, speed and acceleration using the kernel
  (d_est, v_est, a_est) = estimator(t, ticks)



  

  # Distance
  d = 1 - np.cos(2 * np.pi * 1.1 * t) + 10 * t

  # Speed (derivative of d)
  v = 2 * np.pi * 1.1 * np.sin(2 * np.pi * 1.1 * t) + 10

  # Plot
  plt.plot(t, d, label = "distance")
  plt.plot(t, v, label = "speed")
  plt.xlabel("time")
  plt.ylabel("distance")
  plt.legend()
  plt.title('reference speed profile')
  plt.grid(True)
  plt.show()



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  f_s = 10e3
  t_sim = 20

  (t, d, v, a) = trajectory(f_s, t_sim, type = "start_and_settle")

  ticks = odometer(t, d, diameter = 28)

  # Estimate the distance, speed and acceleration using the kernel
  (d_est, v_est, a_est) = estimator(t, ticks, diameter = 28)


  plt.plot(t, d, label = "distance")
  plt.plot(t, v, label = "speed")
  plt.xlabel("time (s)")
  plt.ylabel("distance (km)")
  plt.legend()
  plt.title("reference speed profile")
  plt.grid(True)
  plt.show()
