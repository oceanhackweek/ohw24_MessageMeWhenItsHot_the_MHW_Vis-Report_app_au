# ohw24_MessageMeWhenItsHot_the_MHW_Vis&Report_app_au

## Project Name
Message Me When It's Hot - The MHW Visualisation and Report App

## One-line Description
Create a Web App to visualize extreme ocean temperatures and send alerts to users when it is TOO HOT!

## Collaborators
Anyone is welcome to sign up. Send a message to @mphemming or to @ribeiron on the OHW AUS Slack Channel if you want to be added as a collaborator. 

## Background
The intensity and frequency of extreme ocean temperature events, such as marine heatwaves (MHWs) and marine cold spells (MCSs), are expected to change as our oceans warm. Little is known about marine extremes in Australian coastal waters, particularly below the surface. 

[more to be added here]

![snoop-dogg-dance (1)](https://github.com/user-attachments/assets/2fbd026a-ac1e-44d0-8afa-6c71d8d7c706)


## Goals
Create a Web App that:​

- Visualises extreme ocean temperatures ​

- ​Alerts users when:​

  - New records have been broken​

  - Marine Heatwaves or Coldspells are underway​

  - QC issues are identified (e.g. outliers, drift)​

​The idea is to create a Web App that shows plots similar to the ones in https://www.isithotrightnow.com, but for the ocean. 

## Datasets
- IMOS Mooring data:
  
  - MHW data products at Port Hacking and Maria Island (NetCDF, CSV)​
    
  - Long-Term Time Series Product (LTS) at Port Hacking and Maria Island​
    
- FishSOOP: aggregated product including SST and ML predictions (NetCDF)​
  
- ML Random Forest Regressor model ​

[links to come] 

## Workflow/Roadmap

1. Gather data and create visualisations​
   - Mooring: distribution, heatmap, climatology​
   - FishSOOP: Profile anomaly plots​

​2. Create functions that send email alerts when new data is added:​
  - Mooring:​
    - New temperature records​
    - MHW/MCSs event statistics​
    - QC issues: outliers, drift​
  - FishSOOP:​
    - Whether new profiles anomalously warm/cold​
    - QC issues: outliers, drift​

## References
1. "Is it hot right now?" Website https://www.isithotrightnow.com
