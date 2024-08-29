% This scrip is to generate a plot of temperature distribution at MAI. 
% Data source: https://thredds.aodn.org.au/thredds/fileServer/UNSW/NRS_extremes/Temperature_DataProducts_v2/MAI090/MAI090_TEMP_EXTREMES_1944-2023_v2.nc
% To do this plot, firstly you download data to local computer. 
% Here, my local is:
% \\fs1-per.nexus.csiro.au\{oa-waimos}\work\IMOS\TB\OceanHackWeek_2024\MHW.
% You can change to your local computer at here. 
cd('\\fs1-per.nexus.csiro.au\{oa-waimos}\work\IMOS\TB\OceanHackWeek_2024\MHW') %You can change to your local computer at here. 
ip='MAI090_TEMP_EXTREMES_1944-2023_v2.nc';
time=ncread(ip,'TIME')+datenum(1950,1,1);
depth=ncread(ip,'DEPTH');
temp=ncread(ip,'TEMP');
temp_intp=ncread(ip,'TEMP_INTERP');
temp_p90=ncread(ip,'TEMP_PER90');
temp_p10=ncread(ip,'TEMP_PER10');
% create historgram
        clf
        figure
        id=1; % to plot depth 21
        temp_min=min(temp(id,:));
        temp_max=max(temp(id,:));
        [a1,b1]=hist(temp(id,:),[temp_min:0.1:temp_max]);
        c=sum(a1);
        a2=a1/c*100;
        p10=round(prctile(temp(id,:),10));
        p90=round(prctile(temp(id,:),90));
        p50=round(prctile(temp(id,:),50));
           for i=1:length(b1)-1
               %i=5;
               x=[b1(i) b1(i+1) b1(i+1) b1(i)];
               y=[0 0 a2(i+1) a2(i)];
               z=(a2(i+1)+a2(i))*0.5;
               if b1(i+1)<=p10
                  fill(x,y,'b','LineStyle','none')
               
               elseif b1(i+1) >= p90
               
                   fill(x,y,'r','LineStyle','none')
               else
                   fill(x,y,'w','LineStyle','-')
               end
               hold on
           end 
        hold on
        plot([p10 p10],[0 3],'k--');
        
        tex_p10=['10th percentile: ',num2str(p10),'^{o}C'];
        text(p10-0.2,2,tex_p10,'Rotation',90,'Color','blue')
        hold on
        plot([p90 p90],[0 3],'k--');
        tex_p90=['90th percentile: ',num2str(p90),'^{o}C'];
        text(p90+0.2,2,tex_p90,'Rotation',90,'Color','red')
        hold on
         plot([p50 p50],[0 3],'k--');
         tex_p50=['50th percentile: ',num2str(p50),'^{o}C'];
        text(p50+0.2,2,tex_p50,'Rotation',90,'Color','black')
        
        %TO DAY TEM
        temp_today=16;
        plot([temp_today temp_today],[0 3],'k--');
        text_today=['Temperature today: ',num2str(temp_today),'^{o}C'];
        text(temp_today+0.2,2,text_today,'Rotation',90,'Color','black')
        
        %plot(b1,a2)
        ylabel('(%)')
        xlabel('Temperature (^{o}C)')
       
        tit=['Distribution temperature at MAI, depth: ',num2str(depth(id)),'m'];
        title(tit)
        set(gca,'LineWidth',1,'Box','On','FontSize',14,'XGrid','On','YGrid','On');
        cd('\\fs1-per.nexus.csiro.au\{oa-waimos}\work\IMOS\TB\OceanHackWeek_2024\MHW')
 % Print
        x2 = gcf;
        x2.Color = 'white';
        x2.Visible='on';
        set(x2,'position',[100 100 1000 600]); % width/ height
        %filen=[num2str(depth(1)),'m.html'];
       
        exportgraphics(x2,'Temperature_Distribution_2m.png','Resolution',600)     
