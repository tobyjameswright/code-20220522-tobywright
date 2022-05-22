# Toby Wright 2022
from bmi_calculator import calculate_height_m, calculate_bmi
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
