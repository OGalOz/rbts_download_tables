# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
from util.download_tables import download_table_from_ref_to_dir

from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
#END_HEADER


class rbts_download_tables:
    '''
    Module Name:
    rbts_download_tables

    Module Description:
    A KBase module: rbts_download_tables
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        #END_CONSTRUCTOR
        pass


    def run_rbts_download_tables(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_rbts_download_tables

        dfu = DataFileUtil(self.callback_url)

        # Making return directory
        ret_dp = os.path.join(self.shared_folder, "ret_dir")
        os.mkdir(ret_dp)

        if "input_table_refs" not in params:
            raise Exception("Params 'input_table_refs' needed to run program. Not found.")
        else:
            if not isinstance(params["input_table_refs"], list):
                raise Exception("Expecting param input_table_refs to be a list"
                                f", instead got {type(params['input_table_refs'])}")
            for ref in params["input_table_refs"]:
                logging.info(f"Beginning download process for ref {ref}")
                download_table_from_ref_to_dir(ref, ret_dp, dfu)


        # Returning directory in zipped format:-------------------------------
        file_zip_shock_id = dfu.file_to_shock({'file_path': ret_dp,
                                              'pack': 'zip'})['shock_id']

        dir_link = {
                'shock_id': file_zip_shock_id, 
               'name':  'results.zip', 
               'label':'download_tables_results', 
               'description': 'The directory of outputs from running' \
                + ' RBTS Download Tables.'
        }

        report_util = KBaseReport(self.callback_url)
        report_info = report_util.create_extended_report({
                                        'message': "Finished running RBTS Download Tables.",
                                        'file_links': [dir_link],
                                        'workspace_name': params['workspace_name']
                                        })

        logging.info("report_info after creating extended report.")
        logging.info(report_info)

        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref'],
        }
        #END run_rbts_download_tables

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_rbts_download_tables return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
