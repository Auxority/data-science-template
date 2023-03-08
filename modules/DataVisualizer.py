import seaborn as sns
import numpy as np
from pandas import DataFrame
from matplotlib import pyplot as plt
from typing import Optional

class DataVisualizer:
    def __init__(
            self,
            max_plots: Optional[int] = 30,
            plots_per_row: Optional[int] = 3,
            figure_size: Optional[int] = 5
    ):
        self.max_plots = max_plots
        self.plots_per_row = plots_per_row
        self.figure_size = figure_size
        sns.set_style('darkgrid')
    
    def visualize(self, df: DataFrame) -> None:
        self._visualize_distributions(df, 'number', 'Distribution of {}')
        self._visualize_distributions(df, 'object', 'Counts of {}')
        self._visualize_distributions(df, 'datetime64', 'Distribution of {}')
        self._visualize_correlations(df)

    def _visualize_distributions(self, df: DataFrame, column_type: str, title_format: str) -> None:
        target_columns = df.select_dtypes(include=[column_type]).columns

        plot_count = len(target_columns)
        if len(target_columns) == 0:
            return None

        number_of_rows = int(np.ceil(plot_count / self.plots_per_row))
        figure_width = np.multiply(self.figure_size, self.plots_per_row)
        figure_height = np.multiply(self.figure_size, number_of_rows)
        figure, axes = plt.subplots(
            nrows=number_of_rows,
            ncols=self.plots_per_row,
            figsize=(figure_width, figure_height)
        )

        for i, col in enumerate(target_columns):
            if i >= self.max_plots:
                print(f'Too many columns to plot. Showing the first {self.max_plots} plots.')
                break

            row_index, column_index = divmod(i, self.plots_per_row)
            axe = axes[column_index] if number_of_rows == 1 else axes[row_index, column_index]

            if column_type in ['number', 'datetime64']:
                sns.histplot(x=col, data=df, ax=axe)
            else:
                sns.countplot(x=col, data=df, ax=axe)

            axe.set_title(title_format.format(col))

        if plot_count % self.plots_per_row != 0:
            number_to_remove = self.plots_per_row - (plot_count % self.plots_per_row)
            row_index = number_of_rows - 1
            for j in range(number_to_remove):
                column_index = -(j + 1)
                axe = axes[column_index] if number_of_rows == 1 else axes[row_index, column_index]
                figure.delaxes(axe)

        plt.tight_layout()
        plt.show()
    
    def _visualize_correlations(self, df: DataFrame) -> None:
        numeric_df = df.select_dtypes(include=['number'])
        if len(numeric_df) < 2:
            return None

        corr = numeric_df.corr()

        mask = np.zeros_like(corr, dtype=bool)
        mask[np.triu_indices_from(mask)] = True

        plt.subplots(figsize=(self.figure_size, self.figure_size))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.heatmap(corr, mask=mask, cmap=cmap, center=0, square=True, linewidths=.5, cbar_kws={'shrink': .5})
        plt.show()
