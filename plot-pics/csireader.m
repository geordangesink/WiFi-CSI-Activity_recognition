clear all
%% csireader.m
%
% Read and plot CSI from UDPs created using the nexmon CSI extractor (nexmon.org/csi)
%
% Modify the configuration section to your needs
%
% Make sure you run >mex unpack_float.c before reading values from bcm4358 or bcm4366c0 chip for the first time
%
%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%   IMPORTANT  %%%%%
% In order to run this code you need to adjust the configuration
% and if otherwise unmodified you need a specific directory structure (written in [] can have multiple folders that will all be scanned):
%
% ../data/channel/[personNames]/[movementType]/[action]/[*.pcap]
% ../figures/channel/[personNames]/[movementType]/[action]
% ../images/channel/[personNames]/[movementType]/[action]
% ../images/channel/combined/[movementType]/[action]
%
% this will scan all the pcaps from the first directory and create figures,
% as well as images (1px/packet/subcarrier/) for every .pcap file and put
% them in the respective folders
%
% paths the script is searching for and didnt find will be console logged
%
% run csireader_single_folder if you wish to only render one folder with pcap files while using the same directory structure
%%%%%%%%%%%%%%%%%%%%%%%%

%% Configuration
CHIP = '43455c0'; % WiFi chip (possible values 4339, 4358, 43455c0, 4366c0)
BW = 20; % Bandwidth
CHANNEL = 3;
personList = dir('../data/3'); % specify the path to the person folders

% Loop through each person in the data folder
for h = 1:length(personList)
    % Skip hidden files and non-directories
    if personList(h).name(1) == 'combined'
        continue;
    end
    if personList(h).name(1) == '.' || ~personList(h).isdir
        continue;
    end

    PERSON = personList(h).name;

    folderPathPerson = fullfile('../data',string(CHANNEL), PERSON);
    disp(folderPathPerson)
    typeList = dir(folderPathPerson);

    % Loop through each type in the person folder
    for i = 1:length(typeList)
        % Skip hidden files and non-directories
        if typeList(i).name(1) == '.' || ~typeList(i).isdir
            continue;
        end

        TYPE = typeList(i).name;
        folderPathType = fullfile('../data',string(CHANNEL), PERSON, TYPE);

        actionList = dir(folderPathType);

        % Loop through each action in the type folder
        for j = 1:length(actionList)
            % Skip hidden files and non-directories
            if actionList(j).name(1) == '.' || ~actionList(j).isdir
                continue;
            end

            ACTION = actionList(j).name;
            folderPathAction = fullfile('../data',string(CHANNEL), PERSON, TYPE, ACTION);

            fileList = dir(folderPathAction);

            % Loop through each file in the action folder
            for k = 1:length(fileList)
                % Skip hidden files and directories
                if fileList(k).name(1) == '.' || fileList(k).isdir
                    continue;
                end

                %% Configuration
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
        end
    end
end
