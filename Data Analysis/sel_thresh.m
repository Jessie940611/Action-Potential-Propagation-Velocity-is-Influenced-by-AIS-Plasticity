function [ threshv ] = sel_thresh( intensity, path )

    figure; plot(intensity); title('select threshold');
    [~,threshv] = ginput(1);
    save([path 'threshv.mat'], 'threshv', '-v7.3');

end

