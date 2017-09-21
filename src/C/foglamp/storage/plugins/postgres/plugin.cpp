#include <connection_manager.h>
#include <connection.h>
#include <plugin_api.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include "libpq-fe.h"
#include <iostream>
#include <string>

extern "C" {

static PLUGIN_INFORMATION info = {
	"PostgresSQL",            // Name
	"1.0.0",                  // Version
	SP_COMMON|SP_READINGS,    // Flags
	PLUGIN_TYPE_STORAGE,      // Type
	"1.0.0"                   // Interface version
};

PLUGIN_INFORMATION *plugin_info()
{
	return &info;
}

PLUGIN_HANDLE plugin_init()
{
ConnectionManager *manager = ConnectionManager::getInstance();
  
	manager->growPool(5);
	return manager;
}

bool plugin_common_insert(PLUGIN_HANDLE handle, char *table, char *data)
{
ConnectionManager *manager = (ConnectionManager *)handle;
Connection        *connection = manager->allocate();

	std::cout << "Postgres plugin common insert into " << table << " with payload " <<data;
	bool result = connection->insert(std::string(table), std::string(data));
	manager->release(connection);
	return result;
}

const char *plugin_common_retrieve(PLUGIN_HANDLE handle, char *table, char *query)
{
ConnectionManager *manager = (ConnectionManager *)handle;
Connection        *connection = manager->allocate();
std::string results;

	connection->retrieve(std::string(table), std::string(query), results);
	manager->release(connection);
	return strdup(results.c_str());
}

bool plugin_common_update(PLUGIN_HANDLE handle, char *table, char *data)
{
ConnectionManager *manager = (ConnectionManager *)handle;
Connection        *connection = manager->allocate();

	std::cout << "Postgres plugin common update into " << table << " with payload " <<data;
	bool result = connection->update(std::string(table), std::string(data));
	manager->release(connection);
	return result;
}

bool plugin_common_delete(PLUGIN_HANDLE handle, char *table, char *condition)
{
ConnectionManager *manager = (ConnectionManager *)handle;
Connection        *connection = manager->allocate();

	std::cout << "Postgres plugin common delete from " << table << " with payload " <<condition;
	bool result = connection->deleteRows(std::string(table), std::string(condition));
	manager->release(connection);
	return result;
}

bool plugin_reading_append(PLUGIN_HANDLE handle, char *reading)
{
ConnectionManager *manager = (ConnectionManager *)handle;
Connection        *connection = manager->allocate();

	manager->release(connection);
	return false;
}

char *plugin_reading_fetch(PLUGIN_HANDLE handle, unsigned long id, unsigned int blksize)
{
ConnectionManager *manager = (ConnectionManager *)handle;
Connection        *connection = manager->allocate();

	manager->release(connection);
	return NULL;
}

char *plugin_reading_retrieve(PLUGIN_HANDLE handle, char *condition)
{
ConnectionManager *manager = (ConnectionManager *)handle;
Connection        *connection = manager->allocate();
std::string results;

	connection->retrieve(std::string("readings"), std::string(condition), results);
	manager->release(connection);
	return strdup(results.c_str());
	manager->release(connection);
	return NULL;
}

unsigned int plugin_reading_purge(PLUGIN_HANDLE handle, unsigned long age, unsigned int flags, unsigned long sent)
{
ConnectionManager *manager = (ConnectionManager *)handle;
Connection        *connection = manager->allocate();

	manager->release(connection);
	return 0;
}


void plugin_release(PLUGIN_HANDLE handle, char *results)
{
	(void)handle;
	free(results);
}

PLUGIN_ERROR *plugin_last_error(PLUGIN_HANDLE)
{
	return NULL;
}

bool plugin_shutdown(PLUGIN_HANDLE handle)
{
ConnectionManager *manager = (ConnectionManager *)handle;
  
	manager->shutdown();
	return true;
}

};

