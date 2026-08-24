clear; clc;
year = 2026; month = 8; day = 23; hour = 19; minute = 12; second = 57;
jd = 367 * year - floor(7 * (year + floor((month + 9) / 12)) / 4) + floor(275 * month / 9) + day + 1721013.5 + (hour + minute / 60 + second / 3600) / 24;

posSun_km = [147100000; 25300000; 11000000];
negSpaceOrigin = -posSun_km;

% Write directly to a JSON file for seamless Python ingestion
fid = fopen('capsule_solar_vector.json', 'w');
fprintf(fid, '{\n');
fprintf(fid, '  "status": "locked",\n');
fprintf(fid, '  "julian_date": %.6f,\n', jd);
fprintf(fid, '  "heliocentric_sun_km": [%f, %f, %f],\n', posSun_km(1), posSun_km(2), posSun_km(3));
fprintf(fid, '  "negative_space_origin_v": [%f, %f, %f]\n', negSpaceOrigin(1), negSpaceOrigin(2), negSpaceOrigin(3));
fprintf(fid, '}\n');
fclose(fid);
disp('--- CAPSULE ENDO-SUN JSON EXPORT COMPLETE ---');
