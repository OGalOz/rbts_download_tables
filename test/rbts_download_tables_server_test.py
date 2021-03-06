# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from rbts_download_tables.rbts_download_tablesImpl import rbts_download_tables
from rbts_download_tables.rbts_download_tablesServer import MethodContext
from rbts_download_tables.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class rbts_download_tablesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('rbts_download_tables'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'rbts_download_tables',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = rbts_download_tables(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_download_rbts_table_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_MutantPool_download1(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #

        test_d = {
                "workspace_name": self.wsName,
                "input_table_refs": ['63063/44/1'],
                "app_test": True 
        }

        ret = self.serviceImpl.run_rbts_download_tables(self.ctx, test_d)

    def test_MutantPool_download2(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #

        test_d = {
                "workspace_name": self.wsName,
                "input_table_refs": ['63063/44/1'],
                "app_test": True 
        }

        ret = self.serviceImpl.download_KB_RBTS_table(self.ctx, test_d)

    '''
    def test_BarcodeCount_download1(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #

        test_d = {
                "workspace_name": self.wsName,
                "input_table_refs": ['63063/44/1'],
                "app_test": True 
        }

        ret = self.serviceImpl.run_rbts_download_tables(self.ctx, test_d)
    def test_BarcodeCount_download2(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #

        test_d = {
                "workspace_name": self.wsName,
                "input_table_refs": ['63063/44/1'],
                "app_test": True 
        }

        ret = self.serviceImpl.run_rbts_download_tables(self.ctx, test_d)

    '''
    '''
    def test_RBTS_ExperimentsTable_download(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #

        test_d = {
                "workspace_name": self.wsName,
                "input_table_refs": ['63063/44/1'],
                "app_test": True 
        }

        ret = self.serviceImpl.run_rbts_download_tables(self.ctx, test_d)
    '''
