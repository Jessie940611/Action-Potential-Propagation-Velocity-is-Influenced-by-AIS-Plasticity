function [ meanMov, meanSpike, mark] = mean_movie_spike( mov, mask, lmovie, spikeT, threshv)

    % get the mean AP movie of the whole roi
    [nrow, ncol, nframes] = size(mov);
    itrace = squeeze(sum(sum(mov.*repmat(mask, [1, 1, nframes]))))/sum(mask(:));
    meanMov = zeros(nrow, ncol, lmovie);
    meanSpike = zeros(1, lmovie);
    figure; set(gcf, 'Position', [100,300,1000,400]);
    subplot(1,2,1); set(gca, 'Position', [0.05,0.15,0.4,0.7]); 
    plot(itrace); title('ROI intensity');    
    axis([0,length(itrace),min(itrace),max(itrace)+0.05]);
    
    nspike = length(spikeT);
    nadd = 0;
    mark = zeros(1,nspike);
    for j = 1:nspike
        range = spikeT(j)-floor(lmovie/6):spikeT(j)+floor(5*lmovie/6);
        if range(end) > length(itrace)
            continue;
        end
        while range(1) <= 0
            range(1) = [];
        end
        if max(itrace(range)) > threshv
            mark(j) = 1;
            meanMov = meanMov + mov(:,:,range);
            meanSpike = meanSpike + reshape(itrace(range,:),1,lmovie);
            nadd = nadd + 1;
            hold on; plot(spikeT(j),itrace(spikeT(j)),'r*');
        end
    end
    meanMov = meanMov/nadd;
    meanSpike = meanSpike/nadd;

end

