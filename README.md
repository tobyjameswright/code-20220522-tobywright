# BMI Calculator

## Solution
As the data is provided in JSON format with a limited number of columns I have decided to build an app using pandas and numpy.

I have tested this solution with >1,000,000 records of randomly generated data and it runs locally in ~3 seconds. Note that the json file with >1,000,000 records is 55mb so it would not require a large compute instance to run as is.

I believe this approach will be sufficent for this data and will reduce overall costs of spinning up a cluster to run this in a distrubuted manner with Apache spark or Beam.

If the data was to grow exponentially this script could be repurposed to leverage compute clusters and I would suggest running it in a serverless way via DataProc/DataFlow on GCP unless there is an internal cluster available.

## Missing/Null data
For this script I have decided to remove any rows that have missing data. However a different approach could be used depending on the business use case

# How to run

Run `pip install requirements.txt`
Run `python calculate_bmi.py``

## Description

Python app that takes in JSON patient data, calculates the BMI and then outputs cleaned data and a count per BMI category

Input JSON data is in the patients.json file

Output JSON data is in the patients_clean.json file

Output summarised data is in the patients_counts.csv file

# Calculation
BMI = WeightKG / (HeightM^2)

# Tests
Test are available in the tests folder

# Pre-commit
Pre-commit hooks have been included that:
	- auto format code to black standard
	- check mypy formatting
