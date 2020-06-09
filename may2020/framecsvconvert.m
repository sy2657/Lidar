% convert to csv

frameStart = 1;
frameEnd = 300;

s1 = 0;
s2 = 0;

for i=frameStart:frameEnd
    dataframe = DataTotal{1, i};
    s2 = size(dataframe, 2);
    % try writing to file 
    fname = ['file_out' num2str(i) '.csv'];
    fid_out = fopen(fname,'w');
    disp(s2);
    for j=1:s2
       datacluster = dataframe{1, j};
       sizecluster = size(datacluster, 1);
       for k =1:sizecluster
           cx = datacluster(k, 1);
           cy = datacluster(k,2);
            % write cluster id, x and y
           fprintf(fid_out, '%d, %d, %d \n', j, cx, cy);
       end
    end
    fclose(fid_out);
end



