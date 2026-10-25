import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("SolarPrediction.csv")
dates=df["Data"].str.split().str[0]
df["DateTime"]=pd.to_datetime(dates+" "+df["Time"])
df=df.sort_values("DateTime")
df.reset_index(drop=True)
df["Hour"] = df["DateTime"].dt.hour
week1 = df[df["DateTime"] < (df["DateTime"].min() + pd.Timedelta(days=7))]

plt.figure(figsize=(12, 4))
plt.plot(week1["DateTime"], week1["Radiation"])
plt.xlabel("Time")
plt.ylabel("Radiation")
plt.title("Solar radiation over the first week")
plt.savefig("radiation_vs_time.png", dpi=150, bbox_inches="tight")
plt.show()

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
for ax, col in zip(axes, ["Temperature", "Humidity", "Speed"]):
    ax.scatter(df[col], df["Radiation"], s=3, alpha=0.3)
    ax.set_xlabel(col)
    ax.set_ylabel("Radiation")
    ax.set_title(f"Radiation vs {col}")
plt.tight_layout()
plt.savefig("radiation_vs_variables.png", dpi=150, bbox_inches="tight")
plt.show()

hourly = df.groupby("Hour")["Radiation"].mean()
plt.figure(figsize=(10, 4))
plt.bar(hourly.index, hourly.values)
plt.xlabel("Hour of day")
plt.ylabel("Mean radiation")
plt.title("Average radiation by hour of day")
plt.xticks(range(0, 24))
plt.savefig("radiation_by_hour.png", dpi=150, bbox_inches="tight")
plt.show()

cols = ["Radiation", "Temperature", "Pressure", "Humidity", "WindDirection(Degrees)", "Speed"]
corr = df[cols].corr()
print(corr["Radiation"].sort_values(ascending=False))
print("-------------------------------------------------")

plt.figure(figsize=(7, 6))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="Correlation")
plt.xticks(range(len(cols)), cols, rotation=90)
plt.yticks(range(len(cols)), cols)
for i in range(len(cols)):
    for j in range(len(cols)):
        plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
plt.title("Correlation heatmap")
plt.savefig("correlation_heatmap.png", dpi=150, bbox_inches="tight")
plt.show()

df.boxplot(column="Radiation", by="Hour", figsize=(12, 5), grid=False)
plt.suptitle("")
plt.title("Radiation distribution by hour of day")
plt.xlabel("Hour of day")
plt.ylabel("Radiation")
plt.savefig("radiation_boxplot_by_hour.png", dpi=150, bbox_inches="tight")
plt.show()

hourly_rad = df.groupby("Hour")["Radiation"].mean()
hourly_temp = df.groupby("Hour")["Temperature"].mean()
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(hourly_rad.index, hourly_rad.values, color="orange", marker="o")
ax1.set_xlabel("Hour of day")
ax1.set_ylabel("Mean radiation (W/m²)", color="orange")
ax2 = ax1.twinx()
ax2.plot(hourly_temp.index, hourly_temp.values, color="red", marker="s")
ax2.set_ylabel("Mean temperature", color="red")
plt.title("Radiation and temperature by hour of day")
ax1.set_xticks(range(0, 24))
plt.savefig("radiation_temp_lag.png", dpi=150, bbox_inches="tight")
plt.show()

df["Date"] = df["DateTime"].dt.date
daily = df.groupby("Date")["Radiation"].agg(max_radiation="max", avg_radiation="mean")
best_date = daily["max_radiation"].idxmax()
print("DAILY MAXIMUM AND AVERAGE RADIATION FOR DATE WITH THE HIGHEST PEAK RADIATION")
print("best day:",best_date)
print(daily.loc[best_date])
print("-------------------------------------------------")

day_df = df[df["Date"] == best_date]
peak_row = day_df.loc[day_df["Radiation"].idxmax()]
print("Best Day:",peak_row["Date"])
print("-------------------------------------------------")

print("WEATHER CONDITIONS DURING BEST DAY")
print("Peak time:", peak_row["DateTime"])
print("Radiation:", peak_row["Radiation"])
print("Temperature:", peak_row["Temperature"])
print("Humidity:", peak_row["Humidity"])
print("Wind speed:", peak_row["Speed"])
print("-------------------------------------------------")

sunrise = pd.to_datetime(str(best_date) + " " + peak_row["TimeSunRise"])
sunset = pd.to_datetime(str(best_date) + " " + peak_row["TimeSunSet"])
peak_time = peak_row["DateTime"]
after_sunrise = peak_time - sunrise
daylight = sunset - sunrise
print("COMPARISON BETWEEN SUNRISE, SUNSET AND PEAK TIME")
print("Sunrise:", sunrise.time(), "| Sunset:", sunset.time())
print("Peak occurred after sunrise by:", after_sunrise)
print("In hours:", round(after_sunrise.total_seconds() / 3600, 2))
print("Fraction of daylight elapsed at peak:", round(after_sunrise / daylight, 2))
print("-------------------------------------------------")

top5 = daily.nlargest(5, "avg_radiation")
print("TOP 5 DAYS WITH HIGHEST AVERAGE RADIATION")
print(top5)
print("-------------------------------------------------")
