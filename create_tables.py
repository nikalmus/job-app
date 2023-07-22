import psycopg2
from app.db import connect


create_company_table = """
CREATE TABLE IF NOT EXISTS company (
    id  SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
)
"""

create_status_type = """
CREATE TYPE job_status AS ENUM ('Crickets', 'In Progress', 'Rejected', 'Offer')
"""

create_job_table = """
CREATE TABLE IF NOT EXISTS job (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    company_id INTEGER REFERENCES company(id),
    must_have TEXT[],
    nice_have TEXT[],
    link VARCHAR(1000),
    applied_date DATE DEFAULT CURRENT_DATE,  -- Default to the current date
    first_contact_date DATE,
    last_contact_date DATE,
    status job_status DEFAULT 'Crickets'  -- Default to 'Crickets' status
)
"""


def create_tables():
    try:
        conn = connect()
        cursor = conn.cursor()

        cursor.execute(create_company_table)
        cursor.execute(create_status_type)
        cursor.execute(create_job_table)

        conn.commit()
        cursor.close()
        conn.close()
        print("Tables created successfully!")
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    create_tables()


