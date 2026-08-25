% Sovereign Grid Automated Enhancement Matrix
clear;
clc;

log_folder = '~/sovereign_grid/telemetry_logs/';
files = dir([log_folder, 'snapshot_*.txt']);

if isempty(files)
    disp('[LOAD WARNING] No real-time files found yet. Processing default fallback matrix.');
    raw_data = [30.2672, -97.7431, 150.2, 0.045; 30.2673, -97.7432, 150.5, 0.012; 30.2675, -97.7430, 151.0, 0.089; 30.2676, -97.7433, 149.8, 0.095];
else
    % Sort files by date to target the freshest telemetry log snapshot
    [~, idx] = sort([files.datenum], 'descend');
    latest_file = [log_folder, files(idx(1)).name];
    
    try
        raw_data = load(latest_file);
    catch
        disp('[ERROR] File read error or text formatting mismatch. Using fallback baseline.');
        raw_data = [30.2672, -97.7431, 150.2, 0.045; 30.2673, -97.7432, 150.5, 0.012; 30.2675, -97.7430, 151.0, 0.089; 30.2676, -97.7433, 149.8, 0.095];
    end
end

% Extract and clean variable parameters
latitudes  = raw_data(:, 1);
longitudes = raw_data(:, 2);
altitudes  = raw_data(:, 3);
telemetry_signal = raw_data(:, 4);

threshold = 0.020;
clean_signal = telemetry_signal;
clean_signal(clean_signal < threshold) = threshold;

amplification_factor = 2.5;
enhanced_signal = clean_signal .* amplification_factor;

enhanced_matrix = [latitudes, longitudes, altitudes, enhanced_signal];

save('-v7', '~/sovereign_grid/enhanced_telemetry.mat', 'enhanced_matrix');
disp('=== Stabilized Array Snapshot Output ===');
disp(enhanced_matrix);
