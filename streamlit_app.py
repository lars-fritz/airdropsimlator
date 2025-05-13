import streamlit as st
import numpy as np

st.title("🐣 FLY Token Airdrop Hatch Calculator")

st.markdown("""
### 📄 Overview
Welcome to the FLY Token Airdrop calculator. Use this tool to simulate your hatching time based on your staking and trading volume.

- **1 egg = 0.1 FLY (locked)**
- **Staking > 0.5 FLY per 10 eggs** starts hatching
- Hatching completes in 26 weeks at 1 FLY per 10 eggs
- Volume boosts your effective stake

---  
""")

# Input fields
num_eggs = st.number_input("🥚 Number of Eggs", min_value=10, step=10)
staked_fly = st.number_input("💰 Staked FLY", min_value=0.0, step=0.1)
volume = st.number_input("📊 30-Day Trading Volume ($)", min_value=0.0, step=50000.0)

# Determine multiplier
if volume < 500_000:
    multiplier = 1.0
elif volume < 2_000_000:
    multiplier = 1.5
else:
    multiplier = 2.0

fly_eff = staked_fly * multiplier
alpha = fly_eff / num_eggs

st.markdown(f"**🎯 Effective FLY:** {fly_eff:.2f}")
st.markdown(f"**📈 Volume Multiplier:** {multiplier}x")
st.markdown(f"**⚖️ Alpha (FLY_eff / eggs):** {alpha:.4f}")

# Hatching formula
Ns = 26 * 7 * 24 * 60 * 60  # seconds in 26 weeks
if alpha <= 0.05:
    st.warning("Staking too low — eggs only preserved, not hatched.")
else:
    # Hatch progress estimate
    hatch_time_seconds = Ns / (20 * alpha - 1)
    hatch_weeks = hatch_time_seconds / (7 * 24 * 60 * 60)

    progress = 1 - hatch_time_seconds / Ns
    st.success(f"⏳ Estimated Hatching Time: **{hatch_weeks:.1f} weeks**")
    st.progress(min(progress, 1.0))

---

# 🐣 Tips:
- Minimum stake: **0.5 FLY / 10 eggs** to prevent rot
- Hatch starts above this threshold
""")
