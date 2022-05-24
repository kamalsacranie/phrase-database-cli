from sqlalchemy import create_engine, text


DATABASE_URL: str = "sqlite+pysqlite:///:memory:"

engine = create_engine(DATABASE_URL, echo=True, future=True)


def main():
    # Creating a table using textual
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE some_table (x int, y int)"))
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        )
        conn.commit()

    # Example of begin once
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
            [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
        )

    with engine.connect() as conn:
        result = conn.execute(text("SELECT x, y FROM some_table"))
        for row in result:
            print(f"x: {row.x}  y: {row.y}")


if __name__ == "__main__":
    main()
