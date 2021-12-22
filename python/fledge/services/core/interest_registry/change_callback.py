# -*- coding: utf-8 -*-

# FLEDGE_BEGIN
# See: http://fledge-iot.readthedocs.io/
# FLEDGE_END

""" Module to hold the callback to notify microservices of config changes. """

import json
import asyncio
import aiohttp
from fledge.common.configuration_manager import ConfigurationManager
from fledge.services.core.service_registry.service_registry import ServiceRegistry
from fledge.services.core.service_registry import exceptions as service_registry_exceptions
from fledge.services.core.interest_registry.interest_registry import InterestRegistry
from fledge.services.core.interest_registry import exceptions as interest_registry_exceptions
from fledge.common import logger

__copyright__ = "Copyright (c) 2017 OSIsoft, LLC"
__license__ = "Apache 2.0"
__version__ = "${VERSION}"

_LOGGER = logger.setup(__name__)


async def run(category_name):
    """ Callback run by configuration category to notify changes to interested microservices

    Note: this method is async as needed

    Args:
        configuration_name (str): name of category that was changed
    """

    # get all interest records regarding category_name
    cfg_mgr = ConfigurationManager()
    interest_registry = InterestRegistry(cfg_mgr)
    try:
        interest_records = interest_registry.get(category_name=category_name)
    except interest_registry_exceptions.DoesNotExist:
        return

    category_value = await cfg_mgr.get_category_all_items(category_name)
    payload = {"category" : category_name, "items" : category_value}
    headers = {'content-type': 'application/json'}

    # for each microservice interested in category_name, notify change
    for i in interest_records:
        # get microservice management server info of microservice through service registry
        try: 
            service_record = ServiceRegistry.get(idx=i._microservice_uuid)[0]
        except service_registry_exceptions.DoesNotExist:
            _LOGGER.exception("Unable to notify microservice with uuid %s as it is not found in the service registry", i._microservice_uuid)
            continue
        url = "{}://{}:{}/fledge/change".format(service_record._protocol, service_record._address, service_record._management_port)

        #// FIXME_I:
        import logging


        #// FIXME_I:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("xxx15 run  url :{}: :{}: -".format(url, payload) )
        _LOGGER.setLevel(logging.WARNING)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data=json.dumps(payload, sort_keys=True), headers=headers) as resp:
                    result = await resp.text()
                    status_code = resp.status
                    if status_code in range(400, 500):
                        _LOGGER.error("Bad request error code: %d, reason: %s", status_code, resp.reason)
                    if status_code in range(500, 600):
                        _LOGGER.error("Server error code: %d, reason: %s", status_code, resp.reason)
            except Exception as ex:
                _LOGGER.exception("Unable to notify microservice with uuid %s due to exception: %s", i._microservice_uuid, str(ex))
                continue


async def run_child(parent_category_name, child_category_list):
    """ Callback run by configuration category to notify changes to interested microservices

    Note: this method is async as needed

    Args:
        configuration_name (str): name of category that was changed
    """

    # get all interest records regarding category_name
    cfg_mgr = ConfigurationManager()
    interest_registry = InterestRegistry(cfg_mgr)
    try:
        interest_records = interest_registry.get(category_name=parent_category_name)
    except interest_registry_exceptions.DoesNotExist:
        return

    #// FIXME_I:
    child_category=child_category_list[0]

    category_value = await cfg_mgr.get_category_all_items(child_category)
    payload = {"parent_category" : parent_category_name, "category" : child_category, "items" : category_value}
    headers = {'content-type': 'application/json'}

    # for each microservice interested in category_name, notify change
    for i in interest_records:
        # get microservice management server info of microservice through service registry
        try:
            service_record = ServiceRegistry.get(idx=i._microservice_uuid)[0]
        except service_registry_exceptions.DoesNotExist:
            _LOGGER.exception("Unable to notify microservice with uuid %s as it is not found in the service registry", i._microservice_uuid)
            continue
        url = "{}://{}:{}/fledge/change_child".format(service_record._protocol, service_record._address, service_record._management_port)

        #// FIXME_I:
        import logging

        #// FIXME_I:
        _LOGGER.setLevel(logging.DEBUG)
        _LOGGER.debug("xxx16 run_child category_name  :{}: child_category :{}: -".format(parent_category_name, child_category))
        _LOGGER.debug("xxx16 run_child  url :{}: payload :{}: -".format(url, payload) )
        _LOGGER.setLevel(logging.WARNING)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data=json.dumps(payload, sort_keys=True), headers=headers) as resp:
                    result = await resp.text()
                    status_code = resp.status
                    if status_code in range(400, 500):
                        _LOGGER.error("Bad request error code: %d, reason: %s", status_code, resp.reason)
                    if status_code in range(500, 600):
                        _LOGGER.error("Server error code: %d, reason: %s", status_code, resp.reason)
            except Exception as ex:
                _LOGGER.exception("Unable to notify microservice with uuid %s due to exception: %s", i._microservice_uuid, str(ex))
                continue
