"""Generate sample PD, LGD, and EAD files from UCI_Credit_Card.csv for ECL demo."""
import numpy as np
import pandas as pd

np.random.seed(42)

SOURCE = "UCI_Credit_Card.csv"
SAMPLE_SIZE = 500

df = pd.read_csv(SOURCE)
df = df.sample(n=SAMPLE_SIZE, random_state=42).reset_index(drop=True)

pay_cols = ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]
delinquency = df[pay_cols].clip(lower=0).mean(axis=1)

# PD: logistic transform of delinquency history + historical default flag, plus noise
logit = -2.2 + 0.9 * delinquency + 1.1 * df["default.payment.next.month"]
logit += np.random.normal(0, 0.3, size=len(df))
pd_values = 1 / (1 + np.exp(-logit))
pd_values = pd_values.clip(0.01, 0.95).round(4)

# LGD: beta-distributed around a typical unsecured retail-credit mean (~60%)
lgd_values = np.random.beta(a=6, b=4, size=len(df))
lgd_values = lgd_values.clip(0.10, 0.95).round(4)

# EAD: current utilization of the credit limit (latest bill amount, floored at 0, capped at limit)
ead_values = df["BILL_AMT1"].clip(lower=0)
ead_values = np.minimum(ead_values, df["LIMIT_BAL"]).round(2)
ead_values = ead_values.where(ead_values > 0, df["LIMIT_BAL"] * 0.1).round(2)

pd_df = pd.DataFrame({"ID": df["ID"], "PD": pd_values})
lgd_df = pd.DataFrame({"ID": df["ID"], "LGD": lgd_values})
ead_df = pd.DataFrame({"ID": df["ID"], "EAD": ead_values})

pd_df.to_csv("data/pd_sample.csv", index=False)
lgd_df.to_csv("data/lgd_sample.csv", index=False)
ead_df.to_csv("data/ead_sample.csv", index=False)

print(f"Wrote {len(pd_df)} rows each to data/pd_sample.csv, data/lgd_sample.csv, data/ead_sample.csv")
