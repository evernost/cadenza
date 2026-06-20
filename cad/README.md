# Cadenza project

A bike tachometer with reactive display.

---

## Overview

- **Type:** 
- **Domain:** Digital
- **Status:** Work in progress

---

## Features
This is an attempt to make a bike tachometer with a display providing a much better FPS compared to most tachometers you can find. 
Most of them are incredibly sluggish for reasons that are beyond me.

---

## Interfaces

### Inputs
| Name | Type | Range | Description |
|-----|------|-------|-------------|


### Outputs
| Name | Type | Description |
|------|------|-------------|
| OUT | Audio | Filtered signal |

---

## Controls

| Control | Type | Description |
|--------|------|-------------|
| Cutoff | Potentiometer | Manual cutoff frequency |
| Resonance | Potentiometer | Feedback amount |

---

## Electrical Characteristics

- **Supply voltage:** ±12V
- **Current consumption:** TBD mA
- **Signal levels:** TBD

---

## Implementation Notes
Section is TODO.


---

## Files

| File                          | Description                       |
|-------------------------------|-----------------------------------|
| `playLight_rev_A.pdf`         | Electrical schematic (PDF export) |
| `playLight_rev_A.kicad_sch`   | Schematic (KiCad 9.0.7)           |
| `playLight_rev_A.kicad_pcb`   | PCB layout (KiCad 9.0.7)          |
| `/production`                 | Production files (Gerbers + .zip) |

---

## Calibration / Tuning
None.

---

## Known Issues / TODO
None.

---

## Revision History

| Revision | Date | Notes |
|--------|------|-------|
| Rev A | 2026-06-20 | Initial prototype without USB support |
| Rev B | YYYY-MM-DD | Second version with USB logging |

---

## Tools
Designed with KiCAD 9.0.7

Grid dimensions

|Name | Size | Description|
|--------|------|-------|
| Grid 1 | 0.25 mm | PCB outline |
| Grid 2 | 50 mil | parts placement |
| Grid 3 | 10 mil | routing |

---

## Related Modules
None.


---

## References
| Part type          | Reference                                                                                          | Selection criteria          |
|--------------------|----------------------------------------------------------------------------------------------------| ------------------ |
| LED driver         | TLC591 (TI)                                                                                        | Available in KiCAD<br>At least 8 outputs<br>Daisy-chain support |
| 7 segments display | HDSP-A401 (orange variant)<br>HDSP-7501 (red variant, high efficiency)<br>HDSP-7801 (green variant)| Available in KiCAD<br> Bright enough for outside readbility|
| MCU                | STM32F098                                                                                          | USB OTG (for flash drive support)<br>Low pin count (for size)<br>3.3V supply|