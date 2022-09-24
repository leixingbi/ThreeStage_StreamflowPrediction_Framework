function nonstationary_rusult=NonstationaryAssessmentRbeast()
    % help beast
    % plotbeast(out);
    load("nonstationary_assess_data.mat")
    load("data_start_time.mat")

    out=beast(nonstationary_assess_data, 'start', data_start_time, 'deltat', 1/12, 'freq',12, "season", 'harmonic', "scp.minmax", [0,10],  "sorder.minmax", [1,3], "sseg.min", 12,  "tseg.min", 12,  "tcp.minmax", [0,10]);

    delete("result_NonstationaryAssess.txt")
    diary("result_NonstationaryAssess.txt");
    printbeast(out);
    diary off;


    nonstationary_rusult = 0;
end

 