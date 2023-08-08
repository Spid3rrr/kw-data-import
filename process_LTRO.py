# Imports
import decimal
import math
import dateutil.parser


import pandas as pd
import numpy as np

# LTRO functions
import utils.LTROutils as LT


#  Importing data from LTRO has the following steps:
# 1. Define files received from LTRO
# 2. Clean files (clean & rename columns, delete empty rows, remove anomalous sales)
# 3. use standard property_type
# 4. process duplicates
# 5. use standard parishes

# 1. Files from LTRO:
recent_LTRO_data = "./data/LTRO/LTRO_2018_2022.xlsx"
old_processed_LTRO_data = "./data/LTRO/LTRO_2018.csv"
latest_LTRO_data = "./data/LTRO/LTRO_2022.xlsx"

df = pd.read_excel(recent_LTRO_data, header=None, skiprows=9)
older_ltro = pd.read_csv(old_processed_LTRO_data)
dflast =  pd.read_excel(latest_LTRO_data, header=None, skiprows=9)

# 2. Clean Files
df = LT.clean_ltro_data(df)
dflast = LT.clean_ltro_data(dflast)


df = pd.concat([older_ltro, df, dflast])
df['registration_date'] =  pd.to_datetime(df['registration_date'], format='%Y-%m-%d').dt.date
df.reset_index(drop=True, inplace=True)


print('\n{} sales imported between dates: {} and {} \n'.format(df.shape[0], 
                                                               df.registration_date.min(), 
                                                               df.registration_date.max()))

# 3. a new columns called "property_type"
# is defined. It will contain either
# "fractional", "land", "house", "condo" or False
df = LT.identify_fractionals(df)
df = LT.identify_lands(df)
df = LT.identify_houses(df)
df = LT.identify_condos(df)


# 4. Remove Duplicates
LTRO_entries = df.shape[0]
df = df.drop_duplicates(subset=['application_number','registration_date', 
                                'acquisition_date',
                                'assessment_number_list',
                                'price'], 
                                keep='first', )

print(LTRO_entries - df.shape[0], "duplicates removed")

if df[df['application_number'].duplicated()].shape[0] > 0:
    print("WARNING, some sales HAVE DUPLICATES")

# keep=False to show all duplicate entries (not just the ones after the first)
to_process = df[df['application_number'].duplicated(keep=False)].shape[0]

df = LT.process_duplicates(df)
print(to_process, " rows processed for duplicates")

lv = pd.read_csv("./data/kw-properties.csv")
df = LT.add_arv_to_ltro(df,lv)


# improve sales property type data
df = LT.clean_property_type(df, lv)

# Sanity check:
# keep only properties such that the sales price is more than 2 years of rent.
df = df[~(df['combined_arv']*2 >= df['price'])] #  & (df.property_type != 'fractional')]

# create a column with surface area in hectares
df = LT.clean_area(df)

# 5. Use standard parishes
df = LT.simplify_parishes(df)

# Save to CSV
final_df = df[["application_number", "registration_date", "parish",
               "address", "parcel_area", "parcel_area_ha",
              "assessment_number_list", "acquisition_date",
               "price", "arv", "combined_arv", "property_type"]].copy(deep=False)

final_df.assessment_number_list = final_df.assessment_number_list.apply(LT.get_assessment_number)

# try to find the assessment number or address
# for properties identified only with their parcel ID (like PA-2037)
final_df = LT.clean_parcel_id_based_addresses(final_df)
# Revisit sales data to improve property type
final_df = LT.clean_property_type(final_df, lv)

final_df.to_csv("./data/kw-sales.csv", index=False)

print("\n >> LTRO DATA IMPORTED << \n")


