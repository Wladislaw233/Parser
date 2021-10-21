"""
import sqlite3
conn = sqlite3.connect("inter.db")
sql="CREATE TABLE Components(name TEXT, brand TEXT, price INTEGER, description TEXT, photo_link TEXT, product_link TEXT)"
cursor = conn.cursor()
cursor.execute(sql)
conn.close()
""" #создание таблицы в дб
import sqlite3

from rich.table import Table
from rich.console import Console

console = Console()


def Make_Table(results):
    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("name", style="dim", width=16)
    table.add_column("brand")
    table.add_column("Price")
    table.add_column("Description")
    table.add_column("Photo_link")
    table.add_column("Product_link")

    for line in results:
        table.add_row(str(line[0]), str(line[1]), str(line[2]), str(line[3]))

    console.print(table)


def Read():
    conn = sqlite3.connect('inter.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Components;")
    all_results = cursor.fetchall()
    return all_results


def main():
    all_results = Read()
    Make_Table(all_results)

if __name__ == '__main__':
    main()