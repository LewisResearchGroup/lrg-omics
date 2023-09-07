import pandas as pd
import numpy as np
from pathlib import Path as P
import seaborn as sns
from matplotlib import pyplot as plt



class Eatogram():
    """
    Initializes the Eatogram object with optional data preprocessing steps.

    Parameters:
    -----------
    df : pandas.DataFrame, optional
        A DataFrame containing the metabolomics data. Columns must include sample IDs, types, batches, metabolites, and intensity values.
    fn_mint_data : str, optional
        File name for reading raw MINT data. Used if df is not provided.
    fn_mint_meta : str, optional
        File name for reading MINT metadata. Used if df is not provided.
    sample_col : str, default='ms_file_label'
        The name of the column in df representing the sample IDs.
    batch_col : str, default='plate'
        The name of the column in df representing the batch IDs.
    sample_type_col : str, default='sample_type'
        The name of the column in df representing the sample types.
    media_name : str, default='MH-Pool'
        The name of the media sample type.
    include_types : list of str, optional
        A list of sample types to include in the analysis.
    intensity_col : str, default='peak_area_top3'
        The name of the column in df representing the intensity of each metabolite.
    metabolite_col : str, default='peak_label'
        The name of the column in df representing the label of each metabolite peak.
    low_value_mask : float, default=0
        Threshold below which intensity values will be masked.
    noise_factor : float, default=0
        If greater than zero, random noise scaled by this factor will be added to the intensity values.


    Example 1:
    ----------
    eatogram = Eatogram(
                fn_mint_data='MINT__results.csv', 
                fn_mint_meta='MINT__metadata.csv',
                sample_col='MS-file',
                sample_type_col='Type',
                media_name='MH-Pool',
                batch_col='PLATE',
                intensity_col='peak_area_top3',
                low_value_mask=1e4
    )

    eatogram.transform(c=10)
    eatogram.plot()

    Example 2:
    ----------
    Create a dataframe (df) of the following format:

              sample_col     sample_type  batch_col  metabolite_col  intensity_col
    0         S1             Media        Plate-1     Glucose        100.5e6
    1         S1             Media        Plate-1     Lactose         25.3e3
    2         S2             Biological   Plate-1     Glucose         90.2e5
    3         S2             Biological   Plate-1     Lactose         22.4e4
    4         S3             Media        Plate-2     Glucose        105.0e5
    5         S3             Media        Plate-2     Lactose         24.1e6
    6         S4             Biological   Plate-2     Glucose         92.8e5
    7         S4             Biological   Plate-2     Lactose         20.2e4

    eatogram = Eatogram(
                df=df,
                sample_col='sample_col',
                sample_type_col='sample_type',
                media_name='Media',
                batch_col='batch_col',
                intensity_col='intensity_col',
                low_value_mask=0
    )

    eatogram.transform(c=10)
    eatogram.plot()
    """
    def __init__(self, df=None, 
                 fn_mint_data=None, 
                 fn_mint_meta=None,
                 sample_col='ms_file_label', 
                 batch_col='plate', 
                 sample_type_col='sample_type', 
                 media_name='MH-Pool',
                 include_types=None,
                 metabolite_col='peak_label',
                 intensity_col='peak_area_top3', 
                 low_value_mask=0,
                 noise_factor=0):
        """
        Initializes the Eatogram object with optional data preprocessing steps.

        Parameters:
        -----------
        df : pandas.DataFrame, optional
            A DataFrame containing the metabolomics data. Columns must include sample IDs, types, batches, metabolites, and intensity values.
        fn_mint_data : str, optional
            File name for reading raw MINT data. Used if df is not provided.
        fn_mint_meta : str, optional
            File name for reading MINT metadata. Used if df is not provided.
        sample_col : str, default='ms_file_label'
            The name of the column in df representing the sample IDs.
        batch_col : str, default='plate'
            The name of the column in df representing the batch IDs.
        sample_type_col : str, default='sample_type'
            The name of the column in df representing the sample types.
        media_name : str, default='MH-Pool'
            The name of the media sample type.
        include_types : list of str, optional
            A list of sample types to include in the analysis.
        intensity_col : str, default='peak_area_top3'
            The name of the column in df representing the intensity of each metabolite.
        metabolite_col : str, default='peak_label'
            The name of the column in df representing the label of each metabolite peak.
        low_value_mask : float, default=0
            Threshold below which intensity values will be masked.
        noise_factor : float, default=0
            If greater than zero, random noise scaled by this factor will be added to the intensity values.

        
        Example 1:
        ----------
        eatogram = Eatogram(
                    fn_mint_data='MINT__results.csv', 
                    fn_mint_meta='MINT__metadata.csv',
                    sample_col='MS-file',
                    sample_type_col='Type',
                    media_name='MH-Pool',
                    batch_col='PLATE',
                    intensity_col='peak_area_top3',
                    low_value_mask=1e4
        )

        eatogram.transform(c=10)
        eatogram.plot()
        
        Example 2:
        ----------
        Create a dataframe (df) of the following format:
        
                  sample_col     sample_type  batch_col  metabolite_col  intensity_col
        0         S1             Media        Plate-1     Glucose        100.5e6
        1         S1             Media        Plate-1     Lactose         25.3e3
        2         S2             Biological   Plate-1     Glucose         90.2e5
        3         S2             Biological   Plate-1     Lactose         22.4e4
        4         S3             Media        Plate-2     Glucose        105.0e5
        5         S3             Media        Plate-2     Lactose         24.1e6
        6         S4             Biological   Plate-2     Glucose         92.8e5
        7         S4             Biological   Plate-2     Lactose         20.2e4
        
        eatogram = Eatogram(
                    df=df,
                    sample_col='sample_col',
                    sample_type_col='sample_type',
                    media_name='Media',
                    batch_col='batch_col',
                    intensity_col='intensity_col',
                    low_value_mask=0
        )

        eatogram.transform(c=10)
        eatogram.plot()
        """
        self.df = df
        self.sample_col = sample_col
        self.batch_col = batch_col
        self.sample_type_col = sample_type_col
        self.media_name = media_name
        self.metabolite_col = metabolite_col
        self.intensity_col = intensity_col
        
        if df is None:
            self.df = self.get_data_from_mint_files(fn_mint_data, fn_mint_meta)
        try:
            self.df = self.df[[sample_col, sample_type_col, batch_col, metabolite_col, intensity_col]]
            
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
        """
        Reads metabolomics data from MINT files and merges it with metadata.
        
        Parameters:
        -----------
        fn_mint_data : str
            File name for reading raw MINT data.
        fn_mint_meta : str
            File name for reading MINT metadata.
            
        Returns:
        --------
        pandas.DataFrame
            The merged DataFrame containing metabolomics data and metadata.
        """        
        data = pd.read_csv(fn_mint_data)
        data["MS-file"] = data.ms_file.apply(lambda x: P(x).with_suffix("").name)
        meta = pd.read_csv(fn_mint_meta, index_col=0)
        return pd.merge(meta, data, on="MS-file")
    
    @staticmethod
    def to_mh_score(df, media_name):
        """
        Transforms the data into MH-score format.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame containing metabolomics data.
        media_name : str
            The name of the media sample type.
            
        Returns:
        --------
        pandas.DataFrame
            The DataFrame in MH-score format.
        """
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
        Applies the Durbin transformation to the DataFrame.
        
        Parameters:
        -----------
        X : pandas.DataFrame
            The DataFrame to be transformed.
        c : float, default=1
            Constant to be used in transformation.
            
        Returns:
        --------
        pandas.DataFrame
            The DataFrame after applying Durbin transformation.
        """
        X = np.log2((X + np.sqrt(X**2 + c**2)) / 2)
        return X    
    
    @staticmethod
    def long_to_dense_form(df):
        """
        Converts the DataFrame from long to dense format.
        
        Parameters:
        -----------
        df : pandas.DataFrame
            The DataFrame in long format.
        
        Returns:
        --------
        pandas.DataFrame
            The DataFrame in dense format.
        """        
        return df.set_index(['Sample ID', 'Type', 'Batch', 'Metabolite', 'Mask']).unstack('Metabolite')   
    
    def transform(self, c=1):
        """
        Applies a series of transformations on the DataFrame.
        
        Parameters:
        -----------
        c : float, default=1
            Constant to be used in Durbin transformation.
        """        
        df_mh = self.to_mh_score(self.df, self.media_name)
        dense = self.long_to_dense_form(df_mh)
        durbin = self.durbin_transformation(dense)
        durbin = durbin.stack().reset_index()
        durbin = self.to_mh_score(durbin, media_name=self.media_name)
        durbin = pd.concat([ durbin[durbin['Type'] != self.media_name], durbin[durbin['Type'] == self.media_name]])
        self.df_transformed = durbin
        
    def plot(self, order=None, height=6, aspect=3, dodge=False, hue_order='default', marker='.', low_values_mask=None):
        """
        Plots the transformed data.
        
        Parameters:
        -----------
        order : list, optional
            Order in which to plot the metabolites.
        height : int, default=6
            Height of the plot.
        aspect : int, default=3
            Aspect ratio of the plot.
        dodge : bool, default=False
            Whether to dodge the points in the plot.
        hue_order : list or 'default', default='default'
            Order in which to plot hues.
        marker : str, default='.'
            Marker style for the plot.
        low_values_mask : optional
            If provided, mask low values in the plot.
            
        Returns:
        --------
        seaborn.catplot
            The Seaborn Catplot object.
        """
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
    
    
