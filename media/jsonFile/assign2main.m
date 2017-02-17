[t1,x1] = generateSinusoidal(1.0, 44100, 400, 0.5, pi/2);
plot(t1,x1);
xlabel('time');
ylabel('amplitude');
axis([0 0.005 -1 1]);

[t2,x2] = generateSquare(1.0, 44100, 400, 0.5, 0);
plot(t2,x2);
xlabel('time');
ylabel('amplitude');
axis([0 0.005 min(x2) max(x2)]);

sample_rate_Hz = 44100;
[f1,XAbs1,XPhase1,XRe1,XIm1] = computeSpectrum(x1, sample_rate_Hz);
[f2,XAbs2,XPhase2,XRe2,XIm2] = computeSpectrum(x2, sample_rate_Hz);
subplot(2,1,1);
plot(f2, XAbs2, 'color', 'r');
hold on;
plot(f1, XAbs1, 'color', 'b');
xlabel('freq');
ylabel('magnitude');
subplot(2,1,2);
plot(XPhase2, 'color', 'r');
hold on;
plot(XPhase1, 'color', 'b');
xlabel('freq');
ylabel('magnitude');


