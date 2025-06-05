import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from ydata_profiling import ProfileReport

# ======================================
# Step 1: Data Understanding
# ======================================

df = pd.read_csv("D:\Code\Exploratory-Data-Analysis\Dataset\coaster_db.csv")

# print(df.shape)
# print(df.head(10))
# print(df.columns)
# print(df.dtypes)
# print(df.describe())

# ======================================
# Step 2: Data Preparation
# ======================================

# Select relevant columns
df = df[[
    'coaster_name',
    # 'Length', 'Speed',
    'Location', 'Status',
    # 'Opening date',
    # 'Type',
    'Manufacturer',
    # 'Height restriction', 'Model', 'Height',
    # 'Inversions', 'Lift/launch system', 'Cost', 'Trains', 'Park section',
    # 'Duration', 'Capacity', 'G-force', 'Designer', 'Max vertical angle',
    # 'Drop', 'Soft opening date', 'Fast Lane available', 'Replaced',
    # 'Track layout', 'Fastrack available', 'Soft opening date.1',
    # 'Closing date', 'Opened', 'Replaced by', 'Website',
    # 'Flash Pass Available', 'Must transfer from wheelchair', 'Theme',
    # 'Single rider line available', 'Restraint Style',
    # 'Flash Pass available', 'Acceleration', 'Restraints', 'Name',
    'year_introduced', 'latitude', 'longitude',
    'Type_Main', 'opening_date_clean',
    # 'speed1', 'speed2', 'speed1_value', 'speed1_unit',
    'speed_mph',
    # 'height_value', 'height_unit',
    'height_ft',
    'Inversions_clean', 'Gforce_clean'
]].copy()

# Convert types 
df["opening_date_clean"] = pd.to_datetime(df["opening_date_clean"])

# Rename columns
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

# ======================================
# Check and Handle Missing Values
# ======================================

count = df.isnull().sum()
# print((count / df.count()) * 100)
# print(df[df.isnull().any(axis=1)])

# Fill missing numerical values with mean
for col in ['Latitude', 'Longitude', 'Speed MPH', 'Height FT', 'Gforce Clean']:
    df[col] = df[col].fillna(df[col].mean())

# Fill missing categorical/date values with mode
for col1 in ['Status', 'Manufacturer', 'Opening Date Clean']:
    df[col1] = df[col1].fillna(df[col1].mode()[0])

# print(df['Opening Date Clean'].mode())
# print(df.isnull().sum())

# ======================================
# Handle Duplicates
# ======================================

# print(df.loc[df.duplicated()])
# print(df.loc[df.duplicated(subset='Coaster Name')].head(5))
# print(df.query('Coaster Name == "Crystal Beach Cyclone"'))

df = df.loc[~df.duplicated(subset=['Coaster Name', 'Location', 'Opening Date Clean'])] \
       .reset_index(drop=True)

df = df.sort_values('Year Introduced', ascending=True) \
       .drop_duplicates(subset=['Coaster Name', 'Location', 'Opening Date Clean'], keep='first') \
       .reset_index(drop=True)

# ======================================
# Feature Grouping & Aggregation
# ======================================

df_grouped = df.groupby(['Coaster Name', 'Location'], as_index=False).agg({
    'Speed MPH': 'max',
    'Height FT': 'mean',
    'Gforce Clean': 'mean'
})

df_keepfirst = df.drop_duplicates(subset=['Coaster Name', 'Location', 'Opening Date Clean'], keep='first')
df_keeplast = df.drop_duplicates(subset=['Coaster Name', 'Location', 'Opening Date Clean'], keep='last')

# ======================================
# Step 3: Feature Understanding
# ======================================

# print(df['Year Introduced'].value_counts())

ax = df['Year Introduced'].value_counts().head(10).plot(kind='bar', title="Top 10 Year Introduced")
ax.set_xlabel("Year")
ax.set_ylabel("Count")
# plt.show()

ax = df['Speed MPH'].plot(kind='hist', bins=20, title="Speed MPH")
ax.set_xlabel(["Speed MPH"])
# plt.show()

ax = df['Speed MPH'].plot(kind='kde', title="Speed MPH")
ax.set_xlabel('Speed MPH')
# plt.show()

print(df['Type Main'].value_counts())
ax = df['Type Main'].value_counts().plot(kind='bar', title= "Three Types")
# plt.show()

# ======================================
# Step 4: Feature Relationships
# ======================================

df.plot(kind='scatter', x='Speed MPH', y='Height FT', title='Coaster Speed vs Height')

ax = sns.scatterplot(x='Speed MPH', y='Height FT', hue='Year Introduced', data=df)
ax.set_title('Coaster Speed vs Height')

sns.pairplot(df,
             vars=['Year Introduced', 'Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean'],
             hue='Type Main')
# plt.show()

df_corr = df[['Year Introduced', 'Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean']].dropna().corr()
sns.heatmap(df_corr, annot=True)
# plt.show()

# ======================================
# Step 5: Advanced Analysis
# ======================================

# Compare average speed by coaster type
compared = df.groupby('Type Main')['Speed MPH'].mean().sort_values(ascending=False)
# print(compared)

# Analyze trends by decade
df['Decade'] = ((df['Year Introduced'] // 10) * 10).astype('str') + "s"
# print(df['Decade'])

avg_by_decade = df.groupby('Decade')[['Year Introduced', 'Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean']] \
                  .mean().round(2).reset_index()
# print(avg_by_decade)

ax = avg_by_decade.plot(
    x='Decade',
    y=['Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean'],
    kind='line',
    marker=0,
    title='Roller Coaster Design Trend By Decade'
)
ax.set_ylabel('Average Value')
plt.grid(True)
# plt.show()

ax = avg_by_decade.plot(kind='bar', x='Decade', y='Speed MPH', title='Average Speed By Decade')
# plt.show()

# ======================================
# Generate EDA Report (optional)
# ======================================

profile = ProfileReport(df, title="EDA Report")
profile.to_file("EDA_Report.html")
