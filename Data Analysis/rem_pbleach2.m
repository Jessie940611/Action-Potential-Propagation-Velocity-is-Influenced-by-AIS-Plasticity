function [ mov_bleach, intensN ] = rem_pbleach2( mov, maskAxon, nrow, ncol, nframes, lkernel )
    
    intens = squeeze(sum(sum(mov.*repmat(maskAxon, [1, 1, nframes]))))/sum(maskAxon(:));
    pbleach = imerode(intens,ones(lkernel/4,1));    
    pbleach = smooth(pbleach,double(lkernel*2));
    
    mov_bleach = zeros(nrow, ncol, nframes);     
    for i = 1:nrow
        for j = 1:ncol
            if maskAxon(i,j) == 1
                mov_bleach(i,j,:) = mov(i,j,:)./reshape(pbleach,1,1,length(pbleach));
            end
        end
    end
    
    intensN = squeeze(sum(sum(mov_bleach.*repmat(maskAxon, [1, 1, nframes]))))/sum(maskAxon(:));
    
end

