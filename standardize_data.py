import pandas

# Weight goes to metric_ton
conversion_table = {
    "kg": {
        "ton": 1000,
        "short_ton": 907.18,
        "kg": 1,
        "lb": 0.453592,
        "pound": 0.453592,
        "gram": 0.001,
        "kilogram": 1,
        "ounce": 0.0283495,
        "metric_ton": 1000
    },
    "L": {
        "quart": 1.057,
        "pint": 0.473176,
        "cubic_centimeter": 0.001,
        "cubic_foot": 28.3168,
        "cubic_feet": 28.3168,
        "liter": 1,
        "milliliter": 0.001,
        "gallon": 3.78541,
        "L": 1
    },
    "kWh": {
        "joule": 1/3600000,
        "kilowatt_hour": 1,
        "british_thermal_unit": 0.000293071,
        "kWh": 1
    },
    "hr": {
        "hour": 1,
        "year": 8766,
        "day": 24,
        "week": 168,
        "month": 730.5,
        "minute": 60,
        "hr": 1
    },
    "ft": {
        "kilometer": 3280.84,
        "yard": 3,
        "meter": 3.28084,
        "inch": 0.0833333,
        "mile": 5280,
        "foot": 1,
        "ft": 1
    }
}


def standardize_data():
    df1 = pandas.read_csv("table1.csv", sep="|", skiprows=1)
    df3 = pandas.read_csv("table3.csv", sep="|", skiprows=1)

    # Add Resource-Sector column
    df1["Key"] = df1["Resource"] + "_" + df1["Sector"]
    df3["Key"] = df3["Resource"] + "_" + df3["Sector"]

    df1["Key"] = df1["Key"].str.replace(" ", "_")
    df1["Key"] = df1["Key"].str.replace("-", "_")
    df3["Key"] = df3["Key"].str.replace(" ", "_")
    df3["Key"] = df3["Key"].str.replace("-", "_")

    # Convert Unit and Quantity
    df3 = df3.apply(lambda x: change_unit(x, df1), axis=1)

    # Add UnitPrice column
    df1["UnitPrice"] = df1["Total Value ($CAD)"]/df1["Quantity"]

    df1.to_csv('table1_clean.csv', index=False)
    df3.to_csv('table3_clean.csv', index=False)



def change_unit(row, df1):
    # The resource unit
    res_unit = df1[df1["Key"] == row["Key"]].iloc[0].Unit
    
    for i in range(2):
        if res_unit == row.Unit:
        # Already in the right unit
            return row
        
        conv_value, new_unit = get_conversion_value(row.Unit, res_unit)
        row.Quantity *= conv_value
        row.Unit = new_unit
    
    return row
    

def get_conversion_value(original_unit, res_unit):
    for key, units in conversion_table.items():

        if original_unit == key:
            return 1/units[res_unit], res_unit
        
        if original_unit in units.keys():
            return units[original_unit], key


if __name__ == "__main__":
    standardize_data()
