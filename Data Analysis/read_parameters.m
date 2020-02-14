function [ ] = read_parameters( dataAddr, DAQname, lkernel, lcycle, frameRatio )
% get current and patch parameters

    % current
    name = '';
    list = dir(dataAddr);
    for i = 3:length(list)
        if list(i).isdir == 1 && ~isempty(strfind(list(i).name,'pA'))
            name = list(i).name;
            break;
        end
    end
    current = regexp(name, '00pA', 'split');
    current = current(1);
    current = current{:};
    current = [current(end), '00'];
    current = int16(str2double(current));

    % Ra, Rm, Cm from patch maram.txt    
    patchtxtExist = 0;
    paths = regexp(dataAddr, '/', 'split');
    parampath = '';
    for i = 2:length(paths)-2
        p = paths{i};
        parampath = [parampath '/' p];
    end

    if exist([parampath '/patch param.txt'])
        patchtxtExist = 1;
        [~,~,Ra,Rm,Cm] = textread([parampath '/patch param.txt'], '%n%n%n%n%n', 'delimiter', ' ', 'headerlines', 1);
    elseif exist([parampath '/patch.JPG'])
        figure; imshow([parampath '/patch.JPG']);
        Ra = input('Ra: ');
        Rm = input('Rm: ');
        Cm = input('Cm: ');
    else
        Ra = 0;
        Rm = 0;
        Cm = 0;
    end    
    Ra = Ra(1); Rm = Rm(1); Cm = Cm(1);
    patchPara = zeros(1,3);
    patchPara(1) = Ra;
    patchPara(2) = Rm;
    patchPara(3) = Cm;
    disp(['Ra  Rm  Cm: ' num2str(patchPara)]);

    % resting potential and peak voltage from patch
    patch = importdata([dataAddr, DAQname]);
    patch = patch.data;
    patch = patch(:,2)' * 100; % (mV)
    restV = imerode(patch, ones(1,lkernel*frameRatio));
    restV = mean(restV);
    peakV = findpeaks(patch, 'minpeakdistance', lcycle * frameRatio - 100, 'minpeakheight', 0);
    peakV = mean(peakV);
    elecPara(1) = restV;
    elecPara(2) = peakV;
    disp(['restV peakV: ' num2str(elecPara)]);

    % If the neuron is qualified, keep this neuron
    save([dataAddr 'result/current.mat'], 'current', '-v7.3');
    save([dataAddr 'result/patchPara.mat'], 'patchPara', '-v7.3');
    save([dataAddr 'result/elecPara.mat'], 'elecPara', '-v7.3');

end

