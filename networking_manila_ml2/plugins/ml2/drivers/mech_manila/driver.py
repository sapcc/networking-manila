# Copyright 2014 IBM Corp.
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

from neutron.extensions import portbindings
from neutron.i18n import _LI
from neutron.plugins.common import constants as p_constants

from neutron.plugins.ml2.drivers import mech_agent
from neutron.plugins.ml2 import driver_api as api
from oslo_log import log
from networking_manila_ml2.plugins.ml2.drivers.mech_manila import constants as manila_constants

LOG = log.getLogger(__name__)



class ManilaMechanismDriver(api.MechanismDriver):

    def __init__(self):
        LOG.info(_LI("ASR mechanism driver initializing..."))

        self.vif_type = manila_constants.VIF_TYPE_MANILA
        self.vif_details = {portbindings.CAP_PORT_FILTER: False}




    def initialize(self):
        pass


    def bind_port(self, context):

        # For now we will just bind the last segment
        if context.segments_to_bind:
            segment = context.segments_to_bind.pop()

            device_owner = context.current['device_owner']

            if device_owner and device_owner.startswith('manila'):
                context.set_binding(segment[api.ID], self.vif_type, self.vif_details, p_constants.ACTIVE)
                return True