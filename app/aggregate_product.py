def aggregate_product(df_cleaned):

    df2 = df_cleaned.copy()

    df2["revenue"] = (
        df2["quantity"] * df2["unit_price"]
    )

    product_sales = (
        df2
        .groupby("product")
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum")
        )
        .reset_index()
    )

    return product_sales
