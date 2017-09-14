# -*- coding: utf-8 -*-

# FOGLAMP_BEGIN
# See: http://foglamp.readthedocs.io/
# FOGLAMP_END
import random
import time
import json

import asyncpg
import http.client
import pytest
import asyncio
import uuid
from datetime import datetime, timezone, timedelta

__author__ = "Vaibhav Singhal"
__copyright__ = "Copyright (c) 2017 OSIsoft, LLC"
__license__ = "Apache 2.0"
__version__ = "${VERSION}"

# Module attributes
__DB_NAME = "foglamp"
BASE_URL = 'localhost:8082'
headers = {"Content-Type": 'application/json'}

test_data_asset_code = 'TESTAPI'

pytestmark = pytest.mark.asyncio


async def add_master_data(rows=0):
    conn = await asyncpg.connect(database=__DB_NAME)
    await conn.execute('''DELETE from foglamp.readings WHERE asset_code IN ($1)''', test_data_asset_code)
    uid_list = []
    x_list = []
    y_list = []
    for i in range(rows):
        uid = uuid.uuid4()
        uid_list.append(uid)
        x = random.randint(1, 100)
        y = random.uniform(1.0, 100.0)
        x_list.append(x)
        y_list.append(y)
        await conn.execute("""INSERT INTO foglamp.readings(asset_code,read_key,reading,user_ts) VALUES($1, $2, $3, $4);""",
                           test_data_asset_code, uid,
                           json.dumps({'x': x, 'y': y}), datetime.now(tz=timezone.utc) - timedelta(minutes = 10))
    await conn.close()
    return uid_list, x_list, y_list


async def delete_master_data():
    conn = await asyncpg.connect(database=__DB_NAME)
    await conn.execute('''DELETE from foglamp.readings WHERE asset_code IN ($1)''', test_data_asset_code)
    await conn.close()

@pytest.allure.feature("api")
@pytest.allure.story("browser-assets")
class TestBrowseAssets:
    test_data_uid_list = []
    test_data_x_val_list = []
    test_data_y_val_list = []
    @classmethod
    def setup_class(cls):
        cls.test_data_uid_list, cls.test_data_x_val_list, cls.test_data_y_val_list = \
            asyncio.get_event_loop().run_until_complete(add_master_data(10))

    @classmethod
    def teardown_class(cls):
        asyncio.get_event_loop().run_until_complete(delete_master_data())
        pass

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    # TODO: Add tests for negative cases. Currently only positive test cases have been added.

    async def test_get_all_assets(self):
        conn = http.client.HTTPConnection(BASE_URL)
        conn.request("GET", '/foglamp/asset')
        r = conn.getresponse()
        assert 200 == r.status
        r = r.read().decode()
        conn.close()
        retval = json.loads(r)
        print(retval)
        print("id list ", self.test_data_uid_list)
        assert test_data_asset_code == retval[0]['asset_code']
        all_items = [elements['asset_code'] for elements in retval]
        assert test_data_asset_code in all_items
        for elements in retval:
            if elements['asset_code'] == test_data_asset_code:
                assert len(self.test_data_uid_list) == elements['count']

    async def test_get_asset_readings(self):
        # Assert that if more than 20 readings, only 20 are returned as the default limit
        # http://localhost:8082/foglamp/asset/TESTAPI
        pass

    async def test_get_asset_readings_q_limit(self):
        pass

    async def test_get_asset_readings_q_min(self):
        pass

    async def test_get_asset_readings_q_hrs(self):
        pass

    async def test_get_asset_readings_q_time(self):
        # http://localhost:8082/foglamp/asset/TESTAPI?minutes=13&hours=1&seconds=3600&limit=1
        pass

    async def test_get_asset_sensor_readings(self):
        # Assert that if more than 20 readings, only 20 are returned as the default limit
        # http://localhost:8082/foglamp/asset/TESTAPI/x
        pass

    async def test_get_asset_sensor_readings_q_limit(self):
        pass

    async def test_get_asset_sensor_readings_q_min(self):
        pass

    async def test_get_asset_sensor_readings_q_hrs(self):
        pass

    async def test_get_asset_sensor_readings_q_time(self):
        pass

    async def test_get_asset_sensor_readings_stats(self):
        # Assert that if more than 20 readings, only 20 are returned as the default limit
        # http://localhost:8082/foglamp/asset/TESTAPI/x/summary
        pass

    async def test_get_asset_sensor_readings_stats_q_limit(self):
        pass

    async def test_get_asset_sensor_readings_stats_q_min(self):
        pass

    async def test_get_asset_sensor_readings_stats_q_hrs(self):
        pass

    async def test_get_asset_sensor_readings_stats_q_time(self):
        pass

    async def test_get_asset_sensor_readings_time_avg(self):
        # Assert that if more than 20 readings, only 20 are returned as the default limit
        # http://localhost:8082/foglamp/asset/TESTAPI/x/series?group=hours
        pass

    async def test_get_asset_sensor_readings_time_avg_q_group(self):
        pass

    async def test_get_asset_sensor_readings_time_avg_q_limit(self):
        pass

    async def test_get_asset_sensor_readings_time_avg_q_min(self):
        pass

    async def test_get_asset_sensor_readings_time_avg_q_hrs(self):
        pass

    async def test_get_asset_sensor_readings_time_avg_q_time(self):
        pass