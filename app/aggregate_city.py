def aggregate_city(df_cleaned):

    df2 = df_cleaned.copy()

    df2["revenue"] = (
        df2["quantity"] * df2["unit_price"]
    )

    city_sales = (
        df2
        .groupby("city")
        .agg(
            total_orders=("order_id", "count"),
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum")
        )
        .reset_index()
    )

    return city_sales
