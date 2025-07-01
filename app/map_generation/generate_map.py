import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import calendar
import sqlite3
from adjustText import adjust_text
from matplotlib.lines import Line2D


def get_coordinates(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM '{table_name}'")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    conn.close()

    data_by_column = {col: [] for col in column_names}
    for row in rows:
        for col, val in zip(column_names, row):
            data_by_column[col].append(val)

    return data_by_column


def setup_map(lats, lons, months, years, map_name):
    formatted_months = [
        calendar.month_name[int(month)][:3] for month in months
    ]

    plt.figure(figsize=(30, 15))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.BORDERS)
    ax.gridlines(draw_labels=True)
    plt.title(map_name.title())

    ax.scatter(
        lons, lats, color="red", s=50, marker="o", transform=ccrs.PlateCarree()
    )
    for i in range(len(lons) - 1):
        ax.annotate(
            "",
            xy=(lons[i + 1], lats[i + 1]),
            xytext=(lons[i], lats[i]),
            arrowprops=dict(arrowstyle="->", color="blue", linewidth=2),
            transform=ccrs.PlateCarree()
        )

    texts = []
    for i in range(len(lats)):
        texts.append(
            ax.text(
                lons[i] + 1, lats[i],
                f"{i+1}",
                transform=ccrs.PlateCarree()
            )
        )
    adjust_text(texts, ax=ax)

    buffer = 8
    ax.set_extent([
        min(lons) - buffer,
        max(lons) + buffer,
        min(lats) - buffer,
        max(lats) + buffer
    ], crs=ccrs.PlateCarree())

    legend_elements = [
        Line2D(
            [0], [0], color='none',
            label=f"{i+1}: {formatted_months[i]} {years[i]}"
        ) for i in range(len(lats))
    ]
    ax.legend(
        handles=legend_elements, loc='best', title="Arrow Number: Date"
        )

    save_dir_path = "saved_maps/" + map_name + ".png"
    plt.savefig(save_dir_path, bbox_inches="tight")


def generate_map(table_name, db_path="../../database/coordinates.db"):
    data = get_coordinates(db_path, table_name)
    setup_map(
        data["latitude"], data["longitude"], data["month"], data["year"],
        table_name
    )


if __name__ == "__main__":
    generate_map("Common_Terns")
