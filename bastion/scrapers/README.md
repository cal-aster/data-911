# Data911 - Open Data Collection
`Author: Meryll Dindin`
`Contact: meryll@calaster.com`

## Conventions to add a new city

Start by creating a folder named according to `{state}-{city}`. This folder will contain 3 (or 4) important files required to correctly get our hands on the 911 Open Data.

* `description.yaml` contains meta-data regarding the dataset, but also generic meta-data about the city. We'll find attributes such as longitude, latitude, population in that file.
* `parser-api.yaml` contains the table of correspondence for the data attributes provided by the city and our internal conventions. It also is required to follow the conventions regarding types, as it directly influences the casting and the cleaning. This configuration file will mostly be used during any Socrata API transaction.
* `parser-csv.yaml` contains a similar table than the previous file, but for a possibly given CSV archive of that accessible database. To be defined only if the CSV is available (easier to process at once to avoid any latency bottleneck with Socrata).
* `schema.yaml` contains the SQL schema for the data, which is thus used during the definition of the CREATE TABLE command when the city is initialized.

## Example run on Cincinnati: `bastion/tutorial.ipynb`