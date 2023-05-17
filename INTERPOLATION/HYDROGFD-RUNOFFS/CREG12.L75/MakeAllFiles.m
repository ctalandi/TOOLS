YearStart=2019
YearEnd=2020

%Code will take the ANHA12 liquid+solid runoff files, interpolate to your SEDNA grid, and then fix land points with runoff
% Final file will be called: "FIX_ANHA12_Combined_Liquid_Solid_runoff_2002.nc", using 2002 as the sample year
% Dec 2020, Clark Pennelly, pennelly@ualberta.ca

for Year=YearStart:YearEnd
   RunoffToMask(Year) % Interpolate runoff from CREG025.L75 to CREG12.L75
   FixLandRunoff(Year) % Take runoff on land, move to nearby ocean if close enough
end
