import glob
import pandas as pd
import matplotlib.pyplot as plt
from pvlib import iotools

# ==========================================
# 1. RESEARCH PAPER CONSTANTS (Section 3)
# ==========================================
P_IT = 1000.0          # Active IT power load (kW)[cite: 5]
M_AIR_FLOW = 50.0      # Mass flow rate of server exhaust air (kg/s)[cite: 5]
C_P = 1.005            # Specific heat capacity of air (kJ/kg°C)[cite: 5]
T_EXHAUST = 55.0       # Hot server exhaust air temperature (°C)[cite: 5]
M_EVAP_BASE = 1800.0   # Baseline evaporative water loss rate (Liters/hour)[cite: 5]
M_AWG_MAX = 1200.0     # Maximum designed AWG capacity (Liters/hour)[cite: 5]

# Find all .epw files in the folder
epw_files = glob.glob("*.epw")

if not epw_files:
    print("No .epw files found! Check your folder directory.")
    exit()

# Loop through each location's weather file
for file_path in epw_files:
    print(f"Processing simulation for: {file_path}")
    
    # Read weather data using pvlib
    data, metadata = iotools.read_epw(file_path)
    city = metadata.get('city', 'Unknown City')
    country = metadata.get('country', 'Unknown Country')
    
    # Extract hourly ambient temperature and relative humidity from EPW
    t_ambient = data['temp_air']
    rh = data['relative_humidity']
    
    # ==========================================
    # 2. DYNAMIC THERMODYNAMIC SIMULATION[cite: 5]
    # ==========================================
    
    # Step A: Calculate Hourly Available Waste Thermal Power (Q_waste)[cite: 5]
    # Formula: Q_waste = m_air * C_p * (T_exhaust - T_ambient)[cite: 5]
    q_waste = M_AIR_FLOW * C_P * (T_EXHAUST - t_ambient)
    q_waste = q_waste.clip(lower=0)  # Q_waste cannot be negative if ambient temp spikes
    
    # Step B: Model Dynamic AWG Water Generation Rate (m_awg)[cite: 5]
    # Water generation scales with ambient Relative Humidity (RH) and available Q_waste[cite: 5]
    nominal_q_waste = M_AIR_FLOW * C_P * (T_EXHAUST - 25.0)  # Baseline Q_waste at 25°C[cite: 5]
    m_awg = M_AWG_MAX * (rh / 100.0) * (q_waste / nominal_q_waste)
    m_awg = m_awg.clip(upper=M_AWG_MAX, lower=0)  # Bound by physical system capacity[cite: 5]
    
    # Step C: Calculate Hourly Net Water Usage Effectiveness (WUE_net)[cite: 5]
    # Formula: WUE_net = (m_evap - m_awg) / P_IT[cite: 5]
    wue_net = (M_EVAP_BASE - m_awg) / P_IT
    
    # Save calculations into the dataframe for analytics
    data['Q_waste_kW'] = q_waste
    data['m_awg_L_hr'] = m_awg
    data['WUE_net'] = wue_net
    
    # ==========================================
    # 3. STATISTICAL SUMMARIES & OUTPUTS
    # ==========================================
    total_water_saved_liters = m_awg.sum()  # Cumulative sum of 8,760 hours
    avg_wue_net = wue_net.mean()
    
    print(f"\n================ SYSTEM ANALYSIS: {city.upper()}, {country.upper()} ================")
    print(f"-> Total Groundwater Saved in 1 Year : {total_water_saved_liters:,.2f} Liters")
    print(f"-> Average Operational Net WUE         : {avg_wue_net:.3f} L/kWh (Baseline: 1.80 L/kWh)[cite: 5]")
    print(f"====================================================================\n")
    
    # ==========================================
    # 4. GRAPH VISUALIZATION (First Week Comparison)
    # ==========================================
    plt.figure(figsize=(12, 5))
    wue_net.iloc[:168].plot(label=f"{city} Simulated WUE_net", color='teal', linewidth=2)
    plt.axhline(y=1.8, color='crimson', linestyle='--', label="Traditional Baseline WUE (1.8)")  #[cite: 5]
    
    plt.title(f"Hourly Net WUE Fluctuations (First Week of January) - {city}", fontsize=12, fontweight='bold')
    plt.xlabel("Hours", fontsize=10)
    plt.ylabel("WUE Value (L/kWh)", fontsize=10)
    plt.legend(loc="upper right")
    plt.grid(True, linestyle=':', alpha=0.6)

# Display all simulation windows
plt.show()