clear all
%% csireader.m
%
% Read and plot CSI from UDPs created using the nexmon CSI extractor (nexmon.org/csi)
% Modify the configuration section to your needs
% Make sure you run >mex unpack_float.c before reading values from bcm4358 or bcm4366c0 for the first time
%
% The example.pcap file contains 4 (core 0-1, nss 0-1) packets captured on a bcm4358
%

% Specify the folder containing the files

            PERSON = 'adrian'
            TYPE = 'gestures'
            ACTION = 'big_wave'
            folderPathAction = fullfile('../data', PERSON, TYPE, ACTION);

            fileList = dir(folderPathAction);

            % Loop through each file in the action folder
            for k = 1:length(fileList)
                % Skip hidden files and directories
                if fileList(k).name(1) == '.' || fileList(k).isdir
                    continue;
                end

                %% Configuration
                CHIP = '43455c0'; % WiFi chip (possible values 4339, 4358, 43455c0, 4366c0)
                BW = 20; % Bandwidth
                CHANNEL = 44;
                FILE = fullfile(folderPathAction, fileList(k).name);
                NAME = erase(fileList(k).name, ".pcap");
                NPKTS_MAX = 5000; % Max number of UDPs to process

                %% Read file
                HOFFSET = 16; % Header offset
                NFFT = BW * 3.2; % FFT size
                p = readpcap();
                p.open(FILE);
                n = min(length(p.all()), NPKTS_MAX);
                p.from_start();
                csi_buff = complex(zeros(n, NFFT), 0);
                pkt_idx = 1;

                while (pkt_idx <= n)
                    f = p.next();
                    if isempty(f)
                        disp('No more frames');
                        break;
                    end
                    if f.header.orig_len - (HOFFSET - 1) * 4 ~= NFFT * 4
                        disp('Skipped frame with incorrect size');
                        continue;
                    end
                    payload = f.payload;
                    H = payload(HOFFSET:HOFFSET + NFFT - 1);
                    if strcmp(CHIP, '4339') || strcmp(CHIP, '43455c0')
                        Hout = typecast(H, 'int16');
                    elseif strcmp(CHIP, '4358')
                        Hout = unpack_float(int32(0), int32(NFFT), H);
                    elseif strcmp(CHIP, '4366c0')
                        Hout = unpack_float(int32(1), int32(NFFT), H);
                    else
                        disp('Invalid CHIP');
                        break;
                    end
                    Hout = reshape(Hout, 2, []).';
                    cmplx = double(Hout(1:NFFT, 1)) + 1j * double(Hout(1:NFFT, 2));
                    csi_buff(pkt_idx, :) = cmplx.';
                    pkt_idx = pkt_idx + 1;
                end

                %% Plot
                plotcsi(csi_buff, NFFT, false, BW, NAME, CHANNEL, PERSON, TYPE, ACTION);
                plotcsi_clean(csi_buff, NFFT, false, BW, NAME, CHANNEL, PERSON, TYPE, ACTION);
            end