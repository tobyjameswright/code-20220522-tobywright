# Toby Wright 2022
from bmi_calculator import calculate_height_m, calculate_bmi, calculate_bmi_category
import pandas as pd


def test_calculate_height_m():
    test_df = pd.DataFrame.from_dict(
        {"Gender": ["Male"], "HeightCm": [100], "WeightKg": [82]}
    )
    updated_df = calculate_height_m(test_df)
    assert updated_df["HeightM"].iloc[0] == 1


def test_calculate_bmi():
    test_df = pd.DataFrame.from_dict(
        {"Gender": ["Male"], "HeightCm": [100], "WeightKg": [82]}
    )
    updated_df = calculate_bmi(test_df)
    assert updated_df["BMI"].iloc[0] == 82


def test_calculate_bmi_category():
    test_df = pd.DataFrame.from_dict(
        {"Gender": ["Male"], "HeightCm": [100], "WeightKg": [82]}
    )
    df_bmi = calculate_bmi(test_df)
    updated_df = calculate_bmi_category(df_bmi)
    assert updated_df["BMI_category"].iloc[0] == "Very severely obese"
