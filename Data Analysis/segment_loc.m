function [ maskSeg, boundSeg ] = segment_loc( mask, cline, index, seglen)
% find the small segment's location
%    maskSeg: the mask of the segment
%    boundSeg: the boundary of the segment
    
    % find the segment
    [nrow, ncol] = size(mask);
    maskSeg = zeros(size(mask));
    for i = index-floor(seglen/2-0.1) : index+floor(seglen/2)
        cx = cline(i,1);
        cy = cline(i,2);
        if cx - 2 <= 0
            cx = 3;
        end
        if cy - 2 <= 0
            cy = 3;
        end
        if cx + 2 >= nrow
            cx = nrow - 2;
        end
        if cy + 2 >= ncol
            cy = ncol - 2;
        end            
        maskSeg(cx-2:cx+1,cy-2:cy+2) = 1;
    end
    [segbound, seglogic] = bwboundaries(maskSeg,4);

    if seglogic(cline(index,1),cline(index,2)) ==0
        boundSeg = segbound(1);
    else
        boundSeg = segbound(seglogic(cline(index,1),cline(index,2)));
    end
    boundSeg = boundSeg{:};
end

