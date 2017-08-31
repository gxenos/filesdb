import database
import file_metadata
import os
import prettytable
import argparse


def print_table(cursor):
    table = prettytable.from_db_cursor(cursor)
    print(table)


def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', help='Lists all scans in database.', action='store_true')
    group.add_argument('-st', '--stats', help='Lists stats about database contents.', action='store_true')
    group.add_argument('-sc', '--scan', help='Scan a location and add to the database.', type=str)
    group.add_argument('-qs', '--quickscan', help='Scan a location ignoring hashes and add to the database.', type=str)
    parser.add_argument('-v', '--version', action='version', version='0.0.1')
    parser.add_argument("database", help="Location of the database (Default files.db).", type=str)

    args = parser.parse_args()

    if args.database:
        file_database = database.DataBase(args.database + '.db')
    else:
        file_database = database.DataBase('files.db')

    if args.scan:
        file_database.add_scan(args.scan)
        scan_id = file_database.get_last_scan_id()
        for root, dirnames, files in os.walk(args.scan):
            for file in files:
                file_data = file_metadata.FileMetadata(root, file)
                file_database.add_file(file_data, scan_id)
        cont = file_database.print_all()
        print_table(cont)
        file_database.dissconect()
    elif args.quickscan:
        file_database.add_quick_scan(args.quickscan)
        scan_id = file_database.get_last_scan_id()
        for root, dirnames, files in os.walk(args.quickscan):
            for file in files:
                file_data = file_metadata.FileMetadata(root, file, quick=True)
                file_database.add_quick_file(file_data, scan_id)
        cont = file_database.print_all()
        print_table(cont)
        file_database.dissconect()
    elif args.list:
        cont = file_database.list_scans()
        print_table(cont)
        file_database.dissconect()
    elif args.stats:
        cont = file_database.show_stats()
        print_table(cont)
        file_database.dissconect()


if __name__ == "__main__":
    main()
