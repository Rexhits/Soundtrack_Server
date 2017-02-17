function [t, X] = generateBlocks(x, sample_rate_Hz, block_size, hop_size) 
%UNTITLED5 Summary of this function goes here
%   Detailed explanation goes here
    paddingCount = hop_size - mod(length(x) - block_size, hop_size);
    x(end+paddingCount) = 0;
    N = fix(length(x) / block_size) + 1;
    t = zeros(block_size * N, 1);
    X = zeros(N, block_size);
    for i = 1:N-1
        for n = i:i+block_size-1
            t(i) = n / sample_rate_Hz;
            X(i, n-i+1) = x(n);
        end
    end
end

