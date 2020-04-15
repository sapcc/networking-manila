# Copyright 2018 SAP SE
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

from networking_manila_ml2._i18n import _LI
from networking_manila_ml2.plugins.ml2.drivers.mech_manila import constants
from neutron_lib import constants as p_constants
from neutron_lib.api.definitions import portbindings
from neutron_lib.plugins.ml2 import api
from oslo_config import cfg
from oslo_log import log

LOG = log.getLogger(__name__)


cfg.CONF.import_group('ml2_manila',
                      'networking_manila_ml2.plugins.ml2.drivers.mech_manila.config')


class ManilaMechanismDriver(api.MechanismDriver):
    def __init__(self):
        LOG.info(_LI("Manila mechanism driver initializing..."))
        self.agent_type = constants.MANILA_AGENT_TYPE
        self.vif_type = constants.VIF_TYPE_MANILA
        self.vif_details = {portbindings.CAP_PORT_FILTER: False}
        self.physical_networks = cfg.CONF.ml2_manila.physical_networks

        super(ManilaMechanismDriver, self).__init__()

        LOG.info(_LI("Manila mechanism driver initialized."))

    def initialize(self):
        pass

    def bind_port(self, context):
        device_owner = context.current['device_owner']
        if device_owner and device_owner.startswith('manila:'):
            # bind to first segment if no physical networks are configured
            if self.physical_networks is None:
                self._set_binding(context, context.segments_to_bind[0])
                return True

            # bind to first segment present in list of physical networks
            for segment in context.segments_to_bind:
                if segment[api.PHYSICAL_NETWORK] in self.physical_networks:
                    self._set_binding(context, segment)
                    return True

            LOG.error("No segment matches the configured physical networks "
                      "%(physical_networks)s",
                      {'physical_networks': self.physical_networks})
        return False

    def _set_binding(self, context, segment):
        context.set_binding(segment[api.ID],
                            self.vif_type,
                            self.vif_details,
                            p_constants.ACTIVE)
