import pulp as pulp
import pandas as pd
import json


def algo4():


    df1 = pd.read_csv("table1_clean.csv")
    df2 = pd.read_csv("table2.csv", skiprows=1, sep="|")
    df3 = pd.read_csv("table3_clean.csv")



    ressources = {}
    countries = {}
    vars = []



    #create variables that represent quantity of each resource in each country
    #Adds the variables to the ressources and countries dictionaries
    for index, row in df3.iterrows():
        name = row['Key']+"^^^"+row['Country']
        newVar = pulp.LpVariable(name, lowBound=0, upBound=row['Quantity'], cat='Continuous')
        if row['Key'] not in ressources:
            ressources[row['Key']] = []
        if row['Country'] not in countries:
            countries[row['Country']] = []
        ressources[row['Key']].append(newVar)
        countries[row['Country']].append(newVar)
        vars.append(newVar)

    # Create the 'prob' variable to contain the problem data
    # Objective function, maximize the sum of the unit price of each resource multiplied by the quantity of that resource
    prob = pulp.LpProblem("The Problem", pulp.LpMaximize)
    prob += pulp.lpSum([pulp.lpSum([df1.loc[df1['Key'] == resource.name.split('^^^')[0], 'UnitPrice'].values[0] * df3.loc[df3['Key'] == resource.name.split('^^^')[0], 'Urgency'].values[0] * resource for resource in countries[country]])/df2.loc[df2['Country'] == country, 'Target Donation ($CAD)'].values[0] for country in countries]) 
    #prob += pulp.lpSum([df1.loc[df1['Key'] == name, 'UnitPrice'].values[0] * pulp.lpSum(ressources[name]) for name in ressources])

    #Create constraints, each given ressources must be less than or equal to the total amount of that ressource
    for ressource in ressources:
        total = df1.loc[df1['Key'] == ressource, 'Quantity'].values[0]
        prob += pulp.lpSum(ressources[ressource]) <= total

    #Create constraints, total of donations per country cannot exceed target donation
    for country in countries:
        prob += pulp.lpSum([df1.loc[df1['Key'] == resource.name.split('^^^')[0], 'UnitPrice'].values[0] * resource for resource in countries[country]]) <= df2.loc[df2['Country'] == country, 'Target Donation ($CAD)'].values[0]
        



    prob.solve()

    res = {
        'MoneyPerCountry': {},
        'ResourcesPerCountryBySector': {}, #money per sector per country
        'CountryPerResource': {} #country per resource
    }
    #Create output JSON for visualization
    for country in countries:
        res['MoneyPerCountry'][country] = pulp.lpSum([df1.loc[df1['Key'] == resource.name.split('^^^')[0], 'UnitPrice'].values[0] * resource for resource in countries[country]]).value()
        for vars in countries[country]:
            if vars.varValue > 0:
                if country not in res['ResourcesPerCountryBySector']:
                    res['ResourcesPerCountryBySector'][country] = {}
                if vars.name.split('^^^')[0] not in res['ResourcesPerCountryBySector'][country]:
                    res['ResourcesPerCountryBySector'][country][vars.name.split('^^^')[0]] = 0
                res['ResourcesPerCountryBySector'][country][vars.name.split('^^^')[0]] += vars.varValue
                if vars.name.split('^^^')[0] not in res['CountryPerResource']:
                    res['CountryPerResource'][vars.name.split('^^^')[0]] = {}
                if country not in res['CountryPerResource'][vars.name.split('^^^')[0]]:
                    res['CountryPerResource'][vars.name.split('^^^')[0]][country] = 0
                res['CountryPerResource'][vars.name.split('^^^')[0]][country] += vars.varValue
    with open('frontend/data/algo4output.json', 'w') as outfile:
        json.dump(res, outfile)
    return res


if __name__ == "__main__":
    algo4()




    



