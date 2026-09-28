import pandas as pd


def clean(df):

    # normaliser quantity
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    df["product"] = df["product"].str.strip().str.lower()

    df["city"] = (
        df["city"]
        .str.strip()
        .str.lower()
        .replace("casa", "casablanca")
    )

    df["unit_price"] = df["unit_price"].fillna(
        df.groupby("product")["unit_price"].transform("mean")
    )

    df = df.dropna(subset=["order_date"])

    df["quantity"] = df["quantity"].abs()
    df["unit_price"]=df["unit_price"].abs()

    df = df.dropna(subset=["quantity"])

    df["city"] = df["city"].fillna("unknown")

    df["email"] = df["email"].fillna("unknown")

    df = df.drop_duplicates(subset=["order_id"])


    # =========================
    # TESTS DE QUALITÉ
    # =========================

    assert df["order_id"].notna().all(), \
        "order_id contains NULL"

    assert df["order_id"].is_unique, \
        "Duplicate order_id detected"

    assert (df["quantity"] > 0).all(), \
        "Invalid quantity detected"

    assert (df["unit_price"] > 0).all(), \
        "Invalid unit_price detected"

    assert (df["order_date"] <= pd.Timestamp.today()).all(), \
        "Future order_date detected"

    print("Data quality checks passed!")

    return df
