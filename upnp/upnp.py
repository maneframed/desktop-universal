import socket

class Upnp():
    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    
    def add_port_mapping(self, local_ip):
        SSDP_ADDR = "239.255.255.250"
        SSDP_PORT = 1900
        SSDP_MX = 2
        SSDP_ST = "urn:schemas-upnp-org:device:InternetGatewayDevice:1"

        ssdpRequest = "M-SEARCH * HTTP/1.1\r\n" + \
                        "HOST: %s:%d\r\n" % (SSDP_ADDR, SSDP_PORT) + \
                        "MAN: \"ssdp:discover\"\r\n" + \
                        "MX: %d\r\n" % (SSDP_MX, ) + \
                        "ST: %s\r\n" % (SSDP_ST, ) + "\r\n"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(str.encode(ssdpRequest), (SSDP_ADDR, SSDP_PORT))
        resp = sock.recv(1000)

        import re
        from urllib import parse

        parsed = re.findall(r'(?P<name>.*?): (?P<value>.*?)\r\n', resp.decode('utf-8'))
        # get the location header
        location = list(filter(lambda x: x[0].lower() == "location", parsed))
        # use the urlparse function to create an easy to use object to hold a URL
        router_path = parse.urlparse(location[0][1])

        from urllib.request import urlopen
        from xml.dom.minidom import parseString
        # get the profile xml file and read it into a variable
        directory = urlopen(location[0][1]).read()

        # create a DOM object that represents the `directory` document
        dom = parseString(directory)

        # find all 'serviceType' elements
        service_types = dom.getElementsByTagName('serviceType')

        # iterate over service_types until we get either WANIPConnection
        # (this should also check for WANPPPConnection, which, if I remember correctly
        # exposed a similar SOAP interface on ADSL routers.
        for service in service_types:
            # I'm using the fact that a 'serviceType' element contains a single text node, who's data can
            # be accessed by the 'data' attribute.
            # When I find the right element, I take a step up into its parent and search for 'controlURL'
            if service.childNodes[0].data.find('WANIPConnection') > 0:
                path= str(service.parentNode.getElementsByTagName('controlURL')[0].childNodes[0].data)
                #path = service.parentNode.getElementsByTagName('controlURL')[0].childNodes[0].data)

        from xml.dom.minidom import Document

        doc = Document()

        # create the envelope element and set its attributes
        envelope = doc.createElementNS('', 's:Envelope')
        envelope.setAttribute('xmlns:s', 'http://schemas.xmlsoap.org/soap/envelope/')
        envelope.setAttribute('s:encodingStyle', 'http://schemas.xmlsoap.org/soap/encoding/')

        # create the body element
        body = doc.createElementNS('', 's:Body')

        # create the function element and set its attribute
        fn = doc.createElementNS('', 'u:AddPortMapping')
        fn.setAttribute('xmlns:u', 'urn:schemas-upnp-org:service:WANIPConnection:1')

        # setup the argument element names and values
        # using a list of tuples to preserve order
        arguments = [
            ('NewRemoteHost',''),
            ('NewExternalPort', '43210'),           # specify port on router
            ('NewProtocol', 'TCP'),                 # specify protocol
            ('NewInternalPort', '43210'),           # specify port on internal host
            ('NewInternalClient', local_ip), # specify IP of internal host
            ('NewEnabled', '1'),                    # turn mapping ON
            ('NewPortMappingDescription', 'Test desc'), # add a description
            ('NewLeaseDuration', '0')]              # how long should it be opened?

        # NewEnabled should be 1 by default, but better supply it.
        # NewPortMappingDescription Can be anything you want, even an empty string.
        # NewLeaseDuration can be any integer BUT some UPnP devices don't support it,
        # so set it to 0 for better compatibility.

        # container for created nodes
        argument_list = []

        # iterate over arguments, create nodes, create text nodes,
        # append text nodes to nodes, and finally add the ready product
        # to argument_list
        for k, v in arguments:
            tmp_node = doc.createElement(k)
            tmp_text_node = doc.createTextNode(v)
            tmp_node.appendChild(tmp_text_node)
            argument_list.append(tmp_node)

        # append the prepared argument nodes to the function element
        for arg in argument_list:
            fn.appendChild(arg)

        # append function element to the body element
        body.appendChild(fn)

        # append body element to envelope element
        envelope.appendChild(body)

        # append envelope element to document, making it the root element
        doc.appendChild(envelope)

        # our tree is ready, conver it to a string
        pure_xml = doc.toxml()

        import http.client

        # use the object returned by urlparse.urlparse to get the hostname and port
        print(pure_xml)
        conn = http.client.HTTPConnection(router_path.hostname, router_path.port)

        # use the path of WANIPConnection (or WANPPPConnection) to target that service,
        # insert the xml payload,
        # add two headers to make tell the server what we're sending exactly.
        conn.request('POST',
            path,
            pure_xml,
            {'SOAPAction': '"urn:schemas-upnp-org:service:WANIPConnection:1#AddPortMapping"',
            'Content-Type': 'text/xml'}
        )

        # wait for a response
        resp = conn.getresponse()

        # print the response status
        print(resp.status)

        # print the response body
        print(resp.read())