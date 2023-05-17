function mydata=GetNcVar(ncFileName,ncVarName,startIndex,cnt,isPermute)
% read a given variable from a netcdf file
% usage:
%       myData=GetNcVar(Netcdf-filename,netcdf-varname [,startIndex,cnt,isPermute])

if ~exist(ncFileName,'file')
   error([ncFileName,' is not found!']);
end

ncfid=netcdf.open(ncFileName,'NC_NOWRITE');
varID=netcdf.inqVarID(ncfid,ncVarName);
[varname,vartype,vardimids,numAtts]=netcdf.inqVar(ncfid,varID);

myScale=1; myOffSet=0;

for numA=1:numAtts
    tmpattname=netcdf.inqAttName(ncfid,varID,numA-1);
    switch lower(tmpattname)
        case {'scale_factor','scalefactor'}
           myScale=netcdf.getAtt(ncfid,varID,tmpattname);
        case {'add_offset','off_set','offset','offset_value'}
           myOffSet=netcdf.getAtt(ncfid,varID,tmpattname);
        otherwise
           % do nothing
     end
end

if nargin>=4
   if nargin==4, isPermute=1; end
   mydata=netcdf.getVar(ncfid,varID,startIndex,cnt,'double'); 
   if ischar(isPermute)
      switch lower(isPermute)
        case {'nopermute','origin','xy','xyz','xyzt'}
          isPermute=0;
        otherwise
          disp(['unknown option: ',isPermute])
          isPermute=1;
      end
   end
else
   isPermute=1;
   mydata=netcdf.getVar(ncfid,varID,'double');
   if nargin==3
      switch lower(startIndex)
        case {'nopermute','origin','xy','xyz','xyzt'}
          isPermute=0;
        otherwise
          disp('unknown option: ')
          startIndex
      end
   end
end
netcdf.close(ncfid);

% rescale data if necessary
if isPermute==1
   mydata=permute(mydata,length(size(mydata)):-1:1);
end
mydata=double(mydata);
mydata=mydata*myScale+myOffSet;
