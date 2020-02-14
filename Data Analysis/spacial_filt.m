function out = spacial_filt2( movie, lkernel, nframes, nrow, ncol )
% return a spatially filtered movie, where the Gaussian kernel is of
% dimention [filtsize, filtsize], with standard deviation sigma.
% The filtering is done with a weighted mean, where each pixel is weighted
% by its standard deviation. This preferentially weights active pixels in
% the output movie.

    filtSize = 3;
    sigma = 1;
   
    intens = squeeze(sum(sum(movie)))/sum(nrow * ncol);
    pbleach = medfilt2(intens,[lkernel/2 1],'symmetric');
    pbleach = smooth(pbleach,double(lkernel));

    stdImg = std(movie./repmat(reshape(pbleach',1,1,nframes), [nrow,ncol,1]), [], 3);
    H = fspecial('gaussian', [filtSize, filtSize], sigma);

    out = imfilter(movie.*repmat(stdImg, [1 1 nframes]), H, 'replicate')./...
        repmat(imfilter(stdImg, H, 'replicate'), [1 1 nframes]);

end

