# Toby Wright 2022
import pandas as pd


def load_json_data(filename: str) -> pd.DataFrame:
    """
    Function to load a JSON file into a pandas dataframe
    """
    data = pd.read_json(f"{filename}.json")
    return data


def load_csv_data(filename: str) -> pd.DataFrame:
    """
    Function to load a CSV file into a pandas dataframe
    """
    data = pd.read_csv(f"{filename}.csv")
    return data


def main() -> None:
    patient_df = load_json_data("patient_data")
    bmi_cat_risk = load_csv_data("bmi_categories")


if __name__ == "__main__":
    main()
