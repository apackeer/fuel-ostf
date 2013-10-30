#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import unittest2
from mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker

from fuel_plugin.ostf_adapter.storage import engine


class BaseWSGITest(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.Session = sessionmaker()
        cls.engine = engine.get_engine(
            dbpath='postgresql+psycopg2://ostf:ostf@localhost/ostf'
        )

    def setUp(self):
        #orm session wrapping
        connection = self.engine.connect()
        self.trans = connection.begin()

        self.Session.configure(bind=connection)
        self.session = self.Session()

        #test case level patching

        #mocking
        #request mocking
        self.request_mock = MagicMock()

        self.request_patcher = patch(
            'fuel_plugin.ostf_adapter.wsgi.controllers.request',
            self.request_mock
        )
        self.request_patcher.start()

        #pecan conf mocking
        self.pecan_conf_mock = MagicMock()
        self.pecan_conf_mock.nailgun.host = '127.0.0.1'
        self.pecan_conf_mock.nailgun.port = 8888

        #engine.get_session mocking
        self.request_mock.session = self.session

    def tearDown(self):
        #rollback changes to database
        #made by tests
        self.trans.rollback()
        self.session.close()

        #end of test_case patching
        self.request_patcher.stop()
