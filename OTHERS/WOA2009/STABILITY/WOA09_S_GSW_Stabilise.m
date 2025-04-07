% Nettoyage de l'espace de travail
clear; clc;

%% Chemin du répertoire contenant les fichiers
dataDir = '/data0/project/drakkar/CONFIGS/CREG12.L75/CREG12.L75-I/';

%% Vérification et chargement du package TEOS-10
if exist('gsw_stabilise_SA_CT', 'file') ~= 2
    disp('La fonction gsw_stabilise_SA_CT n''est pas trouvée. Ajout du chemin vers TEOS-10...');
    % Modifier ce chemin en fonction de l'emplacement de votre package TEOS-10
    addpath('/data0/project/drakkar/USERS/ctalandi/MISCE/GSW-MATLAB_v3_06_16/');
    if exist('gsw_stabilise_SA_CT', 'file') ~= 2
        error('Le package TEOS-10 est introuvable. Veuillez l''installer ou corriger le chemin.');
    else
        disp('Package TEOS-10 chargé avec succès.');
    end
else
    disp('Package TEOS-10 déjà installé.');
end

%% Lecture des fichiers NetCDF de température et salinité
file_temp = fullfile(dataDir, 'woa09_ConTem_monthly_1deg_CT_CMA_drowned_Ex_L75.nc');
file_salt = fullfile(dataDir, 'woa09_SalAbs_monthly_1deg_SA_CMA_drowned_Ex_L75.nc');

% Lecture des variables de température et salinité.
% Les dimensions sont : [time_counter, z, lat0, lon0]
CT = ncread(file_temp, 'CT');  % [time, depth, lat, lon]
SA = ncread(file_salt, 'SA');  % [time, depth, lat, lon]


% Lecture des coordonnées spatiales (les fichiers contiennent lat et lon)
lat_grid = ncread(file_temp, 'lat');  % [lat0 x lon0]
lon_grid = ncread(file_temp, 'lon');  % [lat0 x lon0]

% Dimensions des fichiers
[nlon, nlat, nz, nt] = size(CT);
disp(['Données de température lues : ', num2str(nt), ' x ', num2str(nz), ' x ', num2str(nlat), ' x ', num2str(nlon)]);

%% Lecture du fichier de profondeur
file_depth = fullfile(dataDir, 'woa09_depth_Ex_L75.nc');
% Lecture de la variable depth: dimensions [time_counter, z, lat0, lon0]
depth_all = ncread(file_depth, 'depth');  
% Comme les profondeurs sont identiques en chaque point horizontal, on extrait le profil vertical
% en moyennant sur time et en prenant par exemple la première position spatiale
depth_profile = squeeze(mean(depth_all(1, 1,:,:), 1)); % vecteur [z x 1]
disp(['Profondeur lue: ', num2str(length(depth_profile)), ' niveaux.']);

% Transforme la temperature conservative en temperature in-situ
TinSit=gsw_t_from_CT(SA,CT,depth_all)

%% Allocation pour les données stabilisées
SA_stab = SA;
CT_stab = CT;

%% Calcul de la pression
% On suppose que la profondeur est la même sur toute la grille, et on utilise la latitude moyenne
lat_vector = lat_grid(1,:);
single_depth=depth_profile(:,1);
num_lat = length(lat_vector);  % Nombre de latitudes (360)
num_depth = length(single_depth);  % Nombre de profondeurs (75)
pressure = zeros(num_depth, num_lat);  % Initialisation [75 × 360]
for j = 1:num_lat
    pressure(:, j) = gsw_p_from_z(-single_depth, lat_vector(j));
end

%% Stabilisation des profils
% Traitement pour chaque mois (temps), et pour chaque point horizontal.
for t = 1:nt
    for i = 1:nlon
        for j = 1:nlat
            % Extraction des profils verticaux pour le mois t et la position (j,i)
            SA_prof = squeeze(SA(i,j,:,t));
            TinSit_prof = squeeze(TinSit(i,j,:,t));
            loc_pressure= squeeze(pressure(:,j))
            % Vérification des valeurs valides (au moins 3 points non-NaN)
            valid_idx = ~isnan(SA_prof) & ~isnan(TinSit_prof);
            disp(valid_idx);

            if sum(valid_idx) > 2  
                % Stabilisation du profil avec TEOS-10
                [SA_stab(i,j,valid_idx, t)] = ...
                gsw_stabilise_SA_const_t(SA_prof(valid_idx), TinSit_prof(valid_idx), loc_pressure(valid_idx));
            end
        end
    end
end

disp('Stabilisation terminée.');

%% Sauvegarde des données stabilisées dans de nouveaux fichiers NetCDF

% Création du fichier pour SA stabilisée
ncid_SA = netcdf.create(fullfile(dataDir, 'SA_stab.nc'),'CLOBBER');
dimid_time = netcdf.defDim(ncid_SA, 'time_counter', nt);
dimid_depth = netcdf.defDim(ncid_SA, 'z', length(depth_profile));
dimid_lat = netcdf.defDim(ncid_SA, 'lat0', nlat);
dimid_lon = netcdf.defDim(ncid_SA, 'lon0', nlon);
varid_SA = netcdf.defVar(ncid_SA, 'SA', 'double', [dimid_lon, dimid_lat, dimid_depth, dimid_time]);
netcdf.endDef(ncid_SA);
% Note : L'ordre des dimensions doit correspondre à celui d'écriture (ici, [lon, lat, depth, time])
% Pour réarranger les données, on utilise permute :
netcdf.putVar(ncid_SA, varid_SA, SA_stab);
%netcdf.putVar(ncid_SA, varid_SA, permute(SA_stab, [4, 3, 2, 1]));
netcdf.close(ncid_SA);
disp('Fichier SA_stab.nc créé.');

% Création du fichier pour CT stabilisée
%ncid_CT = netcdf.create(fullfile(dataDir, 'CT_stab.nc'),'CLOBBER');
% dimid_time = netcdf.defDim(ncid_CT, 'time_counter', nt);
% dimid_depth = netcdf.defDim(ncid_CT, 'z', length(depth_profile));
% dimid_lat = netcdf.defDim(ncid_CT, 'lat0', nlat);
% dimid_lon = netcdf.defDim(ncid_CT, 'lon0', nlon);
% varid_CT = netcdf.defVar(ncid_CT, 'CT', 'double', [dimid_lon, dimid_lat, dimid_depth, dimid_time]);
% netcdf.endDef(ncid_CT);
% netcdf.putVar(ncid_CT, varid_CT, permute(CT_stab, [4, 3, 2, 1]));
% netcdf.close(ncid_CT);
% disp('Fichier CT_stab.nc créé.');
