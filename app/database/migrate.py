from sqlalchemy import text

from app.database.db import engine


NEW_COLUMNS = {
    "primary_intent": "VARCHAR(50)",
    "primary_confidence": "FLOAT",
    "secondary_intent": "VARCHAR(50)",
    "secondary_confidence": "FLOAT",
    "signals": "TEXT",
    "intent_summary": "TEXT",
}


def migrate():
    with engine.begin() as connection:

        existing_columns = connection.execute(
            text("PRAGMA table_info(discussions)")
        ).fetchall()

        existing_names = {
            column[1]
            for column in existing_columns
        }

        for column_name, column_type in NEW_COLUMNS.items():

            if column_name not in existing_names:
                connection.execute(
                    text(
                        f"ALTER TABLE discussions "
                        f"ADD COLUMN {column_name} {column_type}"
                    )
                )

                print(f"✅ Added column: {column_name}")

            else:
                print(f"⏭ Already exists: {column_name}")


if __name__ == "__main__":
    migrate()