# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import shutil
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
    GIT_URL = "https://github.com/OGalOz/rbts_download_tables.git"
    GIT_COMMIT_HASH = "b8d14eed5dbe387c23b979f749f94e2b5128f614"

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
        if "app_test" in params and params["app_test"]:
            if os.path.exists(ret_dp):
                logging.warning(f"Removing existing workdir at {ret_dp}.")
                shutil.rmtree(ret_dp)
        os.mkdir(ret_dp)

        if "input_table_refs" not in params:
            raise Exception("Params 'input_table_refs' needed to run program. Not found.")
        else:
            if not isinstance(params["input_table_refs"], list):
                raise Exception("Expecting param input_table_refs to be a list"
                                f", instead got {type(params['input_table_refs'])}")
            for ref in params["input_table_refs"]:
                # Making sure there are no duplicates
                if params["input_table_refs"].count(ref) > 1:
                    raise Exception(f"Duplicate data object found with ref {ref}.")
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
            'report_ref': report_info['ref']
        }

        #END run_rbts_download_tables

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_rbts_download_tables return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def download_KB_RBTS_table(self, ctx, params):
        """
        :param params: instance of type "DownloadTableParams" -> structure:
           parameter "input_table_refs" of type "input_table_refs" -> list of
           type "rbts_ref" (rbts_ref is the ref of any of the objects)
        :returns: instance of type "DownloadTableResults" (exit_code (int)
           success is 0, failure is 1 filepath (str) path to where the
           downloaded table is) -> structure: parameter "exit_code" of Long,
           parameter "filepath" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN download_KB_RBTS_table

        dfu = DataFileUtil(self.callback_url)

        # Making return directory
        ret_dp = os.path.join(self.shared_folder, "ret_dir")
        if "app_test" in params and params["app_test"]:
            if os.path.exists(ret_dp):
                logging.warning(f"Removing existing workdir at {ret_dp}.")
                shutil.rmtree(ret_dp)
        os.mkdir(ret_dp)

        ref2fps = []
        exit_code = 0 
        if "input_table_refs" not in params:
            raise Exception("Params 'input_table_refs' needed to run program. Not found.")
        else:
            if not isinstance(params["input_table_refs"], list):
                raise Exception("Expecting param input_table_refs to be a list"
                                f", instead got {type(params['input_table_refs'])}")
            for ref in params["input_table_refs"]:
                try:
                    # Making sure there are no duplicates
                    if params["input_table_refs"].count(ref) > 1:
                        raise Exception(f"Duplicate data object found with ref {ref}.")
                    logging.info(f"Beginning download process for ref {ref}")
                    locs = download_table_from_ref_to_dir(ref, ret_dp, dfu)
                    ref2fpTuple = {
                            "ref": ref,
                            "fps": locs
                    }
                    ref2fps.append(ref2fpTuple)
                except Exception as inst:
                    logging.critical("Download failed for ref: " + ref)
                    exit_code += 1
        
    
        output = {
            'exit_code': exit_code,
            'refs2fps': ref2fps 
        }

        logging.info("Finished downloading. Resulting structure:")
        logging.info(output)



        #END download_KB_RBTS_table

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method download_KB_RBTS_table return value ' +
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
