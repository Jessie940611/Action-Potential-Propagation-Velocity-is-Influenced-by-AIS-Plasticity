function [ deltat, segAPTime, segAPFrame, tmpSpike] = ...
    calculate( meanMov, maskSeg, meanSpikeSpline, pmid, nrow, lmovie, tline, splinedelt, dt)

    % get the average action potential on this segment (mid-late,side-early)
    % deltat depend on where the center is
    if pmid(1) > nrow / 2
        deltat = tline * (double(pmid(1)) - double(nrow) / double(2) - double(1));
    else
        deltat = tline * (double(nrow) / double(2) - double(pmid(1)));
    end
    
    % mean spike on the segment
    spike = squeeze(sum(sum(meanMov.*repmat(maskSeg, [1, 1, lmovie]))))/sum(maskSeg(:));
    
    
    % cubic spline    
    ox = 0:1:lmovie-1;
    oy = spike;   
    ix = 0:splinedelt:lmovie-3;
    spikeSpline = spline(ox, oy, ix);
    
    
    tmpSpike = spikeSpline;
    % move
    if deltat ~= 0
        spikeSpline(round(deltat/dt/splinedelt):end) = spikeSpline(1:length(spikeSpline)-round(deltat/dt/splinedelt)+1);
    end
    

    % replace the spike with the meanSpikeSpline
    spikeSpline = (spikeSpline-min(spikeSpline))/(max(spikeSpline)-min(spikeSpline));
    meanSpikeSpline = (meanSpikeSpline-min(meanSpikeSpline))/(max(meanSpikeSpline)-min(meanSpikeSpline));
    
    
    indexKernel = find(meanSpikeSpline >= 0.5);
    if mod(length(indexKernel),2) == 0
        indexKernel = [indexKernel(1)-1, indexKernel];
    end
    kernel = meanSpikeSpline(indexKernel);
    indexM = indexKernel(1);
    lengthM = length(kernel);
    spikeCorr = imfilter(spikeSpline, kernel, 'same', 'corr');
    point = find(spikeCorr == max(spikeCorr),1);
    midp = floor(lengthM/2) + indexM;
    if point < midp
        trange = midp-point+1:length(meanSpikeSpline);
        spikeSpline(1:length(trange)) = meanSpikeSpline(trange);
        spikeSpline(length(trange)+1:end) = meanSpikeSpline(end);
    else
        trange = point-midp+1:length(spikeSpline);
        spikeSpline(trange) = meanSpikeSpline(1:length(trange));
        spikeSpline(1:point-midp) = meanSpikeSpline(1);
    end

    % calculate the spike time  
    segAPFrame = find(spikeSpline == max(spikeSpline),1);
    segAPTime = segAPFrame * splinedelt * dt;
end

