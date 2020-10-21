from src import mysql
from src.examples import data


def main():
    with mysql.ProjectTable() as client:
        client.create_database()
        client.create_table()
        client.upsert(data.project1)
    return


if __name__ == "__main__":
    main()
