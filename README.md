![](Assets/Roller_Coaster_Data_Analysis_—_Python_EDA_Project.png)

### 🎢 *Exploring the evolution of roller coaster designs using Python & Pandas*

## 📌 Project Overview


This project demonstrates an end-to-end **Exploratory Data Analysis (EDA)** pipeline on a dataset of roller coasters. It highlights the trends in design, performance, and engineering characteristics over time.

**Key Skills Demonstrated:**
- Data cleaning & preprocessing (Pandas)
- Data visualization (Matplotlib & Seaborn)
- Aggregation & statistical analysis
- Correlation & trend analysis by decade
- Reporting with ydata-profiling

---

## 🔧 Tools & Libraries

```python
pandas, matplotlib, seaborn, ydata_profiling
```

📁 Dataset [Download](https://www.kaggle.com/datasets/robikscube/rollercoaster-database)

🧩 Step-by-Step Process

1. 📥 Data Understanding

- Load the dataset with Pandas

- Explore the dataset shape, column types, and missing values

- Display descriptive statistics and top rows

    ```python
    df = pd.read_csv("coaster_db.csv")

    print(df.shape)
    print(df.head(10))
    print(df.columns)
    print(df.dtypes)
    print(df.describe())
    ```


Inspect structurer 

2. 🧹 Data Cleaning & Preparation

- Drop irrelevant columns to focus on key engineering and location metrics

    ```python
    df = df[[
    'coaster_name','Location','Status','Manufacturer','year_introduced', 'latitude', 'longitude','Type_Main','opening_date_clean','speed_mph','height_ft','Inversions_clean', 'Gforce_clean'
    ]].copy()
    ```
- Convert data types (e.g., date fields)

    ```python
    df["opening_date_clean"] = pd.to_datetime(df["opening_date_clean"])
    ```

- Rename columns for consistency and readability

    ```python
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
    ```

- Handle missing values using mean/mode imputation
    
    ```python

    for col in ['Latitude', 'Longitude', 'Speed MPH', 'Height FT', 'Gforce Clean']:
    df[col] = df[col].fillna(df[col].mean())

    for col1 in ['Status', 'Manufacturer', 'Opening Date Clean']:
    df[col1] = df[col1].fillna(df[col1].mode()[0])
    ```

- Remove duplicate entries

    ```python
    df = df.loc[~df.duplicated(subset=['Coaster Name', 'Location', 'Opening Date Clean'])] \
       .reset_index(drop=True)

    df = df.sort_values('Year Introduced', ascending=True) \
       .drop_duplicates(subset=['Coaster Name', 'Location', 'Opening Date Clean'], keep='first') \
       .reset_index(drop=True)
    ```
3. 📊 Exploratory Visualizations
    
- Yearly trends in coaster introductions

    
    ```python
    ax = df['Year Introduced'].value_counts().head(10).plot(kind='bar', title="Top 10 Year Introduced")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    plt.show()
    ```


![](Assets/Top_10_Year_Introduced.png)

- Distribution of coaster speeds and heights

    ```python
    ax = df['Speed MPH'].plot(kind='hist', bins=20, title="Speed MPH")
    ax.set_xlabel(["Speed MPH"])
    ```

    ![Speed MPH](Assets/Speed_MPH_Hist.png)

    ```python
    ax = df['Speed MPH'].plot(kind='kde', title="Speed MPH")
    ax.set_xlabel('Speed MPH')
    plt.show()
    ```

    ![Speed MPH](Assets/Speed_MPH_Kde.png)

- Categorical distributions (e.g., coaster types)

    ```python
    ax = df['Type Main'].value_counts().plot(kind='bar')
    plt.show()
    ```

    ![alt text](Assets/Three_Types_Bar.png)
    

- Scatterplots: Speed vs Height, with color by year
    
    ```python
    df.plot(kind='scatter', x='Speed MPH', y='Height FT', title='Coaster Speed vs Height')
    ```

    ![Coaster Speed vs Height](Assets/Coaster_Speed_vs_Height_Plot.png)

    ```python
    ax = sns.scatterplot(x='Speed MPH', y='Height FT', hue='Year Introduced', data=df)
    ax.set_title('Coaster Speed vs Height')
    ```

    ![Coaster Speed vs Height](Assets/Coaster_Speed_vs_Height_SNS.png)
    
4. 🔗 Feature Relationships
- Pair plots by Type
    
    ```python
    sns.pairplot(df,
             vars=['Year Introduced', 'Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean'],
             hue='Type Main')
    plt.show()
    ```
    ![alt text](Assets/Pairplot_By_Types.png)
- Correlation heatmap of key numeric features

    ```python
    df_corr = df[['Year Introduced', 'Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean']].dropna().corr()
    sns.heatmap(df_corr, annot=True)
    plt.show()
    ```
    ![](Assets/HeatMap.png)
5. 📈 Advanced Trend Analysis
- Average Speed by Coaster Type
    ```python
    compared = df.groupby('Type Main')['Speed MPH'].mean().sort_values(ascending=False)

    df['Decade'] = ((df['Year Introduced'] // 10) * 10).astype('str') + "s"

    avg_by_decade = df.groupby('Decade')[['Year Introduced', 'Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean']] \
                    .mean().round(2).reset_index()
    ```

    ![alt text](Assets/AVG_by_decade.png)
- Design evolution by decade (e.g., higher speeds and heights in 2000s+)
    
    ```python
    ax = avg_by_decade.plot(
    x='Decade',
    y=['Speed MPH', 'Height FT', 'Inversions Clean', 'Gforce Clean'],
    kind='line',
    marker=0,
    title='Roller Coaster Design Trend By Decade'
    )
    ax.set_ylabel('Average Value')
    plt.grid(True)
    plt.show()
    ```

    ![alt text](Assets/Roller_Coaster_Design_Trend_By_Decade.png)

- Multi-metric line and bar charts for insights across decades
    
    ```python
    ax = avg_by_decade.plot(kind='bar', x='Decade', y='Speed MPH', title='Average Speed By Decade')
    plt.show()
    ```

    ![alt text](Assets/Average_Speed_By_Decade.png)

🔍 Key Insights  
- Coaster speed and height have significantly increased over decades

- Types of coasters (e.g., steel vs wooden) show distinct design trends

- Modern coasters are not only faster but also more intense (higher G-force)

📝 Bonus: Automated EDA Report
- An optional HTML report was generated using ydata_profiling for deeper automated insight.

```python
profile = ProfileReport(df, title="EDA Report")
profile.to_file("EDA_Report.html")
```
