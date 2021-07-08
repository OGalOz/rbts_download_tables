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

};
