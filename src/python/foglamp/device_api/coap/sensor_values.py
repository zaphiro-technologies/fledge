# -*- coding: utf-8 -*-
"""FOGLAMP_PRELUDE_BEGIN
{{FOGLAMP_LICENSE_DESCRIPTION}}

See: http://foglamp.readthedocs.io/

Copyright (c) 2017 OSIsoft, LLC
License: Apache 2.0

FOGLAMP_PRELUDE_END
"""
import logging

from cbor2 import loads
import psycopg2
import aiocoap.resource
from sqlalchemy.dialects.postgresql import JSONB
import aiopg.sa
import sqlalchemy as sa

"""CoAP handler for coap://readings URI"""


_sensor_values_tbl = sa.Table(
    'readings',
    sa.MetaData(),
    sa.Column('asset_code', sa.types.VARCHAR(50)),
    sa.Column('read_key', sa.types.VARCHAR(50)),
    sa.Column('user_ts', sa.types.TIMESTAMP),
    sa.Column('reading', JSONB))
"""Defines the table that data will be inserted into"""

class SensorValues(aiocoap.resource.Resource):
    """CoAP handler for coap://readings URI"""
    def __init__(self):
        super(SensorValues, self).__init__()

    def register_handlers(self, resource_root):
        """Registers other/sensor_values URI"""
        resource_root.add_resource(('other', 'sensor-values'), self)
        return

    async def render_post(self, request):
        """Sends asset readings to storage layer
        Input payload looks like:
        {
            "timestamp": "2017-01-02T01:02:03.23232Z-05:00",
            "asset": "pump1",
            "readings": {
                "velocity": "500",
                "temperature": {
                    "value": "32",
                    "unit": "kelvin"
                }
            }
        }
        """

        # TODO: The format is documented at https://docs.google.com/document/d/1rJXlOqCGomPKEKx2ReoofZTXQt9dtDiW_BHU7FYsj-k/edit#
        # and will be moved to a .rst file

        # TODO: Validate request.payload
        original_payload = loads(request.payload)
        
        payload = dict(original_payload)

        key = payload.get('key')

        if key:
            del payload['key']

        # Comment out to demonstrate IntegrityError
        # key = '123e4567-e89b-12d3-a456-426655440000'

        asset = payload.get('asset')

        if asset is not None:
            del payload['asset']

        timestamp = payload.get('timestamp')

        readings = payload.get('readings', {})

        if timestamp:
            del payload['timestamp']

        try:
            async with aiopg.sa.create_engine("postgresql://foglamp:foglamp@localhost:5432/foglamp") as engine:
                async with engine.acquire() as conn:
                    await conn.execute(_sensor_values_tbl.insert().values(
                        asset_code=asset, reading=readings, read_key=key, user_ts=timestamp))
        except psycopg2.IntegrityError:
            logging.getLogger('coap-server').exception(
                "Duplicate key (%s) inserting sensor values: %s"
                , key # Maybe the generated key is the problem
                , original_payload)

        # TODO what should this return?
        return aiocoap.Message(payload=''.encode("utf-8"))

