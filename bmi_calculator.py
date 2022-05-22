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


def calculate_height_m(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to convert Height from CM to M
    """
    data["HeightM"] = data["HeightCm"] / 100
    return data


def calculate_bmi(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate BMI via
    BMI = WeightKg / (HeightM) ^ 2
    1. HeightM is calculated
    2. BMI is calculated as above formula
    3. HeightM column is dropped
    """
    data = calculate_height_m(data)
    data["BMI"] = data["WeightKg"] / (data["HeightM"] ** 2)
    data.drop("HeightM", axis=1, inplace=True)
    return data


def main() -> None:
    patient_df = load_json_data("patient_data")
    bmi_cat_risk = load_csv_data("bmi_categories")
    patient_df_bmi = calculate_bmi(patient_df)


if __name__ == "__main__":
    main()
