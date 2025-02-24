% D. Kaputa
% blenderLink.m
% Ravvenlabs

function image = blenderLink(client,width,height,x,y,z,pitch,roll,yaw,object)
    % send pose
    write(client,single([width,height,x,y,z,pitch,roll,yaw]));
    
    % specify object
    write(client,object)
    
    %get image data
    data = read(client,width*height*4);
    data = reshape(data,4,width,height);
    data = data(1:3,:,:);
    data = permute(data,[3 2 1]);
    image = flipud(data);
