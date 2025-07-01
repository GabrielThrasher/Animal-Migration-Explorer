import requests
import pandas as pd
from dotenv import load_dotenv
import os
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_and_save_movebank_data(dir_path, study_id, animal_species):
    url = (
        "https://www.movebank.org/movebank/service/direct-read?entity_type"
        f"=event&study_id={study_id}"
    )
    load_dotenv()
    auth = (os.getenv("MOVEBANKUSERNAME"), os.getenv("MOVEBANKPASSWORD"))
    session = requests.Session()
    retries = Retry(
        total=5, backoff_factor=1, status_forcelist=[502, 503, 504],
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    response = session.get(url, auth=auth)

    if str(response.status_code)[0] == "2":
        file_name = f"{animal_species}_{study_id}.csv"
        with open(dir_path + file_name, "w") as f:
            f.write(response.text)
        print(f" - Saved study {study_id} data to {dir_path + file_name}")

    else:
        print("Could not save data.")


def get_all_movebank_data(dir_path, study_ids_file):
    print("=" * 100)
    print("Downloading and saving the following movebank data:")
    with open(study_ids_file, "r") as f:
        info = f.read().splitlines()
        study_ids = [x[:x.index(" ")] for x in info]
        animal_species = [
            x[x.index(" ")+1:].replace(" ", "_") for x in info
        ]

    for i in range(len(animal_species)):
        get_and_save_movebank_data(dir_path, study_ids[i], animal_species[i])

    print("=" * 100)


def display_movebank_data(dir_path):
    print("=" * 100)
    print("Displaying all Movebank data...")
    csv_data_file_names = os.listdir(dir_path)
    if len(csv_data_file_names) > 0:
        for i, csv_data_file_name in enumerate(csv_data_file_names):
            df = pd.read_csv(
                dir_path + csv_data_file_name, encoding="ISO-8859-1"
            )
            with pd.option_context(
                    "display.max_columns", None, "display.width", None
            ):
                print("-" * 100)
                print(f"({i+1}/{len(csv_data_file_names)}) Data from "
                      f"{dir_path + csv_data_file_name}")
                print(f"Shape (rows, cols): {df.shape}")
                print(df.head(10))
                print(df.tail(10))
    else:
        print("No data saved.")
    print("=" * 100)


def main():
    dir_path = "csv_data/"
    study_ids_file = "study_ids.txt"

    user_response = input("Would you like to download Movebank data? (y/n): ")
    if user_response.lower() == "y":
        get_all_movebank_data(dir_path, study_ids_file)

    display_movebank_data(dir_path)


if __name__ == "__main__":
    main()
