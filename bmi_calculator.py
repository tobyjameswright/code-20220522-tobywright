# Toby Wright 2022
import pandas as pd
import numpy as np
import logging
import sys


def load_json_data(filename: str) -> pd.DataFrame:
    """
    Function to load a JSON file into a pandas dataframe
    """
    try:
        data = pd.read_json(f"{filename}.json")
        data.dropna(inplace=True)
        logging.info("Data read from JSON file")
        return data
    except ValueError as e:
        logging.warning(f"Json file not found: {e}")
        sys.exit()


def load_csv_data(filename: str) -> pd.DataFrame:
    """
    Function to load a CSV file into a pandas dataframe
    """
    try:
        data = pd.read_csv(f"{filename}.csv")
        logging.info("Data read from CSV file")
        return data
    except FileNotFoundError as e:
        logging.warning(f"CSV file not found: {e}")
        sys.exit()


def write_json_file(data: pd.DataFrame, filename: str) -> None:
    """
    Function to write a json file from a pandas dataframe
    """
    data.to_json(f"{filename}.json")
    logging.info("JSON file written")


def write_csv_file(data: pd.DataFrame, filename: str) -> None:
    """
    Function to write a CSV file from a pandas dataframe
    """
    data.to_csv(f"{filename}.csv")
    logging.info("CSV file written")


def calculate_height_m(data: pd.DataFrame) -> pd.DataFrame:
    """
    Function to convert Height from CM to M
    """
    data["HeightM"] = data["HeightCm"] / 100
    logging.info("Height in M calculated")
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
    logging.info("BMI calculated")
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
    logging.info("BMI category calculated")
    return data


def join_patients_risk(bmi_cat_risk: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
    comb_df = pd.merge(data, bmi_cat_risk, how="left")
    logging.info("Dataset joined with BMI risks")
    return comb_df


def calculate_counts(data: pd.DataFrame, group: str) -> pd.DataFrame:
    """
    Function to calculate the counts per category
    As only the overwight category was requested a filter is also applied,
    however this can be removed to recieve all data
    """
    overweight = data[data["BMI_category"] == "Overweight"]
    count_data = overweight.reset_index().groupby(group).agg({"index": "nunique"})
    count_data.rename(columns={"index": "PatientCount"}, inplace=True)
    logging.info("Counts calculated for Overweight category")
    return count_data


def main() -> None:
    logging.basicConfig(
        filename="bmi_calculator.log", encoding="utf-8", level=logging.INFO
    )
    patient_df = load_json_data("patient_data")
    bmi_cat_risk = load_csv_data("bmi_categories")
    patient_df_bmi = calculate_bmi(patient_df)
    patient_df_bmi_cat = calculate_bmi_category(patient_df_bmi)
    patient_df_bmi_cat_risk = join_patients_risk(bmi_cat_risk, patient_df_bmi_cat)
    write_json_file(patient_df_bmi_cat_risk, "patients_clean")
    summarised_data = calculate_counts(
        patient_df_bmi_cat_risk[["BMI_category"]], "BMI_category"
    )
    write_csv_file(summarised_data, "patients_count")


if __name__ == "__main__":
    main()
