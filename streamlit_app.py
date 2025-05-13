import streamlit as st
import datetime
import math

# Constants
EGGS_TOTAL = 10_000_000
FLY_PER_EGG = 0.1
SECONDS_IN_26_WEEKS = 26 * 7 * 24 * 3600

# Volume multiplier tiers
def get_multiplier(volume):
    if volume < 500_000:
        return 1.0
    elif volume < 2_000_000:
        return 1.5
    else:
        return 2.0

st.title("🥚 FLY Token Airdrop Hatch Simulator")

st.markdown("""
Welcome to the **FLY Airdrop Hatch App**!  
Use the sliders and inputs below to simulate your hatching progress.

---

### 🔢 Input Your Parameters
""")

# User inputs
staked_fly = st.number_input("🪙 Staked FLY", min_value=0.0, value=0.0, step=0.1)
num_eggs = st.number_input("🥚 Number of Eggs", min_value=0, value=1000, step=100)
volume = st.number_input("📈 30-Day Trading Volume ($)", min_value=0.0, value=0.0, step=1000.0)
start_date = st.date_input("📅 Airdrop Start Date", value=datetime.date.today())

# Calculations
multiplier = get_multiplier(volume)
effective_fly = staked_fly * multiplier
alpha = effective_fly / num_eggs if num_eggs > 0 else 0
hatching_active = alpha > 0.05  # equivalent to 0.5 FLY per 10 eggs

# Display effective values
st.markdown(f"""
- 💥 **Volume Multiplier**: `{multiplier}×`  
- 🧮 **Effective FLY**: `{effective_fly:.2f}`  
- 🧪 **FLY per 10 eggs**: `{(effective_fly / num_eggs) * 10 if num_eggs > 0 else 0:.2f}`
""")

# Compute time since airdrop
today = datetime.date.today()
time_since_start = (today - start_date).total_seconds()

if not hatching_active:
    st.warning("⚠️ Minimum threshold not met: eggs are **rotting** but not hatching.")
    rotting_percent = min(100, (time_since_start / (365 * 24 * 3600)) * 100)
    st.markdown(f"💀 **Rotting Progress**: `{rotting_percent:.2f}%` of your eggs may have rotted.")
else:
    # Hatching is active
    progress = (20 * (alpha - 1/20) * time_since_start) / SECONDS_IN_26_WEEKS
    progress = min(1.0, max(0.0, progress))  # Clamp between 0 and 1
    time_remaining_seconds = (1 - progress) * SECONDS_IN
