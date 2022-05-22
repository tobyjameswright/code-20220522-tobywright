# Toby Wright 2022
import pandas as pd
import numpy as np


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


def write_json_file(data: pd.DataFrame, filename: str) -> None:
    """
    Function to write a json file from a pandas dataframe
    """
    data.to_json(f"{filename}.json")


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


def calculate_bmi_category(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate the BMI category
    Underweight = BMI <= 18.4
    Normal weight = 18.5 >= BMI <= 24.9
    Overweight = 25 >= BMI <= 29.9
    Moderatley obese = 30 >= BMI <= 34.9
    Severely obese = 35 >= BMI <= 39.9
    Very severely obese = BMI >= 40
    The table provided requires BMI to be rounded to 1 d.p
    1. Round BMI to 1 d.p
    2. Create BMI category condition list
    3. Create list of BMI category names
    4. Create BMI_category column using numpy select
    5. Drop the BMI_rounded column
    """
    data["BMI_rounded"] = data["BMI"].round(1)
    bmi_bins = [
        (data["BMI_rounded"] <= 18.4),
        (data["BMI_rounded"] >= 18.5) & (data["BMI_rounded"] <= 24.9),
        (data["BMI_rounded"] >= 25) & (data["BMI_rounded"] <= 29.9),
        (data["BMI_rounded"] >= 30) & (data["BMI_rounded"] <= 34.9),
        (data["BMI_rounded"] >= 35) & (data["BMI_rounded"] <= 39.9),
        (data["BMI_rounded"] >= 40),
    ]
    categories = [
        "Underweight",
        "Normal weight",
        "Overweight",
        "Moderately obese",
        "Severely obese",
        "Very severely obese",
    ]
    data["BMI_category"] = np.select(bmi_bins, categories)
    data.drop("BMI_rounded", axis=1, inplace=True)
    return data


def join_patients_risk(bmi_cat_risk: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
    return pd.merge(data, bmi_cat_risk, how="left")


def main() -> None:
    patient_df = load_json_data("patient_data")
    bmi_cat_risk = load_csv_data("bmi_categories")
    patient_df_bmi = calculate_bmi(patient_df)
    patient_df_bmi_cat = calculate_bmi_category(patient_df_bmi)
    patient_df_bmi_cat_risk = join_patients_risk(bmi_cat_risk, patient_df_bmi_cat)
    write_json_file(patient_df_bmi_cat_risk, "patients_clean")


if __name__ == "__main__":
    main()
