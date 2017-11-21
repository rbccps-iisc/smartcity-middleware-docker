from graphviz import Digraph


def create_graph(instances):
    """ Creates a graph of the architecture using graphviz software. Requires graphviz to be installed on the system.
    Site: www.graphviz.org
    Args:
        instances (dict): instances is a dict of the form { 'server' : [IPAddress, Port]}.
    """
    main = Digraph(node_attr={'shape': 'record'}, edge_attr={'minlen': '1'})

    main.node('Individual_User', 'User\\n(HTTPS client with APIKEY)')
    main.node('Devices', 'Devices/Apps\\n(HTTPS client with APIKEY)')
    main.node('Public', 'Public')

    main.edge('Public', 'PublicCatalogue', label="read only")
    main.edge('Individual_User',
              'Firewall',
              _attributes={'xlabel': "APIs to search and manage devices/apps\\n(secure tunnel)"})
    main.edge('Devices', 'Firewall', label="APIs to produce/consume data\\n(secure tunnel)")
    main.body.append('{rankdir=LR;Public, Individual_User, Devices}')

    group = Digraph('cluster_0', graph_attr={'shape': 'record', 'label': '[ Middleware ]', 'color': 'blue'})

    group.node('Persistence',
               '{Persistence|Elasticsearch' +
               ' | {0}:{1}'.format(instances["elasticsearch"][0], instances["elasticsearch"][1]) +
               '}')
    group.node('Broker', '{Broker|RabbitMQ' +
               ' | {0}:{1}'.format(instances["rabbitmq"][0], instances["rabbitmq"][1]) +
               '}')
    group.node('LDAP',
               '{Authentication and\\nauthorization (AA) server|ldapd' +
               ' | {0}:{1}'.format(instances["ldapd"][0], instances["ldapd"][1]) +
               '}',
               _attributes={'color': 'red'})
    group.node('CA',
               '{Certificate\\nAuthority (CA)|OpenSSL' +
               ' | {0}:{1}'.format(instances["certificate_authority"][0], instances["certificate_authority"][1]) +
               '}',
               _attributes={'color': 'red'})
    group.node('PublicCatalogue',
               '{Publicly available\\nopen catalogue' +
               ' | {0}:{1}'.format(instances["hypercat"][0], instances["hypercat"][1]) +
               '}')
    group.node('Firewall',
               '{API gateway + Firewall cluster \\n (Certificates signed by the CA) | kong + iptables' +
               ' | {0}:{1}'.format(instances["kong"][0], instances["kong"][1]) +
               '}',
               _attributes={'style': 'bold'})
    group.node('HistoryAnalytics',
               '{Historical data \\n analytics engine|Apache storm' +
               ' | {0}:{1}'.format(instances["apache_storm"][0], instances["apache_storm"][1]) +
               '}',
               _attributes={'color': 'darkgreen'})
    group.node('StreamAnalytics', '{Stream analytics \\n engine|Apache storm}',
               _attributes={'color': 'darkgreen'})
    group.node('apt_repo', '{APT Repository|Aptly' +
               ' | {0}:{1}'.format(instances["apt_repo"][0], instances["apt_repo"][1]) +
               '}',
               _attributes={'color': 'darkgreen'})
    group.node('DNS', '{DNS\\n(with security extensions)|BIND' +
               ' | {0}:{1}'.format(instances["bind"][0], instances["bind"][1]) +
               '}',
               _attributes={'color': 'darkgreen'})
    group.node('NTP', '{NTP server|OpenNTPD' +
               ' | {0}:{1}'.format(instances["openntpd"][0], instances["openntpd"][1]) +
               '}',
               _attributes={'color': 'darkgreen'})
    group.node('PolicyEnforcer', '{Security policy\\nenforcer and accounting|Custom scripts}',
               _attributes={'color': 'red'})
    group.node('Catalogue', '{Internal Catalogue}')
    group.node('Validation', '{Validation\\nserver|Apache storm}')
    group.node('point', _attributes={'shape': 'point'})

    group.edge('Broker', 'point', _attributes={'arrowhead': "none", 'style': 'dashed'})
    group.edge('Persistence', 'point', _attributes={'arrowhead': "none", 'style': 'dashed'})
    group.edge('Catalogue', 'point', _attributes={'arrowhead': "none", 'style': 'dashed'})
    group.edge('point', 'LDAP', _attributes={'style': 'dashed'})
    group.edge('Firewall', 'Validation', _attributes={'arrowhead': "none"})
    group.edge('Validation', 'Broker')
    group.edge('Broker', 'StreamAnalytics', _attributes={'style': "dashed"})
    group.edge('Validation', 'Persistence')
    group.edge('Validation', 'Catalogue')
    group.edge('Persistence', 'HistoryAnalytics', _attributes={'style': "dashed"})
    group.edge('CA', 'Firewall', label="Certificates", _attributes={'style': "dashed"})
    group.body.append("{rank=same; CA;PolicyEnforcer;PublicCatalogue}")
    group.body.append('{rank=same; DNS;LDAP;NTP}')
    group.body.append('{rank=same;HistoryAnalytics;StreamAnalytics}')
    main.subgraph(group)
    main.render(view=True)
