# ohw24_proj_MessageMeWhenItsHot_the_MHW_Vis&Report_app_au

## Project Name
Message Me When It's Hot - The MHW Visualisation and Report App

## One-line Description
Create a Web App to visualize extreme ocean temperatures and send alerts to users when it is TOO HOT!

## Collaborators
@mphemming
@ribeiron
@ranisa-gupta16
@B-stepin
@bui83
@JasonUWA

## Background

The intensity and frequency of extreme ocean temperature events, such as marine heatwaves (MHWs) and marine cold spells (MCSs), are expected to change as our oceans warm. Little is known about marine extremes in Australian coastal waters, particularly below the surface. 

The Integrated Marine Observing System (IMOS) National Mooring Network Facility has close to 15 years of subsurface mooring data, and more than 70 years of ship profile data at sites around Australia, including off Port Hacking, NSW and Maria Island, Tas. Mooring data are collected every 3-6 months depending on site location. [Ocean data products](https://essd.copernicus.org/articles/16/887/2024/essd-16-887-2024.html) exist at these sites, but there is presently no easy method to visualise the data online. 

It would be great to create a web app that shows clearly when and at what depth record temperatures have been measured, and when MHW and MCSs have occured. We can draw on popular apps such as this [MHW tracker for surface data](https://www.marineheatwaves.org/tracker.html), and [isithotrightnow](https://isithotrightnow.com/) for inspiration. 

It can be challenging to keep track of extreme ocean temperatures, and to compare newly recorded data sets with historical context. Hence, an alert system that identifies extreme ocean temperatures and potential QC issues would also be very handy.

IMOS also now has >15,000 near-realtime [FishSOOP Temperature profiles](https://www.unsw.edu.au/research/oceanography/fishsoop) that have been collected by the FishSOOP Facility since 2021. Hence, we can test the same alert system used for mooring data with this data set to check for potential QC issues, and with the help of a Machine Learning data set, potentially check for extreme temperatures. 


![snoop-dogg-dance (1)](https://github.com/user-attachments/assets/2fbd026a-ac1e-44d0-8afa-6c71d8d7c706)


## Goals
Create a Web App that:​

- Visualises extreme ocean temperatures ​(MHW/MCSs, records)

- ​Alerts users when:​

  - New records have been broken​

  - Marine Heatwaves or Coldspells have occured / are underway​

  - QC issues are identified (e.g. outliers, drift)​

DISCLAIMER: Until Near Real-Time data is available from the IMOS moorings and FishSOOP, the alerts will be send when new delayed data is added instead. The pla is to send an email with a summary of the data that has been added in relation to the dataset that is available. 

​The idea is to create a Web App that shows plots similar to the ones in https://www.isithotrightnow.com, but for the ocean. 
We can look at code from [this project last year](https://github.com/oceanhackweek/ohw23_proj_fancymoorings) - [presentation](https://www.youtube.com/watch?v=90t6h36-BOQ&list=PLVH-j9gOscWmTQNctTx07pf97BRuUxCBX&index=3)


## Datasets
- IMOS Mooring data:
  
  - MHW data products at [Port Hacking](https://thredds.aodn.org.au/thredds/catalog/UNSW/NRS_extremes/Temperature_DataProducts_v2/PH100/catalog.html) and [Maria Island](https://thredds.aodn.org.au/thredds/catalog/UNSW/NRS_extremes/Temperature_DataProducts_v2/MAI090/catalog.html) (NetCDF, CSV)​
    
  - [Long-Term Time Series Product](https://imos.org.au/news/aodn/new-user-friendly-time-series-products-from-the-imos-coastal-mooring-network) (LTS) at [Port Hacking](https://thredds.aodn.org.au/thredds/catalog/IMOS/ANMN/NSW/PH100/catalog.html) and [Maria Island](https://thredds.aodn.org.au/thredds/catalog/IMOS/ANMN/NRS/NRSMAI/catalog.html)​
    
- IMOS FishSOOP data:
  - aggregated profile product, including near-profile satellite SST and preliminary ML profile predictions (NetCDF, on request from @mphemming)​
  
  - Preliminary ML Random Forest Regressor model ​(~6 GB, on request from @mphemming)

- Other data:
  - [Satellite SST](https://thredds.aodn.org.au/thredds/catalog/IMOS/SRS/SST/ghrsst/L3S-1d/ngt/catalog.html) 

## Workflow/Roadmap

1. Gather data and create visualisations​
   - Mooring: data histogram, heatmap (date, depth), climatology​
   - FishSOOP: Profile plots​ (organised by surface MHWs/MCSs)

​2. Send email alerts when new data is added:​
  - Mooring:​
    - New temperature records​
    - MHW/MCSs event statistics​
    - QC issues: outliers, drift​
  - FishSOOP:​
    - Whether new profiles anomalously warm/cold​
    - QC issues: outliers, drift​

## References
1. AMDOT-EXT data products https://essd.copernicus.org/articles/16/887/2024/essd-16-887-2024.html
2. "MHW tracker" Website https://www.marineheatwaves.org/tracker.html
3. "Is it hot right now?" Website https://www.isithotrightnow.com
4. IMOS LTSPs https://imos.org.au/news/aodn/new-user-friendly-time-series-products-from-the-imos-coastal-mooring-network
5. IMOS National Mooring Network Facility descriptiom: https://imos.org.au/facility/national-mooring-network 
