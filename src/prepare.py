"""
Module for prepare .data.
Docs:
    Configure Google Drive as remote storage:
    https://dvc.org/doc/user-guide/setup-google-drive-remote

    DVC user case: https://habr.com/ru/company/funcorp/blog/548942/
"""
import os

import pandas
import yaml


def main():
    cd = CleaningData()
    cd.delete_rows_without_target()
    cd.delete_empty_cols()
    cd.filling_missing_data()
    cd.delete_empty_rows()
    cd.delete_type_object_cols()
    cd.save_data()


class CleaningData:

    def __init__(self):
        self.dataframe = pandas.read_parquet(reports['RawData'])

    def delete_rows_without_target(self) -> None:
        """
        Removes lines with no target value.
        :return: None
        """
        target_name = yaml.safe_load(open('params.yaml'))['prepare']['target_name']
        self.dataframe[target_name] = self.dataframe[target_name].astype(float)
        print('data_cleaning.py: Delete rows without target...')
        self.dataframe = self.dataframe[
            self.dataframe[target_name].notnull()
        ]

    def delete_empty_cols(self) -> pandas.DataFrame:
        """
        Removes columns with poorly populated .data.
        :return: Dataframe with reach populated cols
        """
        full_cols = []
        for col in self.dataframe.columns:
            if self.dataframe[col].isnull().sum() / len(self.dataframe) \
                    < yaml.safe_load(open('params.yaml'))['prepare']['bad_fullness_rate']:
                full_cols.append(col)
        print('data_cleaning.py: Delete empty cols...')
        self.dataframe = self.dataframe[full_cols]
        return self.dataframe

    def filling_missing_data(self) -> pandas.DataFrame:
        """
        Filling in missing .data based on available .data.
        :return: Dataframe with reach populated rows
        """
        print('data_cleaning.py: Filing missing .data...')
        self.dataframe = self.dataframe.fillna(method='backfill')
        return self.dataframe

    def delete_empty_rows(self) -> pandas.DataFrame:
        """
        Removes rows with Nan.
        :return: Dataframe with reach populated rows
        """
        print('data_cleaning.py: Delete empty rows...')
        self.dataframe = self.dataframe.dropna(axis=0)
        return self.dataframe

    def cols_to_datetime(self, cols: list) -> pandas.DataFrame:
        """
        Transforming objects of dataframes to datetime.
        :param cols: List of objects cols
        :return: None
        """
        for col in cols:
            try:
                print('data_cleaning.py: Cols to datetime...')
                self.dataframe[col] = pandas.to_datetime(self.dataframe[col])
                return self.dataframe
            except KeyError:
                pass

    def delete_type_object_cols(self) -> None:
        """
        Deletes all non-float columns.
        :return: None
        """
        print('data_cleaning.py: Delete type object cols...')
        for i in self.dataframe.columns:
            try:
                self.dataframe[i] = self.dataframe[i].astype(float)
            except (ValueError, TypeError):
                self.dataframe.drop(i, axis=1, inplace=True)

    def save_data(self) -> None:
        pass
