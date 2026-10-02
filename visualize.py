import matplotlib.pyplot as plt
import pandas as pd
import os

def visualization(column, df, df2, ab, figures_dir, ignore_index=True):
    column_show = str(column)[:-3].split("/")[-1]

    plt.figure(figsize=(12, 6), dpi=150)
    plt.plot(
        df["年/Year"],
        df[column],
        color='#1f77b4',
        alpha=0.3,
        linewidth=1,
        label=f"Year-{column_show}",
    )
    plt.scatter(
        df["年/Year"],
        df[column],
        color='#1f77b4',
        alpha=0.6,
        s=15,
    )

    df['Rolling_10Y'] = df[column].rolling(window=10, min_periods=1).mean()
    plt.plot(
        df["年/Year"],
        df['Rolling_10Y'],
        color='#2ca02c',
        linewidth=2.5,
        label='10-Year Moving Average',
    )

    ab = list(ab)
    a = ab[0][0]
    b = ab[0][1]
    X_hist = df[['年/Year']].values
    y_fit = a * X_hist + b
    plt.plot(
        df['年/Year'],
        y_fit,
        color='#d62728',
        linestyle='--',
        linewidth=2,
        label='Linear Regression Fit',
    )

    df3 = pd.concat([df, df2], ignore_index=True)
    plt.plot(
        df3["年/Year"],
        df3[column],
        color='#1f77b4',
        linestyle=':',
        linewidth=2,
    )
    plt.scatter(
        df2["年/Year"],
        df2[column],
        color='#d62728',
        marker='.',
        s=80,
        zorder=5,
        label='5-Year Prediction',
    )

    plt.title(
        f'Hong Kong Annual {column_show} Historical Trend & 5-Year Forecast',
        fontsize=14,
        fontweight='bold',
        pad=15,
    )
    plt.xlabel('Year', fontsize=11)
    plt.ylabel(f'{column_show}', fontsize=11)

    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)

    plt.tight_layout()

    filename = f'Annual_HK_{column_show.replace(" ", "_")}_Analysis_ALL.png'
    save_path = os.path.join(figures_dir, filename)
    plt.savefig(save_path, dpi=300)

    print(f"已完成的圖表/Generated Figure: Annual_HK_{column_show.replace(' ', '_')}_Analysis_ALL.png")