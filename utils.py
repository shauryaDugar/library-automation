import pandas as pd

df = pd.read_csv("data.csv")
df = df.set_index("reg_no")

# Function to get name and email by reg_no
def get_info(reg_no):
    if reg_no not in df.index:
        return None
    return df.loc[reg_no, ["name", "email"]]
