This server is implementing the Orion ContextBroker GE, providing data to the Cosmos instance at 
cosmos.lab.fiware.org using the cygnus plugin.

At the moment the security implementation is assure by the PEP Proxy located at 

	https://github.com/ging/fi-ware-pep-proxy

This instance of the PEP Proxy is redirecting all the trafic from the port 1026(PEP)  to the port 10026(ORION)


-------------------------------------------------------------------------------------------------

#Config files are located at 

RUSH SERVER
/opt/rush/lib/config.js

ORION
/etc/sysconfig/contextBroker

CYGNUS
/etc/cygnus/conf/agent_test.conf
/etc/cygnus/conf/cygnus_instance_test.conf

PEPPROXY
/opt/pep-proxy/config.js


-------------------------------------------------------------------------------------------------

Comands to start the diferent services

sudo service redis-server start/stop/restart  # RUSH SERVER
sudo service contextBroker start/stop/restart # ORION SERVER
sudo service mongod start/stop/restart        # DATABASE SERVER
sudo service cygnus start/stop/restart        # CYGNUS SERVER
sudo /opt/pep-proxy/node server               # PEPPROXY SERVER (manual mode)

To start the Pep-Proxy and the Rush Consumer and Listner 

# To list forever services

sudo forever list

# To start the services using forever
cd /opt/pep-proxy/ && sudo forever start server.js
cd /opt/rush/bin/ && sudo forever start consumer
cd /opt/rush/bin/ && sudo forever start listener


-------------------------------------------------------------------------------------------------

LOG Files

tail -f /var/log/contextBroker/contextBroker.log
