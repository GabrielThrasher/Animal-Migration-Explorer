import pandas as pd
import os
import re
import numpy as np
import sqlite3


def csv_to_df(csv_data_dir_path):
    csv_data_file_names = os.listdir(csv_data_dir_path)
    table_names = []
    data_frames = []

    for csv_data_file_name in csv_data_file_names:
        print(f"Converting {csv_data_file_name}.")
        df = pd.read_csv(csv_data_dir_path + csv_data_file_name)
        indiv_ids = df["individual_id"].unique()

        final_data = []
        for indiv_id in indiv_ids:
            if np.isnan(indiv_id):
                break
            subset_df = df[df["individual_id"] == indiv_id]

            data_pts_dict = {}
            for index, row in subset_df.iterrows():
                timestamp = row["timestamp"]
                pattern = r"([0-9]{4})-([0-9]{2})-[0-9]{2}\s.*"
                match = re.search(pattern, timestamp)
                year = match.group(1)
                month = match.group(2)

                if year not in data_pts_dict.keys():
                    data_pts_dict[year] = {}

                if month not in data_pts_dict[year].keys():
                    data_pts_dict[year][month] = {
                        "year": year,
                        "month": month,
                        "latitude": [0, 0],
                        "longitude": [0, 0]
                    }

                lat_list = data_pts_dict[year][month]["latitude"]
                lon_list = data_pts_dict[year][month]["longitude"]

                if not pd.isna(row["location_lat"]):
                    lat_list[0] = lat_list[0] + float(row["location_lat"])
                    lat_list[1] = lat_list[1] + 1
                if not pd.isna(row["location_long"]):
                    lon_list[0] = lon_list[0] + float(row["location_long"])
                    lon_list[1] = lon_list[1] + 1

            data = []
            for year in data_pts_dict.keys():
                for month in data_pts_dict[year].keys():
                    lat_sum = data_pts_dict[year][month]["latitude"][0]
                    lat_num = data_pts_dict[year][month]["latitude"][1]

                    if lat_num != 0:
                        data_pts_dict[year][month]["latitude"] = (
                                lat_sum / lat_num
                        )
                    else:
                        continue

                    lon_sum = data_pts_dict[year][month]["longitude"][0]
                    lon_num = data_pts_dict[year][month]["longitude"][1]

                    if lon_num != 0:
                        data_pts_dict[year][month]["longitude"] = (
                                lon_sum / lon_num
                        )
                    else:
                        continue

                    data.append(data_pts_dict[year][month])

            if len(data) > len(final_data):
                final_data = data

        final_data_df = pd.DataFrame(final_data)

        if not final_data_df.empty:
            table_names.append(csv_data_file_name)
            data_frames.append(final_data_df)
    
    return table_names, data_frames


def drop_all_tables(db_path):
    print(f"Dropping all tables.")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%';"
    )
    tables = cur.fetchall()

    for (table_name,) in tables:
        cur.execute(f"DROP TABLE IF EXISTS '{table_name}';")

    conn.commit()
    conn.close()


def add_tables(db_path, table_names, data_frames):
    conn = sqlite3.connect(db_path)

    for table_name, data_frame in zip(table_names, data_frames):
        table_name = table_name.replace(".csv", "").replace(" ", "_")
        print(f"Adding table {table_name}.")

        data_frame.to_sql(
            table_name, conn, if_exists='replace', index=False
        )

        pd.read_sql(f"SELECT * FROM '{table_name}'", conn)
        conn.commit()

    conn.close()


def main():
    csv_data_dir_path = "csv_data/"
    database_path = "../coordinates.db"

    table_names, data_frames = csv_to_df(csv_data_dir_path)
    drop_all_tables(database_path)
    add_tables(database_path, table_names, data_frames)


if __name__ == "__main__":
    main()
