import pandas as pd
import numpy as np
from pathlib import Path as P
import seaborn as sns
from matplotlib import pyplot as plt



class Eatogram():
    def __init__(self, df=None, 
                 fn_mint_data=None, 
                 fn_mint_meta=None,
                 sample_id_col='ms_file', 
                 batch_col_name='batch', 
                 sample_type_col_name='type', 
                 media_name='MH-Pool',
                 include_types=None,
                 intensity_col_name='peak_area_top3', 
                 peak_label_col_name='peak_label',
                 low_value_mask=0,
                 noise_factor=0):
        
        self.df = df
        self.media_name = media_name
        
        if df is None:
            self.df = self.get_data_from_mint_files(fn_mint_data, fn_mint_meta)
        try:
            self.df = self.df[[sample_id_col, sample_type_col_name, batch_col_name, peak_label_col_name, intensity_col_name]]
        except KeyError as e:
            print(self.df.columns.to_list())
            raise e
        
        self.df.columns = ['Sample ID', 'Type', 'Batch', 'Metabolite', 'Intensity']
        if include_types:
            self.df = self.df[self.df.Type.isin(include_types+[media_name])]
            
        if noise_factor > 0:
            self.df['Intensity'] = self.df['Intensity']+ (noise_factor * np.random.normal(size=len(self.df)))
            
        self.df['Mask'] = (self.df.Intensity >= low_value_mask)
        self.df_transformed = None
        
    def get_data_from_mint_files(self, fn_mint_data, fn_mint_meta):
            data = pd.read_csv(fn_mint_data)
            data["MS-file"] = data.ms_file.apply(lambda x: P(x).with_suffix("").name)
            meta = pd.read_csv(fn_mint_meta, index_col=0)
            return pd.merge(meta, data, on="MS-file")
    
    @staticmethod
    def to_mh_score(df, media_name):

        media_type_data = df[df['Type'] == media_name]

        mh_mean = (
            media_type_data.groupby(["Metabolite", "Batch"], dropna=False)
            .Intensity.mean()
            .to_frame()
            .add_suffix("_mh_mean")
            .reset_index()
        )

        mh_std = (
            media_type_data.groupby(["Metabolite", "Batch"], dropna=False)
            .Intensity.std()
            .to_frame()
            .add_suffix("_mh_std")
            .reset_index()
            .replace(0, 1)
        )

        # Merging mean and standard deviation with the main dataframe
        df = pd.merge(df, mh_mean, on=["Metabolite", "Batch"])
        df = pd.merge(df, mh_std, on=["Metabolite", "Batch"])

        df["Intensity"] = (
            df.Intensity - df.Intensity_mh_mean
        ) / (df.Intensity_mh_std)    
        
        return df[['Sample ID', 'Type', 'Batch', 'Metabolite', 'Intensity', 'Mask']]    

    @staticmethod
    def durbin_transformation(X, c=1):
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
        X = np.log2((X + np.sqrt(X**2 + c**2)) / 2)
        return X    
    
    @staticmethod
    def long_to_dense_form(df):
        return df.set_index(['Sample ID', 'Type', 'Batch', 'Metabolite', 'Mask']).unstack('Metabolite')   
    
    def transform(self, c=1):
        df_mh = self.to_mh_score(self.df, self.media_name)
        dense = self.long_to_dense_form(df_mh)
        durbin = self.durbin_transformation(dense)
        durbin = durbin.stack().reset_index()
        durbin = self.to_mh_score(durbin, media_name=self.media_name)
        durbin = pd.concat([ durbin[durbin['Type'] != self.media_name], durbin[durbin['Type'] == self.media_name]])
        self.df_transformed = durbin
        
    def plot(self, order=None, height=6, aspect=3, dodge=False, hue_order='default', marker='.', low_values_mask=None):
        
        if order is None:
            order = self.df_transformed[self.df_transformed['Mask']].groupby('Metabolite')['Intensity'].mean().sort_values().index.to_list()

        if hue_order == 'default':
            hue_order = ["Biological sample", self.media_name]
            
        g = sns.catplot(
                data=self.df_transformed,
                x="Metabolite",
                y="Intensity",
                hue='Type',
                dodge=False,
                hue_order=hue_order,
                order=order,
                aspect=aspect,
                height=height,
                marker=marker,
            )

        _ = plt.xticks(rotation=90)

        ax = plt.gca()

        ax.axhline(0, color="k", ls="--", lw=0.5)
        ax.axhline(1, color="k", ls="--", lw=0.5)
        ax.axhline(-1, color="k", ls="--", lw=0.5)
        return g
    
    
