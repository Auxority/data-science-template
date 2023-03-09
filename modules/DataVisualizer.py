import seaborn as sns
import numpy as np
from pandas import DataFrame
from matplotlib import pyplot as plt
from matplotlib import axes

class DataVisualizer:
    def __init__(
        self,
        max_plots: int = 30,
        plots_per_row: int = 3,
        figure_size: int = 5,
        max_unique_labels: int = 10,
        max_label_length: int = 8,
    ):
        self.max_plots = max_plots
        self.plots_per_row = plots_per_row
        self.figure_size = figure_size
        self.max_unique_labels = max_unique_labels
        self.max_label_length = max_label_length
        sns.set_style('darkgrid')
    
    def visualize(self, df: DataFrame) -> None:
        self._visualize_distributions(df, 'number')
        self._visualize_distributions(df, 'object')
        self._visualize_distributions(df, 'datetime64')
        self._visualize_correlations(df)

    def _visualize_distributions(self, df: DataFrame, column_type: str) -> None:
        target_columns = df.select_dtypes(include=[column_type]).columns
        number_of_plots = len(target_columns)
        number_of_rows = int(np.ceil(number_of_plots / self.plots_per_row))
        figure_width, figure_height = self._calculate_figure_size(number_of_rows)
        figure, ax = self._create_subplots(number_of_rows, figure_width, figure_height)

        self._create_plots(
            df=df,
            col=target_columns,
            ax=ax,
            column_type=column_type,
            figure=figure,
            target_columns=target_columns,
            number_of_rows=number_of_rows,
        )

        self._remove_empty_plots(
            figure=figure,
            ax=ax,
            number_of_plots=number_of_plots,
            number_of_rows=number_of_rows
        )

        plt.tight_layout()
        plt.show()
    
    def _visualize_correlations(self, df: DataFrame) -> None:
        numeric_df = df.select_dtypes(include=['number', 'datetime64'])
        if len(numeric_df) < 2:
            return None

        corr = numeric_df.corr(numeric_only=True)
        mask = np.zeros_like(corr, dtype=bool)
        mask[np.triu_indices_from(mask)] = True
        cmap = sns.diverging_palette(230, 20, as_cmap=True)

        plt.subplots(figsize=(self.figure_size, self.figure_size))
        sns.heatmap(corr, mask=mask, cmap=cmap, center=0, square=True, linewidths=.5, cbar_kws={'shrink': .5})
        plt.title('Correlation matrix')
        plt.show()

    def _calculate_figure_size(self, number_of_rows: int) -> tuple:
        figure_width = np.multiply(self.figure_size, self.plots_per_row)
        figure_height = np.multiply(self.figure_size, number_of_rows)
        return figure_width, figure_height

    def _create_histogram(self, df: DataFrame, col: str, ax: axes, column_type: str) -> None:
        sns.histplot(x=col, data=df, ax=ax)
        ax.set_title(f'Distribution of {col}')
        min_max_difference = df[col].max() - df[col].min() if column_type == 'number' else df[col].max().timestamp() - df[col].min().timestamp()
        if min_max_difference > 1000:
            ax.set_yscale('log')

        is_skewed = df[col].skew() > 1 or df[col].skew() < -1 if column_type == 'number' else False
        if is_skewed:
            ax.set_xscale('log')
    
    def _create_bar_plot(self, df: DataFrame, col: str, ax: axes, figure: plt.figure) -> None:
        unique_labels = df[col].unique()
        value_counts = df[col].value_counts()

        x_values = unique_labels
        y_values = value_counts.values

        if len(unique_labels) > self.max_unique_labels:
            top_values = value_counts.head(self.max_unique_labels)
            x_values = top_values.index.values
            y_values = top_values.values
            ax.set_title(f'Top {self.max_unique_labels} {col}')
            if top_values.max() - top_values.min() > 1000:
                ax.set_yscale('log')
        else:
            ax.set_title(f'Distribution of {col}')
            if value_counts.max() - value_counts.min() > 1000:
                ax.set_yscale('log')

        if any([len(str(x)) > 4 for x in x_values]):
            ax.tick_params(axis='x', rotation=90, labelsize=8)
            figure.set_figheight(figure.get_figheight() + 1)

        sns.barplot(x=x_values, y=y_values, ax=ax)
    
    def _create_plots(
            self,
            df: DataFrame,
            col: str,
            ax: axes,
            column_type: str,
            figure: plt.figure,
            target_columns: list,
            number_of_rows: int
        ) -> None:
        for i, col in enumerate(target_columns):
            if i >= self.max_plots:
                print(f'Too many columns to plot. Showing the first {self.max_plots} plots.')
                break

            row_index, position_in_row = divmod(i, self.plots_per_row)
            current_ax = ax[position_in_row] if number_of_rows == 1 else ax[row_index, position_in_row]

            if column_type == 'number' or column_type == 'datetime64':
                self._create_histogram(df=df, col=col, ax=current_ax, column_type=column_type)
            else:
                self._create_bar_plot(df=df, col=col, ax=current_ax, figure=figure)

    def _create_subplots(
            self,
            number_of_rows: int,
            figure_width: int,
            figure_height: int
        ) -> tuple:
        return plt.subplots(
            nrows=number_of_rows,
            ncols=self.plots_per_row,
            figsize=(figure_width, figure_height)
        )

    def _remove_empty_plots(
            self, figure: plt.figure,
            ax: axes,
            number_of_plots: int,
            number_of_rows: int
        ) -> None:
        if number_of_plots % self.plots_per_row != 0:
            number_to_remove = self.plots_per_row - (number_of_plots % self.plots_per_row)
            row_index = number_of_rows - 1
            for j in range(number_to_remove):
                position_in_row = -(j + 1)
                current_ax = ax[position_in_row] if number_of_rows == 1 else ax[row_index, position_in_row]
                figure.delaxes(current_ax)
