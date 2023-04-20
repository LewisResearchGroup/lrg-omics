import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pathlib import Path as P

class Eatogram:
    """
    A class used to process and visualize metabolomics data.
    """
    def __init__(self, data_file, metadata_file, name, low_values_mask=1e4, media_type_name='MH-Pool', batch_col_name='PLATE', type_col_name='Type'):
        """
        Parameters
        ----------
        data_file : str
            The path to the data file.
        metadata_file : str
            The path to the metadata file.
        name : str
            The name of the Eatogram instance.
        low_values_mask : float, optional, default: 1e4
            The threshold for masking low values in the dataset.
        media_type_name : str, optional, default: 'MH-Pool'
            The name of the media type in the dataset.
        batch_col_name : str, optional, default: 'PLATE'
            The name of the batch column in the dataset.
        type_col_name : str, optional, default: 'Type'
            The name of the type column in the dataset.
        """
        self.data_file = data_file
        self.metadata_file = metadata_file
        self.name = name
        self.low_values_mask = low_values_mask
        self.media_type_name = media_type_name
        self.batch_col_name = batch_col_name
        self.type_col_name = type_col_name

    @staticmethod
    def durbin_transformation(X, c=0):
        """
        Applies the Durbin transformation to a given dataset.

        Parameters
        ----------
        X : pd.DataFrame
            The input data to be transformed.
        c : float, optional, default: 0
            A constant used in the transformation.

        Returns
        -------
        pd.DataFrame
            The transformed data.
        """
        X = np.log2((X + np.sqrt(X ** 2 + c ** 2)) / 2)
        return X

    def load_data(self):
        """
        Loads data and metadata from their respective files.
        """
        self.df = pd.read_csv(self.data_file)
        self.meta = pd.read_csv(self.metadata_file, index_col=0)

    def preprocess_data(self):
        """
        Preprocesses the loaded data by merging metadata with the data.
        """
        self.df['MS-file'] = self.df.ms_file.apply(lambda x: P(x).with_suffix('').name)
        self.df1 = pd.merge(self.meta, self.df, on='MS-file')

    def calculate_mh_scores(self):
        """
        Calculates the MH scores for the data.
        """
        # Grouping and aggregating mean and standard deviation for media type samples
        media_type_data = self.df1[self.df1.Type == self.media_type_name]
        mh_mean = media_type_data.groupby(['peak_label', self.batch_col_name], dropna=False).peak_max.mean().to_frame().add_suffix('_mh_mean').reset_index()
        mh_std = media_type_data.groupby(['peak_label', self.batch_col_name], dropna=False).peak_max.std().to_frame().add_suffix('_mh_std').reset_index().replace(0, 1)

        # Merging mean and standard deviation with the main dataframe
        self.df1 = pd.merge(self.df1, mh_mean, on=['peak_label', self.batch_col_name])
        self.df1 = pd.merge(self.df1, mh_std, on=['peak_label', self.batch_col_name])

        # Calculating MH scores
        self.df1['peak_max_mh_score'] = (
            (self.df1.peak_max - self.df1.peak_max_mh_mean)
            / (self.df1.peak_max_mh_std)
        )

        X = self.df1.groupby(['ms_file', 'peak_label']).mean().peak_max_mh_score.unstack('peak_label')

        self.X_tranformed = self.durbin_transformation(X, c=1)        
        

    def finalize_data(self):
        """
        Finalizes the data processing by calculating the Durbin transformed MH scores.
        """
        self.df2 = pd.merge(self.df1, self.X_tranformed.unstack().to_frame().rename(columns={0: 'durbin'}), left_on=['peak_label', 'ms_file'], right_index=True)

        media_type_data = self.df2[self.df2.Type == self.media_type_name]
        mh_mean = media_type_data.groupby(['peak_label', self.batch_col_name], dropna=False).durbin.mean().to_frame().add_suffix('_mh_mean').reset_index()
        mh_std = media_type_data.groupby(['peak_label', self.batch_col_name], dropna=False).durbin.std().to_frame().add_suffix('_mh_std').reset_index().replace(0, 1)

        self.df2 = pd.merge(self.df2, mh_mean, on=['peak_label', self.batch_col_name])
        self.df2 = pd.merge(self.df2, mh_std, on=['peak_label', self.batch_col_name])

        self.df2['durbin_mh_score'] = (
            (self.df2.durbin - self.df2.durbin_mh_mean)
            / (self.df2.durbin_mh_std)
        )

        durbin = self.df2[self.df2.Type.isin(['Biological sample', self.media_type_name])].sort_values(self.type_col_name, ascending=True)

        durbin['durbin_mh_score_masked'] = durbin['durbin_mh_score']
        durbin['durbin_mh_score_low_projected_to_zero'] = durbin['durbin_mh_score']
        durbin.loc[durbin['peak_max'] < self.low_values_mask, 'durbin_mh_score_low_projected_to_zero'] = 0
        durbin.loc[durbin['peak_max'] < self.low_values_mask, 'durbin_mh_score_masked'] = None

        self.durbin = durbin        
        
        
    def visualize(self, order=None, aspect=5, height=2.5, **kwargs):
        """
        Visualizes the Durbin transformed MH scores.

        Parameters
        ----------
        order : list, optional, default: None
            The order of the peak labels to be displayed in the plot.
        aspect : float, optional, default: 5
            The aspect ratio of the plot.
        height : float, optional, default: 2.5
            The height of the plot.
        **kwargs : dict
            Additional keyword arguments to pass to the seaborn catplot function.
        """
        if order is None:
            order = self.durbin[(self.durbin[self.type_col_name] == 'Biological sample') & (self.durbin.durbin_mh_score_masked.notna())].groupby('peak_label').durbin_mh_score_masked.median().sort_values().index.to_list()

        g = sns.catplot(data=self.durbin, x='peak_label', y='durbin_mh_score', hue=self.type_col_name,
                        dodge=False, hue_order=['Biological sample', self.media_type_name], order=order,
                        aspect=aspect, height=height, marker='.', **kwargs)

        _ = plt.xticks(rotation=90)

        ax = plt.gca()

        ax.axhline(0, color='k', ls='--', lw=0.5)
        ax.axhline(1, color='k', ls='--', lw=0.5)
        ax.axhline(-1, color='k', ls='--', lw=0.5)

    def transform(self):
        """
        Performs the entire data processing pipeline.
        """
        self.load_data()
        self.preprocess_data()
        self.calculate_mh_scores()
        self.finalize_data()

    def run(self):
        """
        Executes the data processing pipeline and visualizes the results.
        """
        self.transform()
        self.visualize()        