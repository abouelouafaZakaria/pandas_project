import pandas as pd

from clean import clean
from aggregate_product import aggregate_product
from aggregate_city import aggregate_city
from aggregate_date import aggregate_date
from database import get_engine, save_to_postgres


# Lire les données
df = pd.read_csv("sales.csv")


# Nettoyage
df_cleaned = clean(df)


# Agrégations
product_sales = aggregate_product(df_cleaned)
city_sales = aggregate_city(df_cleaned)
monthly_sales = aggregate_date(df_cleaned)


# Connexion à PostgreSQL
engine = get_engine()


# Insertion des tables dans PostgreSQL
save_to_postgres(df_cleaned, "orders_cleaned", engine)
save_to_postgres(product_sales, "sales_by_product", engine)
save_to_postgres(city_sales, "sales_by_city", engine)
save_to_postgres(monthly_sales, "sales_by_month", engine)
