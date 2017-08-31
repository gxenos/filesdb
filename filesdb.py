import database
import file_metadata
import os
import prettytable


def print_table(cursor):
    table = prettytable.from_db_cursor(cursor)
    print(table)


def main():
    file_database = database.DataBase('1.db')
    file_database.add_quick_scan('/home/george/Downloads')
    scan_id = file_database.get_last_scan_id()
    for root, dirnames, files in os.walk('/home/george/Downloads'):
        for file in files:
            file_data = file_metadata.FileMetadata(root, file)
            file_database.add_quick_file(file_data, scan_id)

    cont = file_database.print_all()

    print_table(cont)

    file_database.dissconect()


if __name__ == "__main__":
    main()
