/*
 * Fledge storage service.
 *
 * Copyright (c) 2017 OSisoft, LLC
 *
 * Released under the Apache 2.0 Licence
 *
 * Author: Mark Riddoch
 */
#include <management_api.h>
#include <config_handler.h>
#include <rapidjson/document.h>
#include <logger.h>
#include <time.h>
#include <sstream>


//# FIXME_I:
#include <tmp_log.hpp>


using namespace std;
using namespace rapidjson;
using HttpServer = SimpleWeb::Server<SimpleWeb::HTTP>;

ManagementApi *ManagementApi::m_instance = 0;

/**
 * Wrapper for ping method
 */
void pingWrapper(shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request)
{
        ManagementApi *api = ManagementApi::getInstance();
        api->ping(response, request);
}

/**
 * Wrapper for shutdown method
 */
void shutdownWrapper(shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request)
{
        ManagementApi *api = ManagementApi::getInstance();
        api->shutdown(response, request);
}

/**
 * Wrapper for config change method
 */
void configChangeWrapper(shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request)
{
        ManagementApi *api = ManagementApi::getInstance();
        api->configChange(response, request);
}

// FIXME_I:
void configChangeChildWrapper(shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request)
{
        ManagementApi *api = ManagementApi::getInstance();
        api->configChangeChild(response, request);
}

/**
 * Construct a microservices management API manager class
 */
ManagementApi::ManagementApi(const string& name, const unsigned short port) : m_name(name)
{
	m_server = new HttpServer();
	m_logger = Logger::getLogger();
	m_server->config.port = port;
	m_startTime = time(0);
	m_statsProvider = 0;
	m_server->resource[PING]["GET"] = pingWrapper;
	m_server->resource[SERVICE_SHUTDOWN]["POST"] = shutdownWrapper;
	m_server->resource[CONFIG_CHANGE]["POST"] = configChangeWrapper;
	m_server->resource[CONFIG_CHANGE_CHILD]["POST"] = configChangeChildWrapper;

	m_instance = this;

	m_logger->info("Starting management api on port %d.", port);
}

/**
 * Start HTTP server for management API
 */
static void startService()
{
        ManagementApi::getInstance()->startServer();
}

void ManagementApi::start() {
        m_thread = new thread(startService);
}

void ManagementApi::startServer() {
	m_server->start();
}

void ManagementApi::stop()
{
	this->stopServer();
}

void ManagementApi::stopServer()
{
	m_server->stop();
	m_thread->join();
}

/**
 * Return the signleton instance of the management interface
 *
 * Note if one has not been explicitly created then this will
 * return 0.
 */
ManagementApi *ManagementApi::getInstance()
{
	return m_instance;
}

/**
 * Management API destructor
 */
ManagementApi::~ManagementApi()
{
	delete m_server;
	delete m_thread;
}

/**
 * Register a statistics provider
 */
void ManagementApi::registerStats(JSONProvider *statsProvider)
{
	m_statsProvider = statsProvider;
}

/**
 * Received a ping request, construct a reply and return to caller
 */
void ManagementApi::ping(shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request)
{
ostringstream convert;
string responsePayload;

	(void)request;	// Unsused argument
	convert << "{ \"uptime\" : " << time(0) - m_startTime << ",";
	convert << "\"name\" : \"" << m_name << "\"";
	if (m_statsProvider)
	{
		string stats;
		m_statsProvider->asJSON(stats);
		convert << ", \"statistics\" : " << stats;
	}
	convert << " }";
	responsePayload = convert.str();
	respond(response, responsePayload);
}

/**
 * Received a shutdown request, construct a reply and return to caller
 */
void ManagementApi::shutdown(shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request)
{
ostringstream convert;
string responsePayload;

	(void)request;	// Unsused argument
	m_serviceHandler->shutdown();
	convert << "{ \"message\" : \"Shutdown in progress\" }";
	responsePayload = convert.str();
	respond(response, responsePayload);
}

/**
 * Received a config change request, construct a reply and return to caller
 */
void ManagementApi::configChange(shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request)
{
ostringstream convert;
string responsePayload;
string	category, items, payload;

	payload = request->content.string();
	ConfigCategoryChange	conf(payload);
	ConfigHandler	*handler = ConfigHandler::getInstance(NULL);
	handler->configChange(conf.getName(), conf.itemsToJSON(true));
	convert << "{ \"message\" ; \"Config change accepted\" }";
	responsePayload = convert.str();
	respond(response, responsePayload);
}

// FIXME_I:
void ManagementApi::configChangeChild(shared_ptr<HttpServer::Response> response, shared_ptr<HttpServer::Request> request)
{
ostringstream convert;
string responsePayload;
string	category, items, payload, parent_category;

	payload = request->content.string();


	// FIXME_I:
	string _section="xxx21 ";
	Logger::getLogger()->setMinLevel("debug");
	//Logger::getLogger()->debug("%s / %s - S1 category :%s: config :%s:", _section.c_str(), __FUNCTION__, category.c_str(), config.c_str());
	Logger::getLogger()->debug("%s / %s - S1  payload:%s: ", _section.c_str(), __FUNCTION__, payload.c_str());
	Logger::getLogger()->setMinLevel("warning");


//# FIXME_I:
char tmp_buffer[500000];
snprintf (tmp_buffer,500000, "%s / %s : payload |%s|"
	,_section.c_str()
    ,__FUNCTION__
    ,payload.c_str()
    );
tmpLogger (tmp_buffer);



	ConfigCategoryChange	conf(payload);
	ConfigHandler	*handler = ConfigHandler::getInstance(NULL);
	// FIXME_I:
	//parent_category= "TooHot1";
	parent_category = conf.getmParentName();
	category = conf.getName();
	items = conf.itemsToJSON(true);

	//FIXME_I:
	Logger::getLogger()->setMinLevel("debug");
	//Logger::getLogger()->debug("%s / %s - S1 category :%s: config :%s:", _section.c_str(), __FUNCTION__, category.c_str(), config.c_str());
	Logger::getLogger()->debug("%s / %s - S1.1  parent_category:%s: category:%s: items:%s: ", _section.c_str(), __FUNCTION__
							   , parent_category.c_str()
							   , category.c_str()
							   , items.c_str()
							   );
	Logger::getLogger()->setMinLevel("warning");


	handler->configChangeChild(parent_category, conf.getName(), conf.itemsToJSON(true));
	convert << "{ \"message\" ; \"Config child change accepted\" }";
	responsePayload = convert.str();
	respond(response, responsePayload);
}


/**
 * HTTP response method
 */
void ManagementApi::respond(shared_ptr<HttpServer::Response> response, const string& payload)
{
        *response << "HTTP/1.1 200 OK\r\nContent-Length: " << payload.length() << "\r\n"
                 <<  "Content-type: application/json\r\n\r\n" << payload;
}
