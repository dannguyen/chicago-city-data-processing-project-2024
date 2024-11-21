# Chicago census, police, and municipal dataset work 2024-08

Notes on collecting/parsing city of Chicago data for various analyses. WIP


## Example pipeline run

```sh
./scripts/public-safety/compile_crime_incidents.py \
    --schema-path=meta/schemas/crime-incidents-schema.compiled.csv \
    -i data/alpha/public-safety/sample.crime-incidents.csv \
    > data/compiled/sample.crime-incidents.compiled.csv



## TODOs

Business licenses
- reconcile, filter for active/inactive
- ignore limited licenses?
- data goes back to 2000, figure out good cutoff date for quality
    - maybe when "BUSINESS ACTIVITY ID" is not empty?
- obs
    - "LICENSE NUMBER" is issued per business per "BUSINESS ACTIVITY"
    - an "ACCOUNT NUMBER" can have many licenses

Arrests


Crime incidents
- simplify location categories, time periods (day/night, sunset, sunrise)
- simplify secondary categories
- cutoff at 2012, since new boundaries went into effect
- get fbi codes

Other data
- historical weather data


## Data sources


## business licenses


https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr/about_data



## socioeconomic, etc


#### socioeconomic disadvantaged areas (acs-2014)

https://data.cityofchicago.org/Community-Economic-Development/Socioeconomically-Disadvantaged-Areas/2ui7-wiq8/about_data


https://data.cityofchicago.org/resource/2ui7-wiq8.geojson

> Areas of Chicago, based on census tracts, that are the most socioeconomically disadvantaged, for the purpose of promoting equitable hiring within areas of economic need. Qualifying areas were identified using three criteria, based on data from the 2014 American Community Survey: household income, poverty rate, and unemployment rate. These area designations are used for workforce bid incentives for City contracts administered by the Department of Procurement Services. They will also be used for workforce requirements for construction at the temporary casino facility, as agreed to in the Host Community Agreement between Bally’s and the City of Chicago.


## transit, etc

#### CTA rail stations

> Point data representing location of CTA Rail Station. To view or use these files, compression software and special GIS software, such as ESRI ArcGIS is required. Projected Coordinate System: NAD_1983_StatePlane_Illinois_East_FIPS_1201_Feet

https://data.cityofchicago.org/dataset/CTA-L-Rail-Stations-Shapefile/vmyy-m9qj/about_data
curl https://data.cityofchicago.org/download/vmyy-m9qj/application%2Fx-zip-compressed





## Crime data

### arrests

https://data.cityofchicago.org/Public-Safety/Arrests/dpt3-jri9/about_data


### incidents


https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/about_data

IUCR codes
http://data.cityofchicago.org/Public-Safety/Chicago-Police-Department-Illinois-Uniform-Crime-R/c7ck-438e

data:
https://data.cityofchicago.org/Public-Safety/Crimes-2001-to-Present/ijzp-q8t2/data_preview


#### police stations

[todo]
https://data.cityofchicago.org/Public-Safety/Police-Stations/z8bn-74gv/about_data

#### 2012-current police beats

Current:
https://data.cityofchicago.org/api/views/n9it-hstw/rows.csv?accessType=DOWNLOAD
https://data.cityofchicago.org/api/geospatial/aerh-rz74?method=export&format=GeoJSON

Deprecated:
https://data.cityofchicago.org/Public-Safety/Boundaries-Police-Beats-deprecated-on-12-18-2012-/kd6k-pxkv/about_data


#### police districts, current

https://data.cityofchicago.org/api/geospatial/fthy-xz3r?method=export&format=GeoJSON
https://data.cityofchicago.org/api/views/24zt-jpfn/rows.csv?accessType=DOWNLOAD

#### community areas, current

https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6

[[TODO: download]]

#### wards, current as of may-2023
https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2023-/p293-wvbd

#### wards, old 2015-2023

https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2015-2023-/sp34-6z76

