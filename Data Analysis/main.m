%% set parameters
clear; clc; close all;

number = 1;

listpath = '/datapool/home/zhaomd/Documents/MDFiles/AIS Data/Result_191008/10 mM glucose control.txt';
file = textread(listpath, '%s', 'delimiter', '\n');
fileAddr = file{number};
ncycle = 250;
lblank = 250;

% Movie loading path
resAddr = ['/datapool/home/zhaomd/Documents/MDFiles/AIS Data/Result_191008/' num2str(number) '/'];
pathname = ['/datapool/home/zhaomd/Documents/MDFiles/AIS Data/', fileAddr, '/'];
ResAddr = [pathname 'Result/'];

% make the result file and result excel
mkdir(ResAddr);
mkdir(resAddr);

calcMode = 2;  % 1 = several small dendrites; 2 = a long dendrite;

obj = 40;

mode = 2;     % 1 = optopatch; 2 = patch;
bin = 2;

movinfoname = 'movie_info.txt';
movinfo = textread([pathname movinfoname],'%s');
freq = str2double(movinfo{length(movinfo)-1});

if freq == 484
    nrow = 208;
    ncol = 312;
    if mode == 1
        ncol = 208*2/bin; % later
        nrow = 208*2/bin;
        dt_mov = 2.1535;
        frmStart =26;       % Movie steps start at this frame (included)
        frmStop = 4625;     % Movie steps stop at this frame (included)
        DAQfreq = 4643.4334;
    else
        dt_mov = 2.0658;
        frmStart =26;       % Movie steps start at this frame (included)
        frmStop = 10125;    % Movie steps stop at this frame (included)
        DAQfreq = 9681.4793;
    end
elseif freq == 1058
    if mode == 1
        dt_mov = 0.9549;
        DAQfreq = 10471.20;
    else
        dt_mov = 0.9452;
        DAQfreq = 21159.48;
    end
    ncol = 176*2/bin;
    nrow = 96*2/bin;
    frmStart = 1; %26;     % Movie steps start at this frame (included)
    frmStop = 8400; %10125;   % Movie steps stop at this frame (included)    
    
elseif freq == 671
    ncol = 240*2/bin;
    nrow = 144*2/bin;
    dt_mov = 1.4907;
    frmStart =26;     % Movie steps start at this frame (included)
    frmStop = 6625;    % Movie steps stop at this frame (included)    
    DAQfreq = 6706.9;
elseif freq == 2000
    ncol = 240*2/bin;
    nrow = 48*2/bin;
    dt_mov = 0.4968;
    frmStart =26;     % Movie steps start at this frame (included)
    frmStop = 20125;    % Movie steps stop at this frame (included)
    DAQfreq = 20128.82;
end


% constants
movname = '/movie.bin';
camera_bias = 100*power(bin,2)-3;          % background due to camera bias (100 for bin 1x1)
DAQname = '/movie_DAQ.txt';
dnsamp =DAQfreq/(1000/dt_mov);        % downsampling rate = DAQ rate/camera rate
DAQStart = round(frmStart*dnsamp+1);    % DAQ steps start at this datapoint (included)

% nrow, ncol
for i = 1:length(movinfo)
    tmp = movinfo{i};
    if strcmp(tmp,'ncol') == 1
        nrow = str2double(movinfo{i+2});
    elseif strcmp(tmp,'nrow') == 1
        ncol = str2double(movinfo{i+2});
    end
end



% load bin movie
fname = [pathname movname];
[mov1, ~] = readBinMov(fname, nrow, ncol);
mov1= double(mov1);
% mov1 = mov1(:,107:250,:);
[nrow,ncol,nframe]=size(mov1);
ysize=nrow;
xsize=ncol;
mov1 = mov1-camera_bias;      % remove camera bias


% mov1=mov1(:,:,frmStart:frmStop);% selected frames for analysis
mov1=mov1(:,:,frmStart:end);
nframes = size(mov1,3); % show me how many frames
% Set up a time axis for movie
t_mov = [0:nframes-1]*dt_mov/10^3;      % camera time axis in second



% Plot the raw whole-field intensity of the movie.
intens = squeeze(mean(mean(mov1)));% mean(mov1,3)
figure(1);
plot(intens);
xlabel('Frame number');
ylabel('Whole-field Intensity')
saveas(gca, [resAddr 'Whole-field Intensity.fig']);
saveas(gca, [resAddr 'Whole-field Intensity.png']);


% current, times
name = '';
list = dir(pathname);
for i = 3:length(list)
    if list(i).isdir == 1 && ~isempty(strfind(list(i).name,'injection'))
        name = list(i).name;
        break;
    end
end
name = regexp(name,'[-_]', 'split');
current = name{2};
current = strrep(current,'pA','');
current = int16(str2double(current));


times = name{4};
times = strrep(times,'times','');
times = str2double(times);
lcycle = int16(length(intens)/times);
save([ResAddr 'lcycle.mat'],'lcycle','-v7.3');


%%
frameratio = 20;    % frame of DAQ / frame of opto
% lcycle = 200000 / frameratio / ncycle;    % length of one cycle
lkernel = 4*lcycle; % used in remove baseline
lmovie = 40;        % time length of movie,20+1+20
tline = 0.00974436 * bin;    % the time gap between rows (ms)
splineDelt = 0.002;  % spline delta t
segLen = 40;        % length of each segment (pixel #)
distPerPix = 6.5*bin/obj; % um, 40x, bin = 2
step = 4;



%% select dendrite
img = mean(mov1,3);
scaleBarLength = round(20/distPerPix);
[maskDendSum, clineDendSum, realDistSum, dendType, clineDendMark, antiimg] = click_dendrite(img, ResAddr, pathname, distPerPix, calcMode);
inputlabel = input('please input segment label(d,h,a,x): ', 's');
if length(inputlabel) ~= max(clineDendMark)
    error('input error!');
end
b = unique(clineDendMark,'rows');
for i = length(inputlabel):-1:1
    if inputlabel(i) == 'x'
        clineDendMark(clineDendMark == b(i)) = 4;
    elseif inputlabel(i) == 'a'
        clineDendMark(clineDendMark == b(i)) = 3;
    elseif inputlabel(i) == 'h'
        clineDendMark(clineDendMark == b(i)) = 2;
    elseif inputlabel(i) == 'd'
        clineDendMark(clineDendMark == b(i)) = 1;
    end
end
maskDend = zeros(nrow, ncol);
for i = 1:length(maskDendSum)
    maskDend = maskDend + maskDendSum{i};
end
maskDend(maskDend > 1) = 1;

%% process the movie
% spacial filt the movie
movFilt = spacial_filt(mov1, lkernel, nframes, nrow, ncol);

% remove the baseline from all pixels on axon
[mov_bleach,intensN] = rem_pbleach2(movFilt, maskDend, nrow, ncol, nframes, lkernel );
[intensNO, pbleach] = rem_pbleach1(intens, 2*lmovie);

% choose the spike threshold
close all;
threshV = sel_thresh( intensN, ResAddr );
save([ResAddr 'threshV.mat'],'threshV','-v7.3');


% generate mean movie and mean spike on axon
[pks,spikeT] = findpeaks(intensNO, 'MinPeakDistance', lcycle-10);
[meanMov, meanSpike, markSpike] = mean_movie_spike(mov_bleach, maskDend, lmovie, spikeT, threshV);
tSpline = 0:splineDelt:lmovie-3;
meanSpikeSpline = spline(0:1:lmovie-1, meanSpike, tSpline);
legend('intensity','whole field peak time');

subplot(1,2,2); set(gca, 'Position', [0.53,0.15,0.4,0.7]); 
plot(meanSpikeSpline); title('mean spike');
saveas(gca, [resAddr 'mean spike + ROI intensity.png']);



%% calculate the arrive time of spike for each dendrite

%     figure;
clineDend = clineDendSum{1};
maskDend = maskDendSum{1};
realDist = realDistSum{1};

% initialize the variables
nSeg = floor((length(clineDend)-segLen + 1)/step);
calibrationT = zeros(1, nSeg);
segAPTime = zeros(1, nSeg);
segAPFrame = zeros(1, nSeg);
segColor = zeros(1,nSeg);
indexUse = uint8(ceil(segLen/2):step:ceil(segLen/2)+nSeg*step-1);   
segRealDist = realDist(indexUse); 

%     figure;
% calculate the mean spike and times
for j = 1:nSeg
    [maskSeg, ~] = segment_loc(maskDend, clineDend, indexUse(j), segLen);
    [calibrationT(j), segAPTime(j), segAPFrame(j), spike] = ...
         calculate(meanMov, maskSeg, meanSpikeSpline, clineDend(indexUse(j),:), nrow, lmovie, tline, splineDelt, dt_mov);
end

figure;
% generate .gif
ax1 = subplot(1,2,1);
ax2 = subplot(1,2,2);
colorSeq = {'r','b','m','g','c','y','k'};
for i = 1:nSeg
    cla(ax1);
    cla(ax2);
    [~, sg] = segment_loc(maskDend, clineDend, indexUse(i), segLen);
    pmid = clineDend(indexUse(i),:);

    ax1 = subplot(1,2,1);
    set(gcf, 'Position', [100,300,800,400]);
    set(gca, 'Position', [0.05, 0.11, 0.43, 0.8]);
    imshow(img,[]); axis off; hold on;    
    for j = 1:length(indexUse)
        tmp = indexUse(j);
        tmpColor = clineDendMark(tmp);
        plot(clineDend(indexUse(j),2),clineDend(indexUse(j),1),'Color', colorSeq{tmpColor},'Marker','.','MarkerSize',8);
    end
    [bound,~] = bwboundaries(maskDend);
    plot(bound{1}(:,2),bound{1}(:,1),'w');
    plot(sg(:,2),sg(:,1),'g-');
    plot(pmid(2),pmid(1),'g*');  

    ax2 = subplot(1,2,2);
    set(gca, 'Position', [0.55, 0.185, 0.4, 0.65]);
    for j = 1:i
        tmp = indexUse(j);
        tmpColor = clineDendMark(tmp);
        plot(segAPTime(j), segRealDist(j),'Color', colorSeq{tmpColor},'Marker','*','MarkerSize', 8); hold on;
    end
    xlabel('time (ms)'); ylabel('distance to soma (\mum)');
    title('AP time');
    axis([min(segAPTime)-0.06, max(segAPTime)+0.06,0,segRealDist(end)]);

    frame = getframe(gcf);
    im = frame2im(frame);
    [I,map] = rgb2ind(im,20);
    if i == 1
        imwrite(I,map,[ResAddr 'seg.gif'],'gif','Loopcount',inf,'DelayTime',0.15);
        imwrite(I,map,[resAddr 'seg.gif'],'gif','Loopcount',inf,'DelayTime',0.15);
    elseif i == nSeg
        imwrite(I,map,[ResAddr 'seg.gif'],'gif','WriteMode','Append', 'DelayTime', 3);
        imwrite(I,map,[resAddr 'seg.gif'],'gif','WriteMode','Append', 'DelayTime', 3);
    else
        imwrite(I,map,[ResAddr 'seg.gif'],'gif','WriteMode','Append', 'DelayTime', 0.15);
        imwrite(I,map,[resAddr 'seg.gif'],'gif','WriteMode','Append', 'DelayTime', 0.15);
    end
end


% generate .png
figure;
set(gcf, 'Position', [100,300,800,400]);
ax1 = subplot(1,2,1);
set(gca, 'Position', [0.05, 0.11, 0.43, 0.8]);
imshow(img,[]); axis on; hold on;
for j = 1:length(indexUse)
    tmp = indexUse(j);
    tmpColor = clineDendMark(tmp);
    plot(clineDend(indexUse(j),2),clineDend(indexUse(j),1),'Color', colorSeq{tmpColor},'Marker','.','MarkerSize',8);
end
[bound,~] = bwboundaries(maskDend);
plot(bound{1}(:,2),bound{1}(:,1),'w');

ax2 = subplot(1,2,2);
set(gca, 'Position', [0.55, 0.1, 0.4, 0.8]);
for j = 1:length(indexUse)
    tmp = indexUse(j);
    segColor(j) = clineDendMark(tmp);
    plot(segAPTime(j), segRealDist(j),'Color', colorSeq{segColor(j)},'Marker','*'); hold on;
end
xlabel('time (ms)'); ylabel('distance to soma (\mum)');
title('AP time');
axis([min(segAPTime)-0.2, max(segAPTime)+0.2,0,segRealDist(end)]);
saveas(gcf,[ResAddr 'seg.png']);

save([ResAddr 'segAPTime.mat'], 'segAPTime', '-v7.3');
save([ResAddr 'segRealDist.mat'], 'segRealDist', '-v7.3');

% save AIS info
aislength = realDist(find(clineDendMark == 3, 1,'last')) - realDist(find(clineDendMark == 3, 1, 'first')) + distPerPix;
aisdist = realDist(find(clineDendMark == 3, 1, 'first')) - realDist(1);
save([ResAddr 'aislength.mat'], 'aislength', '-v7.3');
save([ResAddr 'aisdist.mat'], 'aisdist', '-v7.3');

% start loc info
start_loc = zeros(1,2);
[~,start_loc(1)] = ginput(1);
start_loc(2) = (start_loc(1)-aisdist)/aislength;
save([ResAddr 'start_loc.mat'], 'start_loc', '-v7.3');

% find the number of the segmented segment by start location
segFlag = 0;  % flag of the segment that is segmented by the start location
startPre = find(segRealDist < start_loc(1), 1, 'last' );
startAft = find(segRealDist > start_loc(1), 1, 'first' );
if segColor(startPre) == segColor(startAft)
    segFlag = segColor(startPre);
end


%% PPT image
figure;
set(gcf, 'outerposition',get(0,'screensize'));
ha = tight_subplot(2,4,[0.08,0.03],[0.12,0.08],[0.02,0.02]);
axes(ha(1)); title('ROI movie'); set(gca,'Xcolor','w','Ycolor','w');
axes(ha(2)); 
patch = importdata([pathname, DAQname]);
patch = patch.data;
patch = patch(:,2)' * 100; % (mV)
plot(patch);
title('patch');
axes(ha(3)); 
imagesc(antiimg); axis image; 
map = zeros(255,3);
map(2:end,2) = linspace(0,1,254);
map(2:end,3) = linspace(0,1,254);
map(1,:) = [1,1,1];
colormap(map);
title('anti image (mark AIS)');

axes(ha(4)); 
plot(intensN); hold on; plot(spikeT(markSpike==1),intensN(spikeT(markSpike==1)),'r*');
title('ROI intensity'); xlabel(['frame (',num2str(dt_mov),' ms/frame)']); ylabel('intensity');
legend('intensity','used cycles (whole field peaks)','location','southeast');
axes(ha(5)); set(gca,'Xcolor','w','Ycolor','w');
axes(ha(6)); set(gca,'Xcolor','w','Ycolor','w');
axes(ha(7));  
for j = 1:length(indexUse)
    plot(segAPTime(j), segRealDist(j),'Color', colorSeq{segColor(j)},'Marker','*','MarkerSize', 8); hold on;
end
[~,indexMid] = min(abs(clineDend(indexUse,1)-repmat(nrow/2,length(segRealDist),1)));
h = plot(mean(segAPTime),segRealDist(indexMid),'g.','MarkerSize',20);
legend(h,'middle row','location','southeast');
xlabel({'time (ms)','','',['path: ',strrep(fileAddr,'_','\_')]});
ylabel('distance to soma (\mum)');
title('AP arrival time of segments');


% calculate the mean velocity of each segment
meanVLevel = zeros(4,2);
for j = 1:length(inputlabel)
    if inputlabel(j) == 'd'
        k = 1;
    elseif inputlabel(j) == 'h'
        k = 2;
    elseif inputlabel(j) == 'a'
        k = 3;
    elseif inputlabel(j) == 'x'
        k = 4;
    end
    if k ~= segFlag
        tmpTime = segAPTime(segColor == k);
        tmpDist = segRealDist(segColor == k);
        p = polyfit(tmpDist, tmpTime, 1);
        meanVLevel(k,1) = 1/p(1);
        plot(polyval(p,tmpDist),tmpDist,'Color',colorSeq{k}, 'LineWidth', 2); hold on;
    else
        tmpTime = segAPTime(find(segColor == k,1,'first'):startPre);
        tmpDist = segRealDist(find(segColor == k,1,'first'):startPre);
        p = polyfit(tmpDist, tmpTime, 1);
        meanVLevel(k,1) = 1/p(1);
        plot(polyval(p,tmpDist),tmpDist,'Color',colorSeq{k}, 'LineWidth', 2); hold on;

        tmpTime = segAPTime(startAft:find(segColor == k,1,'last'));
        tmpDist = segRealDist(startAft:find(segColor == k,1,'last'));
        p = polyfit(tmpDist, tmpTime, 1);
        meanVLevel(k,2) = 1/p(1);
        plot(polyval(p,tmpDist),tmpDist,'Color',colorSeq{k}, 'LineWidth', 2); hold on;
    end
end

axes(ha(8)); 
c = 1;
for i = 1:4
    for j = 1:2
        if meanVLevel(i,j) ~= 0
            plot(c, meanVLevel(i,j),'color',colorSeq{i},'MarkerSize',10,'Marker','*'); hold on;
            c = c + 1;
        end
    end
end
xlabel('part number (#)');
ylabel('velocity (\mum/ms)');
axis([0 length(meanVLevel)+1 min(meanVLevel(:))-10 max(meanVLevel(:))+10]);
set(gca,'XTick',0:1:c);
title('mean velocity of parts');


saveas(gca,[ResAddr 'ALL.fig']);
saveas(gca,[ResAddr 'ALL.png']);    
saveas(gca,[resAddr 'ALL.fig']);
saveas(gca,[resAddr 'ALL.png']); 
save([ResAddr 'meanVLevel.mat'],'meanVLevel','-v7.3');
save([ResAddr 'meanVMark.mat'],'meanVLevel','-v7.3');


%% ---------------- read current and patch info -----------------


% Ra, Rm, Cm from patch maram.txt    
patchtxtExist = 0;
paths = regexp(pathname, '/', 'split');
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
patchpara = zeros(1,3);
patchpara(1) = Ra;
patchpara(2) = Rm;
patchpara(3) = Cm;
disp(['Ra  Rm  Cm: ' num2str(patchpara)]);


restV = smooth(patch,double(lkernel));
restV = mean(restV);
peakV = findpeaks(patch, 'minpeakdistance', lcycle * frameratio - 100, 'minpeakheight', 0);
peakV = mean(peakV);
elecpara(1) = restV;
elecpara(2) = peakV;
disp(['restV peakV: ' num2str(elecpara)]);

% If the neuron is qualified, keep this neuron
save([ResAddr 'current.mat'], 'current', '-v7.3');
save([ResAddr 'patchpara.mat'], 'patchpara', '-v7.3');
save([ResAddr 'elecpara.mat'], 'elecpara', '-v7.3');


close all;
axontype = input('Is the axon somatic or dendritic (s/d)?','s');
if axontype == 's' || axontype == 'd'
    save([ResAddr 'axontype.mat'], 'axontype', '-v7.3');
else
    error('Axon type input error.');
end





