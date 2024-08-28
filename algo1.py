import pandas as pd
import json
import random as rd

Request_Table = pd.read_csv("table3_clean.csv")
Available_Ressource_Table = pd.read_csv("table1_clean.csv")

def algo(M1, M2, M3):
    def get_ressource_value(ressource, sector, quantity_asked, Available_Ressource_Table):
        """
        Finds value of a certain request
        """
        total_value = Available_Ressource_Table.loc[(Available_Ressource_Table["Sector"]==sector) & (Available_Ressource_Table["Resource"]==ressource), "Total Value ($CAD)"].iloc[0]
        total_available = Available_Ressource_Table.loc[(Available_Ressource_Table["Sector"]==sector) & (Available_Ressource_Table["Resource"]==ressource), "Quantity"].iloc[0]
        return (total_value/total_available)*quantity_asked
        
    def Output_dictionary(Country_Ressource_Info_Dictionary, Request_Table, Available_Ressource_Table, ressource_set):
        '''
        Creates output dictionary in standardized format
        '''
        res = {
            'MoneyPerCountry': {},
            'ResourcesPerCountryBySector': {}, #money per sector per country
            'CountryPerResource': {} #country per resource
        }

        for country in Country_Ressource_Info_Dictionary:
            res['MoneyPerCountry'][country] = Country_Ressource_Info_Dictionary[country][2]

            res['ResourcesPerCountryBySector'][country] = {} 
            res['ResourcesPerCountryBySector'][country][Country_Ressource_Info_Dictionary[country][1]] = Country_Ressource_Info_Dictionary[country][2]

        
        for resource in ressource_set:
            for country in Country_Ressource_Info_Dictionary:
                if resource in Country_Ressource_Info_Dictionary[country]:
                    res['CountryPerResource'][resource] = {}
                    res['CountryPerResource'][resource][country] = res['MoneyPerCountry'][country]
        return res

    def country_info_init(Request_Table):
        '''
        Intiates a country info dict
        '''
        all_countries = set()
        for index, row in Request_Table.iterrows():
            all_countries.add(row['Country'])

        #init country with format {coutry:[nb request, got ressource=false]}
        Country_info = {}
        for country in all_countries:
            nb_request = Request_Table.loc[Request_Table["Country"]==country]
            Country_info[country] = [nb_request[nb_request.columns[0]].count(), False]
        
        return Country_info

    def ressource_init(Request_Table):
        #init ressource with format {(sector, ressource):[total ask, total available, now available=total available]}
        #Lock on ressource+sector (total unit*int)
        #available int * unit
        ressource = {}
        pairings = set()
        sectors = set()
        for index, row in Request_Table.iterrows():
            sectors.add(row['Sector'])

        #initialize pairings (sector, resource) using table 3 (could be done with table 1, might also have been simpler)
        for i in sectors:
            ressource_set = set()
            sector_table = Request_Table.loc[Request_Table["Sector"]==i]
            for index, row in sector_table.iterrows():
                ressource_set.add(row['Resource'])
            for resource in ressource_set:
                pairings.add((i, resource))

        #find info about pairing
        for pairing in pairings:
            #total ask
            sectorresource_table = Request_Table.loc[(Request_Table["Sector"]==pairing[0]) & (Request_Table["Resource"]==pairing[1])]
            total_ask = 0
            for index, row in sectorresource_table.iterrows():
                total_ask += row['Quantity']
            #total available
            total_available = Available_Ressource_Table.loc[(Available_Ressource_Table["Sector"]==pairing[0]) & (Available_Ressource_Table["Resource"]==pairing[1]), "Quantity"].iloc[0]
            ressource[pairing] = [total_ask,total_available, total_available]
        
        return (ressource, ressource_set)

    def init_request_dict(Request_Table, ressource, M1, M2, M3):
        #init request with format Request_dict = {[country, ressource, sector]: V}
        Request_dict = {}
        for index, row in Request_Table.iterrows():
            country_of_request = row['Country']
            resource_of_request = row['Resource']
            sector_of_request = row['Sector']
            ask = Request_Table.loc[(Request_Table["Sector"]==sector_of_request) & (Request_Table["Resource"]==resource_of_request) & (Request_Table["Country"]==country_of_request), "Quantity"].iloc[0]

            #FORMULA
            M1 = M1
            M2 = M2
            M3 = M3
            V = M1*(ressource[(sector_of_request, resource_of_request)][0]/float(ressource[(sector_of_request, resource_of_request)][1])) + M2*(ask/float(ressource[(sector_of_request, resource_of_request)][1])) - M3*Country_info[country_of_request][0]

            Request_dict[(country_of_request,resource_of_request,sector_of_request)]= V
        return (Request_dict, ask)



    Country_info = country_info_init(Request_Table)
    ressource, ressource_set = ressource_init(Request_Table)
    Request_dict, ask = init_request_dict(Request_Table, ressource, 1, 1, 1)


    #Info about each resource given to each country in the following format {Country_Ressource_Info_Dictionary : [Sector, Resource, Value ($)]}
    Country_Ressource_Info_Dictionary = {}
    #Minimum value (Minimum request has the following format {[country, ressource, sector]: V} )
    for i in range(len(Request_dict)):
        minimum_request = min(Request_dict, key=Request_dict.get)
        #country doesn't have a resource yet
        if not (Country_info[minimum_request[0]][1]):
            #ask smaller than available
            if ressource[(minimum_request[2],minimum_request[1])][2] > ask:
                Country_info[minimum_request[0]][1] = True
                ressource[(minimum_request[2],minimum_request[1])][2] = ressource[(minimum_request[2],minimum_request[1])][2] - ask
                value = get_ressource_value(minimum_request[1], minimum_request[2], ask, Available_Ressource_Table) 
                Country_Ressource_Info_Dictionary[minimum_request[0]] = [minimum_request[2], minimum_request[1], value]
        del Request_dict[minimum_request]


    output = Output_dictionary(Country_Ressource_Info_Dictionary, Request_Table, Available_Ressource_Table, ressource_set)
    with open('frontend/data/algo1output.json', 'w') as outfile:
        json.dump(output, outfile)

    return len(Country_Ressource_Info_Dictionary)



algo(0.8168157399129422, 0.014737762150057954, 3.2408863740720264)