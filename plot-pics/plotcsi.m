function [] = plot_full_scan_heatmap(csi_buff, nfft, normalize, BW, NAME, CHANNEL, PERSON, TYPE, ACTION)
% PLOT_FULL_SCAN_HEATMAP generates a heatmap for all packets captured during the scan
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

% Create the heatmap for all packets
figure('Visible', 'off'); % Create an invisible figure
x = -(nfft / 2):1:(nfft / 2 - 1);  % Subcarrier range

% Plot CSI heatmap
imagesc(x, [1 size(csi_buff, 1)], csi_mag)  % Plot magnitude of CSI for all packets
colormap jet  % Color map for the heatmap (can use other color maps like 'hot', 'parula', etc.)
colorbar  % Show color bar to indicate magnitude scale
caxis([0 1500])  % Set color axis limits from 0 to 1000
set(gca, 'YDir', 'reverse')  % Reverse the y-axis for packet numbering
xlabel('Subcarrier')
ylabel('Packet number')
formattedName = strrep(NAME, '_', ' ');
title(sprintf('Channel: %d, Bandwidth: %d MHz, File: %s', CHANNEL, BW, formattedName));  % Use BW and formattedName in the title
axis tight

% Optional: Save the heatmap plot to an image file
saveas(gcf, strcat('../figures/', PERSON,'/', TYPE, '/', ACTION, '/', NAME, '.png'));  % Save the heatmap as a PNG image

close
end
