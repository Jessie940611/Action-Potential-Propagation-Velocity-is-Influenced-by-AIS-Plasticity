function [maskDendSum, clineDendSum, realDistSum, dendType, clineDendMark, antiImg1] = click_dendrite(refimg, savepath, path, distPerPix, mode)
% click the center line of dendrite
% get the binary image and center line of dendrite
%     mode: 1-click single dendrite; 2-click dendrite and cut it into two

    fl = regexp(path, '/', 'split');
    antipath = [];
    for i = 2:length(fl)-2
        antipath = [antipath '/' fl{i}];
    end
    list = dir(antipath);
    for i = 1:length(list)
        if contains(list(i).name, 'patch') && list(i).isdir == 1
            break;
        end
    end   
    antipath = [antipath '/' list(i).name];
    list = dir(antipath);
    for i = 1:length(list)
        if (contains(list(i).name, 'Anti') || contains(list(i).name, '405')) && contains(list(i).name, 'tif')
            break;
        end
    end
    
    antiImg1 = imread([antipath '/' list(i).name]);
    mx = max(antiImg1(:)) * 0.8;
    antiImg1(antiImg1>mx) = mx;
    antiImg1 = double(antiImg1-min(antiImg1(:)))/double(max(antiImg1(:)-min(antiImg1(:))))*double(254)+1;  

 
    width = 2;
    
    fl = regexp(path, '/', 'split');
    mergeImgPath = [];
    for i = 2:length(fl)-2
        mergeImgPath = [mergeImgPath '/' fl{i}];
    end
    mergeImg = imread([mergeImgPath '/Composite.png']);
    
    figure;
    set(gcf, 'outerposition',get(0,'screensize'));
    
%     Img = imread([path 'Composite.png']);
    ax1 = subplot(2,2,1);
    title('Neurofascin');
    set(gca,'Position',[0.02,0.02,0.2,0.3]);
    imagesc(mergeImg); axis image; axis off;
    map = zeros(255,3);
    map(2:end,2) = linspace(0,1,254);
    map(2:end,3) = linspace(0,1,254);
    map(1,:) = [1,1,1];
    colormap(ax1, map);
    %text(260,195,'10 \mum', 'Color','w','FontSize', 10, 'FontWeight', 'bold');    
    
    subplot(1,2,2);
    set(gca, 'Position', [0.2,0.02,0.8,0.98]);
%     figure;
%     set(gcf, 'Position', [100,300,2000,800]);
    imagesc(refimg); axis image;
    if mode == 1
        title(['Please draw the centerline of the axon ' '(draw several single dendrite)'], 'position',[110,0.5]);
    else
        title(['Please draw the centerline of the axon ' '(draw a long dendrite)'], 'position',[110,0.5]);
    end
    hold on;

    [nrow,ncol,~] = size(refimg);   
    maskDendSum = {};
    clineDendSum = {};
    realDistSum = {};
    if mode == 1
        % draw the center line of axon and the maskAxon
        maskDend = zeros(nrow,ncol);
        clineDend = [];
        [clickX, clickY] = getline(gca);
        ndend = 0;
        % set the direction
        deltx = abs(clickX(1)-clickX(end));
        delty = abs(clickY(1)-clickY(end));
        if deltx > delty
            directAll = 1;
        else
            directAll = 2;
        end

        while ~isempty(clickX)
            ndend = ndend + 1;
            for i = 1:length(clickX)-1
                deltx = abs(clickX(i)-clickX(i+1));
                delty = abs(clickY(i)-clickY(i+1));
                if deltx > delty
                    directPart = 1;
                    a = polyfit(clickX(i:i+1),clickY(i:i+1),1);
                    x = min(clickX(i:i+1)):0.1:max(clickX(i:i+1));
                    y = a(1) .* x + a(2);
                    if abs(clickX(i)-x(1)) > abs(clickX(i)-x(end))
                        x = flip(x);
                        y = flip(y);
                    end
                else
                    directPart = 2;
                    a = polyfit(clickY(i:i+1),clickX(i:i+1),1);
                    y = min(clickY(i:i+1)):0.1:max(clickY(i:i+1));
                    x = a(1).* y + a(2);
                    if abs(clickX(i)-x(1)) > abs(clickX(i)-x(end))
                        x = flip(x);
                        y = flip(y);
                    end
                end   

                clineDend = [clineDend;[round(y(1)),round(x(1))]];
                for j = 2:length(x)
                    if round(x(j)) == clineDend(end,2) && round(y(j)) == clineDend(end,1)
                        continue;
                    end
                    tx = round(x(j));
                    ty = round(y(j));
                    clineDend = [clineDend;[ty,tx]];
                end
                ccn = 0;
                for j = 2:length(clineDend)-1
                    k = j-ccn;
                    if (clineDend(k-1,1) == clineDend(k,1) && clineDend(k,2) == clineDend(k+1,2)) ||...
                            (clineDend(k-1,2) == clineDend(k,2) && clineDend(k,1) == clineDend(k+1,1))
                        clineDend(k,:) = [];
                        ccn = ccn + 1;
                        continue;
                    end
                    tx = clineDend(k,2);
                    ty = clineDend(k,1);
                    maskDend(ty-width:ty+width, tx-width:tx+width) = 1;
                end            
            end
            maskDendSum{ndend} = maskDend;
            clineDendSum{ndend} = clineDend;
            plot(clineDend(:,2),clineDend(:,1),'w.','MarkerSize',8);
            dendType(ndend) = input('level (0-mother, 1-daughter): ');
            clear clickX clickY;
            text(mean(clineDend(:,2)),mean(clineDend(:,1)), ...
                ['No',num2str(ndend),': ','level ',num2str(dendType(ndend))],...
                'Color','k','FontSize', 10, 'FontWeight', 'bold');

            realDist = zeros(1,length(clineDend));
            realDist(1) = distPerPix/2;
            for i = 2 : length(clineDend)
                pixel_a = clineDend(i, :);
                pixel_b = clineDend(i - 1, :);
                if pixel_a(:,1) == pixel_b(:,1) || pixel_a(:,2) == pixel_b(:,2)
                    dist = distPerPix;
                else
                    dist = sqrt(2) * distPerPix;
                end
                realDist(i) = realDist(i-1) + dist;
            end
            realDistSum{ndend} = realDist;

            maskDend = zeros(nrow,ncol);
            clineDend = [];
            [clickX, clickY] = getline(gca);
        end
        
        clineDendMark = 0;
        save([savepath, 'maskDendSum_mode1.mat'], 'maskDendSum', '-v7.3');
        save([savepath, 'clineDendSum_mode1.mat'], 'clineDendSum', '-v7.3');
        save([savepath, 'realDistSum_mode1.mat'], 'realDistSum', '-v7.3');
        
        saveas(gca,[savepath 'click_image_mode1.fig']);
        saveas(gca,[savepath 'click_image_mode1.png']);
    else
        % draw the center line of axon and the maskAxon
        maskDend = zeros(nrow,ncol);
        clineDend = [];
        [clickX, clickY] = getline(gca);
        ndend = 1;
        % set the direction
        deltx = max(clickX)-min(clickX);
        delty = max(clickY)-min(clickY);
        if deltx > delty
            directAll = 1;
        else
            directAll = 2;
        end

        for i = 1:length(clickX)-1
            deltx = abs(clickX(i)-clickX(i+1));
            delty = abs(clickY(i)-clickY(i+1));
            if deltx > delty
                directPart = 1;
                a = polyfit(clickX(i:i+1),clickY(i:i+1),1);
                x = min(clickX(i:i+1)):0.1:max(clickX(i:i+1));
                y = a(1) .* x + a(2);
                if abs(clickX(i)-x(1)) > abs(clickX(i)-x(end))
                    x = flip(x);
                    y = flip(y);
                end
            else
                directPart = 2;
                a = polyfit(clickY(i:i+1),clickX(i:i+1),1);
                y = min(clickY(i:i+1)):0.1:max(clickY(i:i+1));
                x = a(1).* y + a(2);
                if abs(clickX(i)-x(1)) > abs(clickX(i)-x(end))
                    x = flip(x);
                    y = flip(y);
                end
            end   

            clineDend = [clineDend;[round(y(1)),round(x(1))]];
            for j = 2:length(x)
                if round(x(j)) == clineDend(end,2) && round(y(j)) == clineDend(end,1)
                    continue;
                end
                tx = round(x(j));
                ty = round(y(j));
                clineDend = [clineDend;[ty,tx]];
            end
            ccn = 0;
            for j = 2:length(clineDend)-1
                k = j-ccn;
                if (clineDend(k-1,1) == clineDend(k,1) && clineDend(k,2) == clineDend(k+1,2)) ||...
                        (clineDend(k-1,2) == clineDend(k,2) && clineDend(k,1) == clineDend(k+1,1))
                    clineDend(k,:) = [];
                    ccn = ccn + 1;
                    continue;
                end
                tx = clineDend(k,2);
                ty = clineDend(k,1);
                maskDend(ty-width:ty+width, tx-width:tx+width) = 1;
            end            
        end    
        maskDendSum{ndend} = maskDend;
        clineDendSum{ndend} = clineDend;
        plot(clineDend(:,2),clineDend(:,1),'w.','MarkerSize',8);
        clear clickX clickY;

        realDist = zeros(1,length(clineDend));
        realDist(1) = distPerPix/2;
        for j = 2 : length(clineDend)
            pixel_a = clineDend(j, :);
            pixel_b = clineDend(j - 1, :);
            if pixel_a(:,1) == pixel_b(:,1) || pixel_a(:,2) == pixel_b(:,2)
                dist = distPerPix;
            else
                dist = sqrt(2) * distPerPix;
            end
            realDist(j) = realDist(j-1) + dist;
        end
        realDistSum{ndend} = realDist;

        % cut the axon with several lines
        maskCut = maskDendSum{1};
        bdpoint = [];
        [clickX, clickY] = getline(gca); 
        while ~isempty(clickX)
            bdpoint = [bdpoint;[clickX, clickY]];
            deltx = abs(clickX(1)-clickX(2));
            delty = abs(clickY(1)-clickY(2));
            if deltx > delty
                a = polyfit(clickX,clickY,1);
                x = min(clickX):0.1:max(clickX);
                y = a(1) .* x + a(2);
            else
                a = polyfit(clickY,clickX,1);
                y = min(clickY):0.1:max(clickY);
                x = a(1).* y + a(2);
            end
            for i = 1:length(x)
                maskCut(round(y(i)),round(x(i))) = 0;
            end
            plot(clickX,clickY,'Linewidth',1,'Color','w');
            [clickX, clickY] = getline(gca);  
        end
        clineDendMark = zeros(length(clineDend),1);
        [~, logic] = bwboundaries(maskCut,4);
        for j = 1:length(clineDendMark)
            tmp = logic(clineDend(j,1),clineDend(j,2));
            if tmp ~= 0
                clineDendMark(j) = tmp;
            elseif j ~= 1
                clineDendMark(j) = clineDendMark(j-1);
            else
                clineDendMark(j) = clineDendMark(j+1);
            end
        end
        
        [C,~,~] = unique(clineDendMark,'stable');
        if clineDendMark(1) ~= 1
            tmp = clineDendMark;
            for j = 1:max(logic(:))
                clineDendMark(tmp == C(j)) = j;
            end
        end

        colorSeq = {'r','b','m','g','c','y','k'};
        for j = 1:max(clineDendMark)
            tmp = clineDend(clineDendMark == j,:);
            plot(tmp(:,2),tmp(:,1),'Color', colorSeq{j},'Marker','.','MarkerSize',8);
        end
        
        dendType = 0;
        save([savepath, 'maskDendSum_mode2.mat'], 'maskDendSum', '-v7.3');
        save([savepath, 'clineDendSum_mode2.mat'], 'clineDendSum', '-v7.3');
        save([savepath, 'realDistSum_mode2.mat'], 'realDistSum', '-v7.3');
        save([savepath, 'clineDendMark_mode2.mat'], 'clineDendMark', '-v7.3');
        
        saveas(gca,[savepath 'click_image_mode2.fig']);
        saveas(gca,[savepath 'click_image_mode2.png']);
    end
    
end
