"""
Configuration for project setting.
"""

# Dirs
DATA_DIRECTORY = 'datasets'
FEATURES_DATA_DIRECTORY = 'features'
LOGS_DIRECTORY = 'logs'
MODELS_DIRECTORY = 'models'

# Globals
DAYS = 365

# Globals for models
RANDOM_SEED = 42
TEST_SIZE = 0.2

# Datasets used in the project
reports = {
    'RawData': f'{DATA_DIRECTORY}/RawData.parquet',
    'CleanedData': f'{DATA_DIRECTORY}/CleanedData.parquet',
    'FeaturedData': f'{DATA_DIRECTORY}/FeaturedData.parquet'
}

# COLUMNS IN MAIN DATAFRAME

# Extra columns in main dataframe (delete by data_cleaning module)
extra_cols = [

]

# Datetime columns
datetime_cols = [

]

target_cols = [

]
