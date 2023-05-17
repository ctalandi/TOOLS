function RunoffToMask(Year)

%Variables you might want to change
datamsk='/data0/project/drakkar/CONFIGS/CREG12.L75/GRID/';
MaskFile=[datamsk,'CREG12.L75-REF09_tmask.nc'] 
%datamsk='/data0/project/drakkar/CONFIGS/ARC60/MESH-MASK/';
%MaskFile=[datamsk,'SEDNA_tmask_LargeReady_20200808_Clean_Z.nc'] 
SpatialMultiplier=1 % extra cells in x/y direction, as a radius, to put the runoff from the file onto your new mask
%SpatialMultiplier=2 % extra cells in x/y direction, as a radius, to put the runoff from the file onto your new mask
% Should be 0 if the same resolution= only 1 cell gets the runoff
%  going from 1/12 to 1/60 means you need 25 as many cells. this is the same as a radius of 2: center point, 2 up,left,right,down=box of sides = 5. 25x more points

% Written by Clark Pennelly, pennelly@ualberta.ca
% Shouldnt need to change the below
%datain='/data0/project/drakkar/CONFIGS/ARC60/RUNOFFS/ANHA12_Runoff_DATA/';
%RunoffFile=['ANHA12_Combined_Liquid_Solid_runoff_',num2str(Year),'.nc']
datain='/data0/project/drakkar/CONFIGS/CREG025.L75/DATA_FORCING/RUNOFFS/HYDROGFD/';
RunoffFile=['CREG025_ReNat_HydroGFD_HBC_runoff_monthly_y',num2str(Year),'.nc']

RunoffLat=GetNcVar([datain,RunoffFile],'nav_lat');
RunoffLon=GetNcVar([datain,RunoffFile],'nav_lon');
RunoffData=GetNcVar([datain,RunoffFile],'sorunoff');
RunoffData(RunoffData==0)=nan;
[times RunoffY RunoffX]=size(RunoffData)

MaskLat=GetNcVar(MaskFile,'nav_lat');
MaskLon=GetNcVar(MaskFile,'nav_lon');
MaskMask=GetNcVar(MaskFile,'tmask');

[MaskY MaskX]=size(MaskMask)
RUNOFF=zeros(times,MaskY,MaskX);

%%% Loop over time through the Runoff file. Anywhere runoff >0, find its lat/lon. Then look through MaskLat/Lon to find closest point. Drop Runoff value onto this point and move on. Will smoothe/fix later

count=0;
tmprunoff=squeeze(permute(nansum(RunoffData(:,:,:),1),[2,3,1]));
[yys xxs]=find(tmprunoff>0);
clear('tmprunoff')
[steps ignoreme]=size(yys)
tic
for spot=1:steps
   if(mod(spot,10)==0)
      disp([num2str(100*spot/steps),' % done'])
   end
   yspot=yys(spot);
   xspot=xxs(spot);
   LAT=RunoffLat(yspot,xspot);
   LON=RunoffLon(yspot,xspot);
   [YY,XX]=GetXYfromLatLon(LAT,LON,MaskLat,MaskLon);
   if(YY>SpatialMultiplier && XX>SpatialMultiplier && YY<MaskY-SpatialMultiplier && XX<MaskX-SpatialMultiplier)
      for t=1:12
         RUNOFF(t,YY-SpatialMultiplier:YY+SpatialMultiplier,XX-SpatialMultiplier:XX+SpatialMultiplier)=RunoffData(t,yspot,xspot)+RUNOFF(t,YY-SpatialMultiplier:YY+SpatialMultiplier,XX-SpatialMultiplier:XX+SpatialMultiplier);
      end % t loop
   end
end %spot loop
toc

% Set boundary to 0, as above method puts values outside Mask at boarder
RUNOFF(isnan(RUNOFF))=0;
RUNOFF(:,1,:)=0;
RUNOFF(:,:,1)=0;
RUNOFF(:,:,end)=0;
RUNOFF(:,end,:)=0;



SOURCE=RUNOFF;
SOURCE=nansum(SOURCE,1);
SOURCE=squeeze(permute(SOURCE,[2,3,1]));
SOURCE(SOURCE>0)=0.5;

%%% save file

dataout='/data0/project/drakkar/CONFIGS/CREG12.L75/FORCING/HYDROGFD-RUNOFFS/WORKAREA/';
NewFileName=[dataout,'FIX_',RunoffFile]
FinalFile=netcdf.create(NewFileName,'write');
times=12
%dimensions x y and time_counter unlimited
dimid1 = netcdf.defDim(FinalFile, 'x', double(MaskX));
dimid2 = netcdf.defDim(FinalFile, 'y', double(MaskY));
dimid3 = netcdf.defDim(FinalFile, 'time_counter',netcdf.getConstant('NC_UNLIMITED'));

%variables x y sorunoff, time_counter, socoefr
varid1 = netcdf.defVar(FinalFile, 'nav_lon','float', [dimid1,dimid2]);
varid2 = netcdf.defVar(FinalFile, 'nav_lat','float', [dimid1,dimid2]);
varid3 = netcdf.defVar(FinalFile, 'time_counter','double', [dimid3]);
varid4 = netcdf.defVar(FinalFile, 'runoff','float', [dimid1,dimid2,dimid3]);
varid5 = netcdf.defVar(FinalFile, 'socoefr','float', [dimid1,dimid2]);
varid6= netcdf.defVar(FinalFile, 'tmask','float', [dimid1,dimid2]);
%put variables

FinalFile
netcdf.endDef(FinalFile);
netcdf.putVar(FinalFile, varid1, permute(MaskLon,[2,1]));
netcdf.putVar(FinalFile, varid2, permute(MaskLat,[2,1]));
netcdf.putVar(FinalFile, varid3, [0], [times], 1:times);
netcdf.putVar(FinalFile, varid4, permute(RUNOFF,[3,2,1]));
netcdf.putVar(FinalFile, varid5, permute(SOURCE,[2,1]));
netcdf.putVar(FinalFile, varid6, permute(MaskMask,[2,1]));

netcdf.close(FinalFile)

end
