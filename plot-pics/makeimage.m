file = 'test_example.csv'
thisMat= readtable(file)
M = csvread(file)
figure;
        pcolor(M)
        shading flat
        axis off