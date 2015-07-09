var config = {};

config.pep_port = 1026;

// Set this var to undefined if you don't want the server to listen on HTTPS
config.https = {
    enabled: false,
    cert_file: 'cert/cert.crt',
    key_file: 'cert/key.key',
    port: 443
};

config.account_host = 'https://account.lab.fiware.org';

config.keystone_host = 'cloud.lab.fiware.org';
config.keystone_port = 4730;

config.app_host = 'localhost';
config.app_port = '10026';

config.username = 'pepProxy';
config.password = 'pepProxy';

// in seconds
config.chache_time = 300;

// if enabled PEP checks permissions with AuthZForce GE. 
// only compatible with oauth2 tokens engine
config.azf = {
    enabled: false,
    host: '130.206.84.5',
    port: 6017,
    path: '/authzforce/domains/d698df7f-ffd4-11e4-a09d-ed06f24e1e78/pdp'
};

// options: oauth2/keystone
config.tokens_engine = 'keystone';
config.magic_key = undefined;
module.exports = config;
