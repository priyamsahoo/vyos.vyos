# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The vyos prefix_lists fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.rm_templates.prefix_lists import (
    Prefix_listsTemplate,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.argspec.prefix_lists.prefix_lists import (
    Prefix_listsArgs,
)

class Prefix_listsFacts(object):
    """ The vyos prefix_lists facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = Prefix_listsArgs.argument_spec

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Prefix_lists network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = connection.get("show configuration commands | grep prefix-list")

        # parse native config using the Prefix_lists template
        prefix_lists_parser = Prefix_listsTemplate(lines=data.splitlines(), module=self._module)
        
        # if prefix_lists_parser.parse().get("ipv4"):
        #     objs = list(prefix_lists_parser.parse().get("ipv4").values())

        objs = prefix_lists_parser.parse()

        objs = [value for value in objs.values()]
        for item in objs:
            item['prefix_lists'] = [value for value in item['prefix_lists'].values()]

        ansible_facts['ansible_network_resources'].pop('prefix_lists', None)

        params = utils.remove_empties(
            prefix_lists_parser.validate_config(self.argument_spec, {"config": objs}, redact=True)
        )

        facts['prefix_lists'] = params['config']
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
