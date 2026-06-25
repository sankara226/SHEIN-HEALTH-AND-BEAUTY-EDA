def insight_top_vs_low(df):
    top = df.nlargest(10, "quantity_sold")[["price", "discount", "quantity_sold"]]
    low = df.nsmallest(10, "quantity_sold")[["price", "discount", "quantity_sold"]]

    print("INSIGHT — Top 10 Best Sellers")
    print(top)
    print("")

    print("INSIGHT — Bottom 10 Worst Sellers")
    print(low)
    print("")


def insight_elasticity(df):
    corr_price = df["price"].corr(df["quantity_sold"])
    corr_discount = df["discount"].corr(df["quantity_sold"])

    print("INSIGHT — Elasticity")
    print(f"Correlation (Price → Sales): {corr_price}")
    print(f"Correlation (Discount → Sales): {corr_discount}")
    print("")


def run_business_insights(df):
    print("=== BUSINESS INSIGHTS ===\n")
    insight_top_vs_low(df)
    insight_elasticity(df)

    print("Business insights completed.\n")
