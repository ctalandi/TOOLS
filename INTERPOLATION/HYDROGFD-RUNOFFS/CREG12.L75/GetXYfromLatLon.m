function [YY,XX]=GetXYFromLatLon(latval,lonval,MaskLat,MaskLon)
DeltaLon=abs(MaskLon-lonval);
DeltaLat=abs(MaskLat-latval);
Delta=DeltaLon+DeltaLat;
MinVal=min(min(Delta));
[YY,XX]=find(Delta==MinVal);
[ysize ignoreme]=size(YY);
if(ysize>1)
  YY=YY(1);
  XX=XX(1);
end
if(Delta)>1 % too much variation, accounts for regions outside the mask
   YY=1;
   XX=1;
end

end % end function
