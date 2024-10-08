import pandas as pd
import scipy.stats as stats

# Load the datasets
girls_village_data = pd.read_excel(r'C:\Users\ASUS\OneDrive\Desktop\girls village.xlsx')
girls_city_data = pd.read_excel(r'C:\Users\ASUS\OneDrive\Desktop\girlscity.xlsx')
boys_village_data = pd.read_excel(r'C:\Users\ASUS\OneDrive\Desktop\boysvillage.xlsx')
boys_city_data = pd.read_excel(r'C:\Users\ASUS\OneDrive\Desktop\boyscity.xlsx')

# Combine the data for analysis
combined_data = pd.DataFrame({
    'Total': pd.concat([boys_village_data['TOTAL'], girls_village_data['TOTAL']]),
    'Stress': pd.concat([boys_village_data['STRESS'], girls_village_data['STRESS']]),
    'Group': (
        ['Boys village'] * len(boys_village_data) + 
        ['Girls village'] * len(girls_village_data)
    )
})

# Perform ANOVA
anova_result = stats.f_oneway(
    combined_data[combined_data['Group'] == 'Boys village']['Total'],
    combined_data[combined_data['Group'] == 'Girls village']['Total'])

# Calculate sum_sq and df
ss_between = sum((combined_data.groupby('Group')['Total'].mean() - combined_data['Total'].mean())**2) * len(girls_village_data)
ss_within = sum((combined_data['Total'] - combined_data.groupby('Group')['Total'].transform('mean'))**2)
df_between = combined_data['Group'].nunique() - 1
df_within = len(combined_data) - combined_data['Group'].nunique()

# Create ANOVA table
anova_table = pd.DataFrame({
    'Source': ['Between Groups', 'Within Groups'],
    'Sum_sq': [ss_between, ss_within],
    'df': [df_between, df_within],
    'F-Value': [anova_result.statistic, 'N/A'],
    'P-Value': [anova_result.pvalue, 'N/A']
})

print(anova_table)
