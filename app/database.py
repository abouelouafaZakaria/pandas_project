from sqlalchemy import create_engine


def get_engine():

    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@postgres-db:5432/sales"
    )

    return engine


def save_to_postgres(df, table_name, engine):

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )
