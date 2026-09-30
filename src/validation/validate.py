import pandas as pd
from pandera.errors import SchemaErrors
from validation.schema import schema
from config import REJECTS_DIR

def validate(df):
    try:
        clean_df = schema.validate(df, lazy=True)
        rejects_df = pd.DataFrame(columns=df.columns)
        rejects_df["reject_reason"] = []          
        return clean_df, rejects_df

    except SchemaErrors as e:
        failures = e.failure_cases
        bad_rows = failures["index"].unique()

        reasons = (failures.groupby("index")["check"]
                           .agg("; ".join))

        rejects_df = df.loc[bad_rows].copy()
        rejects_df["reject_reason"] = (reasons.reindex(bad_rows).values)
        rejects_df.insert(0, "n", range(1, len(rejects_df) + 1))
        clean_df = df.drop(bad_rows)
        return clean_df, rejects_df



def write_rejects(rejects_df, day):
    REJECTS_DIR.mkdir(parents=True, exist_ok=True)
    rejects_df.to_csv(REJECTS_DIR / f"{day}_rejects.csv", index=False)