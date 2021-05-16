# Data911 - Open Data Collection

`Author: Meryll Dindin`
`Contact: meryll@calaster.com`

## Conventions to add a new city

Start by creating a folder named according to `{state}-{city}`. This folder will contain 3 (or 4) important files required to correctly get our hands on the 911 Open Data.

- `description.yaml` contains meta-data regarding the dataset, but also generic meta-data about the city. We'll find attributes such as longitude, latitude, population in that file.
- `parser-api.yaml` contains the table of correspondence for the data attributes provided by the city and our internal conventions. It also is required to follow the conventions regarding types, as it directly influences the casting and the cleaning. This configuration file will mostly be used during any Socrata API transaction.
- `parser-csv.yaml` contains a similar table than the previous file, but for a possibly given CSV archive of that accessible database. To be defined only if the CSV is available (easier to process at once to avoid any latency bottleneck with Socrata).
- `schema.yaml` contains the SQL schema for the data, which is thus used during the definition of the CREATE TABLE command when the city is initialized.

## Sourcing:

A good census point regarding Open Data has been made [here](http://us-cities.survey.okfn.org/dataset/emergency-calls).

## TODOs:

- Baton Rouge, Louisiana [311 Citizen Requests for Service](https://data.brla.gov/Government/311-Citizen-Requests-for-Service/7ixm-mnvx)
- Baton Route, Louisiana [Fire Incidents](https://data.brla.gov/Public-Safety/Baton-Rouge-Fire-Incidents/dakq-4sda/data)
- Bellevue, Washington [Fire Incidents](https://bellevue.data.socrata.com/Safe-Community/Open-Data-Fire-RMS-Incidents-Jan-1-2013-May-31-201/7zhy-vmpj)
- Chattanooga, Tennessee [Police Incidents](https://www.chattadata.org/Public-Safety/Police-Incident-Data/jvkg-79ss)
- Detroit, Michigan [911 Calls](https://data.detroitmi.gov/datasets/911-calls-for-service?geometry=-86.917%2C42.028%2C-79.926%2C42.738)
- Detroit, Michigan [Fire Incidents](https://data.detroitmi.gov/datasets/fire-incidents)
- Gainesville, Florida [Fire Responses](https://data.cityofgainesville.org/Public-Safety/Fire-Rescue-Responses/s7de-wj39)
- San Jose, California [Police Incidents](https://data.sanjoseca.gov/dataset/police-calls-for-service)
- San Jose, California [Fire Incidents](https://data.sanjoseca.gov/dataset/san-jose-fire-incidents/resource/e465b97c-c209-412a-ba4d-cde03d655f44)
- Sacramento, California [Fire Incidents](https://data.cityofsacramento.org/datasets/0b32edde7b14480e82d0d746108431db_0?geometry=-123.164%2C38.304%2C-119.669%2C38.680)
- Johns Creek, Georgia [Police Incidents](https://datahub.johnscreekga.gov/datasets/police-calls-for-service?geometry=169.250%2C-85.837%2C158.704%2C48.873)
- Johns Creek, Georgia [Fire Incidents](https://datahub.johnscreekga.gov/datasets/fire-department-incidents?geometry=-117.055%2C30.552%2C-89.094%2C33.805)
- Las Vegas, Nevada [Police Incidents](https://opendataportal-lasvegas.opendata.arcgis.com/datasets/metro-cfs-opendata)
- Las Vegas, Nevada [Fire Incidents](https://opendataportal-lasvegas.opendata.arcgis.com/datasets/fire-department-incident-count)
