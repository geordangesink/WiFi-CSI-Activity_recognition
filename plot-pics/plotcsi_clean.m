function [] = plot_full_scan_heatmap(csi_buff, nfft, normalize, BW, NAME, CHANNEL, PERSON, TYPE, ACTION)
% PLOT_FULL_SCAN_HEATMAP generates a clean heatmap for all packets captured during the scan.
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
figure('Visible', 'off'); % Create an invisible figure for clean output
x = -(nfft / 2):1:(nfft / 2 - 1);  % Subcarrier range
y = 1:size(csi_buff, 1);  % Packet indices

% Resize the output to match the exact dimensions of packets and subcarriers
imagesc(x, y, csi_mag);  % Plot magnitude of CSI for all packets
colormap jet;  % Color map for the heatmap (can use other color maps like 'hot', 'parula', etc.)
caxis([0 1500]);  % Set color axis limits from 0 to 1500

% Remove all visual decorations for a clean plot
set(gca, 'XTick', [], 'YTick', [], 'XColor', 'none', 'YColor', 'none', 'Color', 'none');
axis tight;
set(gca, 'Position', [0 0 1 1]); % Expand plot to cover the entire figure

% Save the heatmap plot to an image file
output_path = strcat('../images/', string(CHANNEL), '/', PERSON, '/', TYPE, '/', ACTION, '/', NAME, '_clean.png');
output_path_combined = strcat('../images/',string(CHANNEL),'/combined/', TYPE, '/', ACTION, '/', NAME, '_clean.png');
set(gcf, 'Units', 'pixels', 'Position', [100, 100, size(csi_mag, 2), size(csi_mag, 1)]);  % Match figure size to data dimensions
set(gca, 'Units', 'normalized', 'Position', [0 0 1 1]);  % Remove any padding

% Save the figure with exact pixel resolution
print(gcf, output_path, '-dpng', '-r0');  % '-r0' ensures no scaling, matches pixel dimensions exactly
print(gcf, output_path_combined, '-dpng', '-r0'); 
close;

