function FixLandRunoff(Year)
% Written by Clark Pennelly, Dec 2020. Pennelly@ualberta.ca
% Code takes the input file's tmask, socoefr, and runoff variable. Moves any runoff where tmask=0 onto nearby ocean
datain='/data0/project/drakkar/CONFIGS/CREG12.L75/FORCING/HYDROGFD-RUNOFFS/WORKAREA/';
file=['FIX_CREG025_ReNat_HydroGFD_HBC_runoff_monthly_y',num2str(Year),'.nc']

%shouldnt need to change below unless variable names are different
lat=GetNcVar([datain,file],'nav_lat');
lon=GetNcVar([datain,file],'nav_lon');
runoff=GetNcVar([datain,file],'runoff');
source=GetNcVar([datain,file],'socoefr');
tmask=GetNcVar([datain,file],'tmask');

[times ys xs]=size(runoff)
%Take data, set to 0 where tmask is ocean (1). Anywhere that remains >0 is runoff over land. Find nearby ocean point, dump runoff into those points
Search=30;
counter=0
for t=1:times
tic
   tmprunoff=squeeze(permute(runoff(t,:,:),[2,3,1]));
   tmprunoff(tmask==1)=0;
   [yy xx]=find(tmprunoff>0);
   CellsToFix=size(yy)
   for i=1:CellsToFix
      ypoint=yy(i); xpoint=xx(i);
      if(ypoint>Search && xpoint > Search && ypoint <(ys-Search) && xpoint<(xs-Search))
         search=1;
         while(search<Search) % look for nearby ocean, drop runoff into it
            [yocean xocean]=find(tmask(ypoint-search:ypoint+search,xpoint-search:xpoint+search)==1);
            [points ignoreme]=size(yocean);
            if(points>1)
               counter=counter+1;
%               search=Search+1;
               RunoffPerCell=runoff(t,ypoint,xpoint)/points;
               runoff(t,ypoint,xpoint)=0;
               for spot=1:points
                  yspot=ypoint-search+yocean(spot)-1;
                  xspot=xpoint-search+xocean(spot)-1;
                  runoff(t,yspot,xspot)=runoff(t,yspot,xspot)+RunoffPerCell;
               end
               search=Search+1;
            end %point loop
            search=search+1;
         end %whilte loop
      end
   runoff(t,ypoint,xpoint)=0;
   end %cells to fix loop
toc
end %time loop

runoff(:,1,1)=0;

SOURCE=runoff;
SOURCE=nansum(SOURCE,1);
SOURCE=squeeze(permute(SOURCE,[2,3,1]));
SOURCE(SOURCE>0)=0.5;

dataout='/data0/project/drakkar/CONFIGS/CREG12.L75/FORCING/HYDROGFD-RUNOFFS/FINAL/';
fileout=['CREG12_ReNat_HydroGFD_HBC_runoff_monthly_y',num2str(Year),'.nc']
NewFileName=[dataout,'FixedLandRunoff_',fileout]
FinalFile=netcdf.create(NewFileName,'write');
times=12
%dimensions x y and time_counter unlimited
dimid1 = netcdf.defDim(FinalFile, 'x', double(xs));
dimid2 = netcdf.defDim(FinalFile, 'y', double(ys));
dimid3 = netcdf.defDim(FinalFile, 'time_counter',netcdf.getConstant('NC_UNLIMITED'));

%variables x y sorunoff, time_counter, socoefr
varid1 = netcdf.defVar(FinalFile, 'nav_lon','float', [dimid1,dimid2]);
varid2 = netcdf.defVar(FinalFile, 'nav_lat','float', [dimid1,dimid2]);
varid3 = netcdf.defVar(FinalFile, 'time_counter','double', [dimid3]);
varid4 = netcdf.defVar(FinalFile, 'runoff','float', [dimid1,dimid2,dimid3]);
varid5 = netcdf.defVar(FinalFile, 'socoefr','float', [dimid1,dimid2]);
varid6 = netcdf.defVar(FinalFile, 'tmask','float', [dimid1,dimid2]);
%put variables

FinalFile
netcdf.endDef(FinalFile);
netcdf.putVar(FinalFile, varid1, permute(lon,[2,1]));
netcdf.putVar(FinalFile, varid2, permute(lat,[2,1]));
netcdf.putVar(FinalFile, varid3, [0], [times], 1:times);
netcdf.putVar(FinalFile, varid4, permute(runoff,[3,2,1]));
netcdf.putVar(FinalFile, varid5, permute(SOURCE,[2,1]));
netcdf.putVar(FinalFile, varid6, permute(tmask,[2,1]));

netcdf.close(FinalFile)

end
