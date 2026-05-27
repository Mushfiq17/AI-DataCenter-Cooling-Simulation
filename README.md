Mushfiq17
# AI Data Center Cooling Simulation: Mitigating Aquifer Depletion

This repository contains the Python-based simulation framework developed for the research paper: 
**"Mitigating Aquifer Depletion in Artificial Intelligence Infrastructure: A Comprehensive Research Framework"**.

**Author:** Mushfiq Shahriar  
**Student ID:** 242311061  
**Target:** Faculty Supervisor & Academic Peer Review  

---

## 📌 Project Overview
The exponential growth of Artificial Intelligence (AI) infrastructure has created an unprecedented environmental challenge: hyperscale data centers are consuming freshwater aquifers at a rate that threatens regional water security. This computational study models and simulates two sustainable alternatives to eliminate or mitigate aquifer depletion:
1. **Baseline Model:** Traditional Evaporative Cooling Systems.
2. **Solution A:** Waste-Heat Driven Atmospheric Water Generation (AWG) operating under varying climate profiles.
3. **Solution B:** Supercritical Carbon Dioxide ($sCO_2$) Closed-Loop Waterless Cooling.

Using standard thermodynamic libraries, this simulation framework validates system performance, climate-dependency, and the specific heat capacity ($C_p$) spike of $sCO_2$.

---

## 🛠️ Software Stack & Dependencies
The simulation is fully implemented as a Jupyter Notebook (`simulation.ipynb`) using Python. It relies on the following scientific and thermodynamic libraries:

* **CoolProp:** Used to calculate the real-time thermophysical properties of Supercritical Carbon Dioxide ($CO_2$) across varying pressure and temperature thresholds.
* **PsychroLib:** Utilized for psychrometric calculations to estimate moisture harvesting potentials based on ambient temperature and relative humidity.
* **Pandas & NumPy:** Applied for managing simulation arrays, baseline calculations, and 10-year operational forecasting data.
* **Matplotlib:** Used for generating high-resolution engineering and comparative plots for the manuscript.

---

## 🚀 How to Run the Simulation Locally

### 1. Clone the Repository
Open your terminal or command prompt and execute:
```bash
git clone [https://github.com/Mushfiq17/AI-DataCenter-Cooling-Simulation.git](https://github.com/Mushfiq17/AI-DataCenter-Cooling-Simulation.git)
cd AI-DataCenter-Cooling-Simulation
