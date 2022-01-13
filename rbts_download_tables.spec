/*
A KBase module: rbts_download_tables
*/

module rbts_download_tables {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_rbts_download_tables(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;


    /*
        This function takes a KBaseRBTnSeq Data Table ref and returns a table 
    */

    /*
        rbts_ref is the ref of any of the objects
    */
    typedef string rbts_ref;


    typedef list<rbts_ref> input_table_refs;


    typedef structure {
        input_table_refs input_table_refs;
    } DownloadTableParams;

    /*
        exit_code (int) success is 0, failure is any number larger,
                        for each ref failure exit_code += 1.
        filepath (str) path to where the downloaded table is
    */

    typedef structure {
        int exit_code;
        string filepath;
    } DownloadTableResults;

    funcdef download_KB_RBTS_table(DownloadTableParams params) returns (DownloadTableResults output) authentication required;




};
