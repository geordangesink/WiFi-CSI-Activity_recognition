function [] = plot_full_scan_heatmap(csi_buff, nfft, normalize)
% PLOT_FULL_SCAN_HEATMAP generates a heatmap for all packets captured during the scan
% and combines signals from positive and negative subcarriers.
%
%   csi_buff: Matrix containing the CSI data (complex numbers)
%   nfft: FFT size (number of subcarriers)
%   normalize: Boolean flag for normalization

% Normalize if required
if normalize
    % Normalize CSI to the maximum value across all packets
    csi_buff = csi_buff ./ max(abs(csi_buff(:)));
end

% Aggregate data (taking the magnitude of the complex CSI values)
csi_mag = abs(csi_buff);

% Combine positive and negative subcarriers
n_half = nfft / 2;  % Half the number of subcarriers
csi_mag_combined = zeros(size(csi_mag, 1), n_half + 1);  % Initialize matrix for combined values

% Combine symmetric subcarriers
for i = 1:n_half
    csi_mag_combined(:, i) = csi_mag(:, n_half + i) + csi_mag(:, n_half - i + 1);
end

% Handle the central subcarrier (DC subcarrier)
csi_mag_combined(:, n_half + 1) = csi_mag(:, n_half + 1);

% Create the heatmap for all packets
figure
x = 0:n_half;  % Subcarrier indices (absolute values)

% Plot CSI heatmap
imagesc(x, [1 size(csi_buff, 1)], csi_mag_combined)  % Plot magnitude of CSI for all packets
colormap jet  % Color map for the heatmap (can use other color maps like 'hot', 'parula', etc.)
colorbar  % Show color bar to indicate magnitude scale
caxis([0 2000])  % Set color axis limits from 0 to 1000
set(gca, 'YDir', 'reverse')  % Reverse the y-axis for packet numbering
xlabel('Subcarrier Index')
ylabel('Packet number')
title('44-80 router on-1')
axis tight

% Optional: Save the heatmap plot to an image file
saveas(gcf, 'full_scan_csi_heatmap.png');  % Save the heatmap as a PNG image

close
end
