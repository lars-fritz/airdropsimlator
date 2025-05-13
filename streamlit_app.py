import streamlit as st
import numpy as np

st.set_page_config(page_title="FLY Airdrop Simulator", layout="wide")

st.title("🪂 FLY Token Airdrop Simulator")

with st.expander("📘 Full Airdrop Documentation", expanded=True):
    st.markdown("""
### Airdrop Allocation

- **500,000 FLY Tokens (Free)**
- **1,000,000 FLY Tokens (Locked)**
    - Represented by **10,000,000 Eggs**
    - Eggs must be **hatched** to unlock underlying FLY tokens
    - If unhatched, eggs rot, unless they are hatched with a minimum stake that halts the rotting

---

## 🥚 Egg Mechanics

- Each **egg = 0.1 FLY token**
- Eggs are not tradeable, but represent a **claim**
- Hatching is required to realize their value

---

## ☠️ Rotting Mechanism

- Eggs **rot linearly over 1 year** if unhatched
- Rotting occurs on a **weekly schedule**
- Rotten eggs = permanently burnt FLY

| Time Since Airdrop | % Rotten |
| --- | --- |
| 1 week | ~1.92% |
| 1 month | ~8.33% |
| 6 months | ~50% |
| 12 months | 100% |

---

## 🐣 Hatching & Staking Rules

### Hatching Conditions

- Stake **≥ 0.5 FLY per 10 eggs**: rot is halted
- Stake **> 0.5 FLY per 10 eggs**: hatching starts
- Stake **= 1 FLY per 10 eggs**: unlocks in 26 weeks

---

### ⏳ Hatching Formula

Let:

- $N_s$ = seconds in 26 weeks
- $\alpha = \frac{FLY_{eff}}{N_{eggs}}$
- $t$ = time passed

Then hatching time remaining:

$$
N(t) = N_s - 20\left(\alpha - \frac{1}{20}\right)t
$$

Progress:

$$
\text{Progress} = 1 - \frac{N(t)}{N_s}
$$

- **Effective FLY** = `Staked FLY × Volume Multiplier`

---

## 📈 Volume Multiplier

| 30-Day Trading Volume | Volume Multiplier |
| --- | --- |
| < $500,000 | 1× |
| $500,000 – $1,999,999 | 1.5× |
| ≥ $2,000,000 | 2× |

> 🔓 Higher volume = faster hatching

---

## ✅ Summary

- Claim up to **1.5M FLY**
- **10M Eggs** = locked FLY
- Stake to **stop rot** or **start hatching**
- More stake + more volume = faster unlock
""")

st.markdown("---")
st.header("🔢 Hatching Time Calculator")

# === User Inputs ===
col1, col2, col3 = st.columns(3)

with col1:
    num_eggs = st.number_input("🥚 Number of Eggs", min_value=10, step=10)

with col2:
    staked_fly = st.number_input("💰 Staked FLY", min_value=0.0, step=0.1)

with col3:
    volume = st.number_input("📊 30-Day Trading Volume ($)", min_value=0.0, step=50000.0)

# === Determine Volume Multiplier ===
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
st.markdown(f"**⚖️ Alpha (FLY_eff / eggs):** `{alpha:.4f}`")

# === Hatching Time Calculation ===
Ns = 26 * 7 * 24 * 60 * 60  # seconds in 26 weeks

if alpha <= 0.05:
    st.warning("🚫 Insufficient staking — rotting is halted but no hatching will occur.")
else:
    hatch_time_seconds = Ns / (20 * alpha - 1)
    hatch_weeks = hatch_time_seconds / (7 * 24 * 60 * 60)
    progress = 1 - hatch_time_seconds / Ns
    progress = max(0.0, min(progress, 1.0))

    st.success(f"⏳ Estimated Hatching Time: **{hatch_weeks:.1f} weeks**")
    st.progress(progress)

st.markdown("""
---

📌 **Note:**
- If you reduce your stake or lose your multiplier, hatching resets.
- Keep parameters constant to hatch at the estimated rate.
""")
