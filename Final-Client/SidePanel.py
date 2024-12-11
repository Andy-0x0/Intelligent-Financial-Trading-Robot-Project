import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from time import time

CSV_PATH = 'test_data.csv'


class Sampler:
    def __init__(self, df, step):
        self.df_source = df
        self.step = step

    def subsample(self):
        df_sampled = self.df_source.iloc[::self.step, :]
        return df_sampled


class Drawer:
    def __init__(self, df:pd.DataFrame):
        self.ori_df = df
        self._config()

    def _config(self, step=5):
        sampler = Sampler(self.ori_df, step)
        self.ori_df = sampler.subsample()

        # self.ori_df = self.ori_df.set_index('date')
        # self.ori_df.index = pd.to_datetime(self.ori_df.index)
        self.ori_df = self.ori_df.interpolate(method='akima').ffill().bfill()

    def _find_lowest_boundary(self):
        min_val = self.ori_df.iloc[:, 0].min()

        for col in self.ori_df.columns:
            new_min_val = self.ori_df.loc[:, col].min()
            if min_val > new_min_val:
                min_val = new_min_val
        return min_val

    def draw(self):
        fig, ax = plt.subplots(figsize=(10, 6))

        fig.patch.set_facecolor('#f0f0f0')
        ax.set_facecolor('#f0f0f0')

        colors = ['#0066cc', '#ff9933', '#339966']
        lines = []
        for i, column in enumerate(self.ori_df.columns):
            line, = ax.plot(self.ori_df.index, self.ori_df[column], lw=0.97, color=colors[i], label=column)
            lines.append(line)

            y = self.ori_df[column].values
            lower_bound = self._find_lowest_boundary()
            ax.fill_between(self.ori_df.index, y, lower_bound, color=colors[i], alpha=0.2,
                            where=(y > lower_bound), interpolate=True)

        ax.set_title('Test Data', fontsize=15, pad=20)
        ax.set_xlabel('Date', fontsize=12, labelpad=10)
        ax.set_ylabel('Value', fontsize=12, labelpad=10)

        ax.grid(True, axis='y', linestyle='--', linewidth=0.5)
        ax.grid(False, axis='x')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(False)

        ax.legend(handles=lines, fontsize=10, shadow=True, frameon=False)

        plt.show()


if __name__ == "__main__":
    

    start = time()

    drawer = Drawer(CSV_PATH)
    # drawer.show_info()
    drawer.draw()

    end = time()

    print(f'Time Consumption: {end - start:.3f}s')
