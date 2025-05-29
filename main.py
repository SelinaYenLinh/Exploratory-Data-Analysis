import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ydata_profiling import ProfileReport

# ===================================
# Step 1: Data Understanding
# ===================================

df = pd.read_csv("coaster_db.csv")

# ===================================
# Step 2: Data Preparation
# ===================================

# Select relevant columns
df = df[[
    'coaster_name', 'Location', 'Status', 'Manufacturer',
    'year_introduced', 'latitude', 'longitude',
    'Type_Main', 'opening_date_clean',
    'speed_mph', 'height_ft', 'Inversions_clean', 'Gforce_clean'
]].copy()

# Convert data types
df["opening_date_clean"] = pd.to_datetime(df["opening_date_clean"])

# Rename columns for better readability
df = df.rename(columns={
    'coaster_name': 'Coaster Name',
    'year_introduced': 'Year Introduced',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'Type_Main': 'Type Main',
    'opening_date_clean': 'Opening Date Clean',
    'speed_mph': 'Speed MPH',
    'height_ft': 'Height FT',
    'Inversions_clean': 'Inversions Clean',
    'Gforce_clean': 'Gforce Clean'
})

# ===================================
# Step 3: Handling Missing Values
# ===================================

# Fill missing numeric columns with the mean
for col in ['Latitude', 'Longitude', 'Speed MPH', 'Height FT', 'Gforce Clean']:
    df[col] = df[col].fillna(df[col].mean())

# Fill missing categorical/date columns with the mode
for col in ['Status', 'Manufacturer', 'Opening Date Clean']:
    df[col] = df[col].fillna(df[col].mode()[0])

# ===================================
# Step 4: Handling Duplicates
# ===================================

# Drop exact duplicate records
df = df.loc[~df.duplicated(subset=['Coaster Name', 'Location', 'Opening Date Clean'])] \
       .reset_index(drop=True)

# Keep the first occurrence by year if multiple entries exist
df = df.sort_values('Year Introduced', ascending=True) \
       .drop_duplicates(subset=['Coaster Name', 'Location', 'Opening Date Clean'], keep='first') \
       .reset_index(drop=True)

# ===================================
# Step 5: Feature Understanding
# ===================================

# Group data to analyze by coaster and location
df_grouped = df.groupby(['Coaster Name', 'Location'], as_index=False).agg({
    'Speed MPH': 'max',
    'Height FT': 'mean',
    'Gforce Clean': 'mean'
})

# Create variations for first/last duplicates if needed
df_keepfirst = df.drop_duplicates(subset=['Coaster Name', 'Location', 'Opening Date Clean'], keep='first')
df_keeplast = df.drop_duplicates(subset=['Coaster Name', 'Location', 'Opening Date Clean'], keep='last')

# ===================================
# Step 6: Advanced Analysis
# ===================================

# Compare average speed between coaster types (e.g., Wood vs Steel)
avg_speed_by_type = df.groupby('Type Main')['Speed MPH'].mean().sort_values(ascending=False)

# Create a new column for decade
df['Decade'] = ((df['Year Introduced'] // 10) * 10).astype(str) + "s"

# Calculate average design features by decade
avg_by_decade = df.groupby('Decade')[['Year Introduced', 'Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean']] \
                  .mean().round(2).reset_index()

# Plot average trends by decade
# Uncomment to visualize

# ax = avg_by_decade.plot(
#     x='Decade',
#     y=['Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean'],
#     kind='line',
#     marker='o',
#     title='Roller Coaster Design Trends by Decade'
# )
# ax.set_ylabel('Average Value')
# plt.grid(True)
# plt.show()

# Generate an EDA profile report (optional, takes time)
# profile = ProfileReport(df, title="Roller Coaster EDA Report")
# profile.to_file("EDA_Report.html")
