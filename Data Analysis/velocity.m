function [ velocityLoc, velocity, loc, time] = velocity( segRealDist, segAPTime )
% this function is to calculate the velocity along the axon
% input: 30% peak time of each segment
%        the real segment location
%        start dist
% output: velocity along axon

% inte_dx = 0.5; % (um)
% window = 5; % window * dx (um)
% vel_dx = 3;
% loc = min(segRealDist):inte_dx:max(segRealDist);
% time_pre = interp1(segRealDist, segAPTime, loc, 'linear');
% time = smooth(time_pre, window, 'moving')';
% 
% index = 1:vel_dx:length(time);
% velocityLoc = (loc(index(1:length(index)-1)) + loc(index(2:end)))./2;
% velocity = repmat(vel_dx,1,length(velocityLoc)) .* inte_dx ./ diff(time(index),1);
% 
% delindex = find(velocity == inf);
% velocity(delindex) = [];
% velocityLoc(delindex) = [];
% 
% while(std(velocity) > 100)
%     threshVe = [mean(velocity) - 2*std(velocity), mean(velocity) + 2*std(velocity)];
%     delindex = find(velocity < threshVe(1));
%     delindex = [delindex find(velocity > threshVe(2))];
%     if isempty(delindex)
%         break;
%     end
%     velocity(delindex) = [];
%     velocityLoc(delindex) = [];
% end


% another method
p = polyfit(segRealDist, segAPTime, 2);
k = polyder(p);
velocityLoc = min(segRealDist):1:max(segRealDist);
velocity = 1./polyval(k, velocityLoc);
time = polyval(p, velocityLoc);
loc = 0;

end

