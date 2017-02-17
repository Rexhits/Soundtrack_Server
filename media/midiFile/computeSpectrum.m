function [f,XAbs,XPhase,XRe,XIm] = computeSpectrum(x, sample_rate_Hz) 
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
    fft_X = fft(x);
    n = fix(length(fft_X) / 2);
    i = 1 : n;
    fbin = i*sample_rate_Hz/(2*n);
    XAbs = abs(fft_X(1:n) / n);
    XPhase = angle(fft_X(1:n));
    XRe = real(fft_X(1:n));
    XIm = imag(fft_X(1:n));
    f = fbin(1:n);
end

