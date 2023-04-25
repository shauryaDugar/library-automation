import pandas as pd

df = pd.read_csv("libraryAuto/Database/data.csv")
df = df.set_index("reg_no")

# Function to get name and email by reg_no
def get_info(data):
    if not data.isdigit():
        return None
    reg_no=int(data)
    if reg_no not in df.index:
        return None
    return df.loc[reg_no, ["name", "email"]]
