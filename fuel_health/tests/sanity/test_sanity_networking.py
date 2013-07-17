from nose.plugins.attrib import attr
from nose.tools import timed

from fuel_health.tests.sanity import base


class NetworksTest(base.BaseNetworkTest):
    """
    TestClass contains tests check base networking functionality
    """

    @attr(type=['sanity', 'fuel'])
    @timed(5.5)
    def test_list_networks(self):
        """Test checks that available networks can be listed."""
        resp, body = self.client.list_networks()
        self.verify_response_status(resp.status, u'Network (Neutron or Nova)')
        self.verify_response_body(body, u'networks',
                                  "Network list is unavailable. "
                                  "Looks like something is broken in Network "
                                  "(Neutron or Nova).")

    @attr(type=['sanity', 'fuel'])
    @timed(5.5)
    def test_list_ports(self):
        """Test checks that existing ports can be listed."""
        resp, body = self.client.list_ports()
        self.verify_response_status(resp.status, u'Network (Neutron or Nova)')
        self.verify_response_body(body, u'ports',
                                  'Ports list is unavailable. '
                                  'Looks like something is broken in Network '
                                  '(Neutron or Nova).')