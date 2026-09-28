def aggregate_date(df_cleaned):

    df2 = df_cleaned.copy()

    df2["revenue"] = (
        df2["quantity"] * df2["unit_price"]
    )

    df2["order_month"] = (
        df2["order_date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_sales = (
        df2
        .groupby("order_month")
        .agg(
            total_orders=("order_id", "count"),
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum")
        )
        .reset_index()
    )

    return monthly_sales
