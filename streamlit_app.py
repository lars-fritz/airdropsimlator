import streamlit as st
import numpy as np
from math import tanh

st.set_page_config(page_title="FLY Airdrop Simulator", layout="wide")

st.title("🪂 FLY Token Airdrop Simulator")

# === Simple Airdrop Overview ===
st.markdown("""
### 🎁 Airdrop Overview
Claim up to **1.5M FLY tokens** via airdrop:
- **500,000 FLY (free)**
- **1,000,000 FLY (locked)** represented by **1,000,000 eggs**
- Eggs must be **hatched** by staking FLY or they **rot over time**
""")

st.divider()

# === Hatching Time Calculator ===
st.header("🔢 Hatch Time Calculator")

# === Inputs ===
col1, col2, col3 = st.columns(3)

with col1:
    num_eggs = st.number_input("🥚 Number of Eggs", min_value=10, step=10)

with col2:
    staked_fly = st.number_input("💰 Staked FLY", min_value=0.0, step=0.1)

with col3:
    volume = st.number_input("📊 30-Day Trading Volume ($)", min_value=0.0, step=50000.0)

# === Multiplier ===
if volume < 500_000:
    multiplier = 1.0
elif volume < 2_000_000:
    multiplier = 1.5
else:
    multiplier = 2.0

fly_eff = staked_fly * multiplier
alpha = fly_eff / num_eggs if num_eggs > 0 else 0
st.markdown(f"**🎯 Effective FLY:** `{fly_eff:.2f}`")
st.markdown(f"**📈 Volume Multiplier:** `{multiplier}x`")
st.markdown(f"**⚖️ Stake-to-Egg Ratio:** `{alpha:.4f}`")

# === Hatch Time Calculation ===
Ns = 26 * 7 * 24 * 60 * 60  # seconds in 26 weeks

if fly_eff / num_eggs < 0.1:
    st.warning("🚫 Staking too low — eggs are rotting.")
else:
    hatch_time_seconds = (1+1/7*alpha)/(4/7*alpha)*Ns 
    hatch_weeks = hatch_time_seconds / (7 * 24 * 60 * 60)
    progress = 1 - hatch_time_seconds / Ns
    progress = max(0.0, min(progress, 1.0))

    st.success(f"⏳ Estimated Hatching Time: **{hatch_weeks:.1f} weeks**")
    st.progress(progress)

st.markdown("""
ℹ️ **Note:** Hatching only starts if stake > 1 FLY per 1 egg. 
""")

st.divider()

# === Full Documentation Below ===
with st.expander("📘 Full Airdrop Documentation"):
    st.markdown("""
### 🧾 Airdrop Allocation
- **500,000 FLY Tokens (Free)**
- **1,000,000 FLY Tokens (Locked)**
  - Represented by **1,000,000 Eggs**
  - Eggs must be hatched to claim underlying tokens
  - Without action, eggs **rot** and value is lost

---

### 🥚 Egg Basics
- **1 egg = 1 FLY token**
- Eggs are non-tradeable placeholders for locked FLY
- Eggs rot unless preserved or hatched by staking

---

### 🧟 Rotting Timeline

| Time Since Airdrop | % Rotten |
|--------------------|----------|
| 1 week             | ~25%   |
| 2 weeks            | ~50%%   |
| 3 weeks           | ~75%     |
| 4 weeks          | 100%     |

---

### 🐣 Staking to Hatch

- **1 FLY per 1 egg**: begins hatching, hatches in 52 weeks
- **2 FLY per 10 eggs**: fully hatched in 29 weeks
- **3 The minimal hatching time is 4 weeks
- Hatching happens **continuously** over time and so do unlocks

---

### 🚀 Volume-Based Boosting

Your **30-day trading volume** boosts your hatching speed:

| Volume ($)           | Multiplier |
|----------------------|------------|
| < $500,000           | 1×         |
| $500k – $1.99M       | 1.5×       |
| ≥ $2M                | 2×         |

> 🔓 Higher trading = faster hatching

---

### ✅ Summary

- **Claim up to 1.5M FLY** (500k free + 1M locked)
- **Stake FLY** to stop eggs from rotting or begin hatching
- **Boost with volume** to hatch faster
""")
