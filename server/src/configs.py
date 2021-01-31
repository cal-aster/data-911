# Author:  Meryll Dindin
# Date:    November 04, 2020
# Project: CalAster
from utils import *

specific_incident_config = {'CharlestonScrapping':
                            {
                                'assault': {
                                    'source': 'classification',
                                    'contains': ['102D', 'assault']
                                },
                                'suicide': {
                                    'source': 'classification',
                                    'contains': ['127', 'suicidal']
                                },
                                'shooting': {
                                    'source': 'classification',
                                    'contains': ['shots', 'shooting']
                                },
                                'domestic_violence': {
                                    'source': 'classification',
                                    'contains': ['114B', '114D', 'dom disturb', 'domestic physical']
                                },
                                'burglary': {
                                    'source': 'classification',
                                    'contains': ['burglary', 'burg']
                                },
                                'sexual_offense': {
                                    'source': 'classification',
                                    'contains': ['pornography', 'prostitution']
                                },
                                'drugs': {
                                    'source': 'classification',
                                    'contains': ['drugs', '116']
                                }
                            },
                            'BerkeleyScrapping':
                            {
                                'assault': {
                                    'source': 'description',
                                    'contains': ['assault']
                                },
                                'shooting': {
                                    'source': 'description',
                                    'contains': ['gun weapon', 'shooting', 'shots']
                                },
                                'domestic_violence': {
                                    'source': 'description',
                                    'contains': ['domestic violence']
                                },
                                'burglary': {
                                    'source': 'description',
                                    'contains': ['burglary']
                                },
                                'sexual_offense': {
                                    'source': 'description',
                                    'contains': ['sexual assault']
                                },
                                'drugs': {
                                    'source': 'description',
                                    'contains': ['drugs', 'narcotics']
                                }

                            },
                            'CambridgeScrapping':
                            {
                                'assault': {
                                    'source': 'classification',
                                    'contains': ['assault']
                                }
                            },
                            'StPetersburgScrapping':
                            {
                                'assault': {
                                    'source': 'classification',
                                    'contains': ['assault']
                                },
                                'homocide': {
                                    'source': 'classification',
                                    'contains': ['homocide']
                                },
                                'burglary': {
                                    'source': 'classification',
                                    'contains': ['burglary']
                                },
                                'sexual_offense': {
                                    'source': 'classification',
                                    'contains': ['sexual offense']
                                },
                                'drugs': {
                                    'source': 'classification',
                                    'contains': ['drugs', 'narcotics']
                                }

                            },
                            'MesaScrapping':
                            {
                                'assault': {
                                    'source': 'classification',
                                    'contains': ['assault']
                                },
                                'homocide': {
                                    'source': 'classification',
                                    'contains': ['homocide', 'homicide']
                                },
                                'suicide': {
                                    'source': 'classification',
                                    'contains': ['suicide']
                                },
                                'burglary': {
                                    'source': 'classification',
                                    'contains': ['burglary']
                                },
                                'sexual_offense': {
                                    'source': 'classification',
                                    'contains': ['sexual offense', 'sexual assault', 'prostitution', 'obscene harassing', 'molesting']
                                },
                                'drugs': {
                                    'source': 'classification',
                                    'contains': ['drugs', 'narcotics']
                                },
                                'shooting': {
                                    'source': 'classification',
                                    'contains': ['shooting', 'shots']
                                }

                            },
                            'CincinnatiScrapping':
                            {
                                'assault': {
                                    'source': 'classification',
                                    'contains': ['asslt', 'assault']
                                },
                                'shooting': {
                                    'source': 'classification',
                                    'contains': ['gun', 'shoot', 'shots']
                                },
                                'domestic_violence': {
                                    'source': 'classification',
                                    'contains': ['dominj', 'domvio', 'domvir']
                                },
                                'burglary': {
                                    'source': 'classification',
                                    'contains': ['burglary', 'burg']
                                },
                                'sexual_offense': {
                                    'source': 'classification',
                                    'contains': ['sex', 'rape', 'prosti']
                                },
                                'drugs': {
                                    'source': 'classification',
                                    'contains': ['drug', 'heroin', 'sdet']
                                },
                                'suicide': {
                                    'source': 'classification',
                                    'contains': ['suic', 'suicide']
                                }

                            }, 'SanFranciscoScrapping':
                            {
                                'assault': {
                                    'source': 'classification',
                                    'contains': ['asslt', 'assault', '240', '241', '220', '245']
                                },
                                'homocide': {
                                    'source': 'classification',
                                    'contains': ['187']
                                },
                                'shooting': {
                                    'source': 'classification',
                                    'contains': ['gun', 'shoot', 'shots', '216', '217', '221', '10-71', '10-72']
                                },
                                'burglary': {
                                    'source': 'classification',
                                    'contains': ['burglary', 'burg', '459']
                                },
                                'sexual_offense': {
                                    'source': 'classification',
                                    'contains': ['sex', 'rape', 'prosti', '647B', '288', '261', '262',  '266']
                                },
                                'drugs': {
                                    'source': 'classification',
                                    'contains': ['drug', 'heroin', 'sdet']
                                },
                                'suicide': {
                                    'source': 'classification',
                                    'contains': ['suic', 'suicide', '801']
                                }

                            }
                            }

highest_priority_config = {"CambridgeScrapping": ["1"],
                           "CincinnatiScrapping": ["1"],
                           "DallasScrapping": ["1"],
                           "DetroitScrapping": ["1"],
                           "HartfordScrapping": ["A"],
                           "MesaScrapping": ["Emergency", "E"],
                           "NewOrleansScrapping": ["3"],
                           "OrlandoScrapping": ["1"],
                           "RichmondScrapping": ["1"],
                           "SanFranciscoScrapping": ["3"],
                           "SeattleScrapping": ["1"]
                           }

arrest_config = {"SeattleScrapping":
                 {
                     'source': 'clearance_description',
                     'contains': ['physical arrest']
                 },
                 "AshevilleScrapping":
                 {
                     'source': 'disposition',
                     'contains': ['arrested', 'arrest']
                 },
                 "SanFranciscoScrapping":
                 {
                     'source': 'disposition',
                     'contains': ['arr']
                 },
                 'SantaMonicaScrapping':
                 {
                     'source': 'disposition',
                     'contains': ['arrest']
                 },
                 'RichmondScrapping':
                 {
                     'source': 'description',
                     'contains': ['warrant arrest']
                 },
                 'OrlandoScrapping':
                 {
                     'source': 'description',
                     'contains': ['warrant arrest', 'arrest warrant', 'arrest affidavit']
                 },
                 'CincinnatiScrapping':
                 {
                     'source': 'disposition',
                     'contains': ['arrest']
                 },
                 'CharlestonScrapping':
                 {
                     'source': 'description',
                     'contains': ['arrest', 'warrant ar']
                 }

                 }

geojson_config = {
    "nhoods": {
        "San Francisco": {'name': 'neighborhood_geojsons/neighborhoods_san_francisco.geojson'},
        "Cincinnati": {'name': 'neighborhood_geojsons/neighborhoods_cincinnati.json'}
    },
    'None': None



}
