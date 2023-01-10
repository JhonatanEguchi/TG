#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink


class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 2 routers in two different subnets
        r = []
        for i in range(0,7):
          r.append(self.addHost('r'+str(i+1), cls=LinuxRouter,
                          ip='10.'+str(i)+'.0.1/24',))

        d1 = self.addHost(name='d1',
                          ip='10.0.0.100/24',
                          defaultRoute = 'via 10.0.0.1')

        self.addLink(d1, 
                    r[0],
                    intfName2='r1-eth1',
                    params2={'ip': '10.0.0.1/24'})

        linkopts = dict(bw = 100, delay = '1ms', loss = 0, use_thb = True)

        self.addLink(r[0],
                     r[1],
                     intfName1='r1-eth2',
                     intfName2='r2-eth2',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'},)

        self.addLink(r[0],
                     r[1],
                     intfName1='r1-eth0',
                     intfName2='r2-eth0',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'},
                     **linkopts)
        # Add 2 switches
        # s1 = self.addSwitch('s1')
        # s2 = self.addSwitch('s2')

        # Add host-switch links in the same subnet
        # self.addLink(s1,
        #              r1,
        #              intfName2='r1-eth1',
        #              params2={'ip': '10.0.0.1/24'})

        # self.addLink(s2,
        #              r2,
        #              intfName2='r2-eth1',
        #              params2={'ip': '10.1.0.1/24'})

        # Add router-router link in a new subnet for the router-router connection

        # Adding hosts specifying the default route
        d = []
        
        linkoptsClient = dict(bw = 15, delay = '0ms', loss = 0, use_thb = True)

        for i in range(0,5):
            d.append(self.addHost(name=('c' + str(i+1)),
                            ip='10.'+str(i+2)+'.0.100/24',
                            defaultRoute = 'via 10.'+str(i+2)+'.0.1'))
            if(i == 0):
                self.addLink(d[i], 
                        r[i+2],
                        intfName2='r'+str(i+3)+'-eth1',
                        params2={'ip': '10.'+str(i+2)+'.0.1/24'})
            else:
                self.addLink(d[i], 
                        r[i+2],
                        intfName2='r'+str(i+3)+'-eth1',
                        params2={'ip': '10.'+str(i+2)+'.0.1/24'})
            self.addLink(r[i+2],
                       r[1],
                       intfName1='r'+str(i+3)+'-eth2',
                       intfName2='r2-eth'+str(i+3),
                       params1={'ip': '10.'+str(101+i)+'.0.1/24'},
                       params2={'ip': '10.'+str(101+i)+'.0.2/24'})
        

        # Add host-switch links


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo, link = TCLink)

    # Add routing for reaching networks that aren't directly connected
    info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.101.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.102.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.103.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.104.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.105.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.3.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.4.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.5.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r1'].cmd("ip route add 10.6.0.0/24 via 10.100.0.2 dev r1-eth0"))
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev r2-eth0"))
    info(net['r2'].cmd("ip route add 10.2.0.0/24 via 10.101.0.1 dev r2-eth3"))
    info(net['r2'].cmd("ip route add 10.3.0.0/24 via 10.102.0.1 dev r2-eth4"))
    info(net['r2'].cmd("ip route add 10.4.0.0/24 via 10.103.0.1 dev r2-eth5"))
    info(net['r2'].cmd("ip route add 10.5.0.0/24 via 10.104.0.1 dev r2-eth6"))
    info(net['r2'].cmd("ip route add 10.6.0.0/24 via 10.105.0.1 dev r2-eth7"))
    info(net['r3'].cmd("ip route add 10.1.0.0/24 via 10.101.0.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.0.0.0/24 via 10.101.0.2 dev r3-eth2"))
    info(net['r3'].cmd("ip route add 10.100.0.0/24 via 10.101.0.2 dev r3-eth2"))
    info(net['r4'].cmd("ip route add 10.1.0.0/24 via 10.102.0.2 dev r4-eth2"))
    info(net['r4'].cmd("ip route add 10.0.0.0/24 via 10.102.0.2 dev r4-eth2"))
    info(net['r4'].cmd("ip route add 10.100.0.0/24 via 10.102.0.2 dev r4-eth2"))
    info(net['r5'].cmd("ip route add 10.1.0.0/24 via 10.103.0.2 dev r5-eth2"))
    info(net['r5'].cmd("ip route add 10.0.0.0/24 via 10.103.0.2 dev r5-eth2"))
    info(net['r5'].cmd("ip route add 10.100.0.0/24 via 10.103.0.2 dev r5-eth2"))
    info(net['r6'].cmd("ip route add 10.1.0.0/24 via 10.104.0.2 dev r6-eth2"))
    info(net['r6'].cmd("ip route add 10.0.0.0/24 via 10.104.0.2 dev r6-eth2"))
    info(net['r6'].cmd("ip route add 10.100.0.0/24 via 10.104.0.2 dev r6-eth2"))
    info(net['r7'].cmd("ip route add 10.1.0.0/24 via 10.105.0.2 dev r7-eth2"))
    info(net['r7'].cmd("ip route add 10.0.0.0/24 via 10.105.0.2 dev r7-eth2"))
    info(net['r7'].cmd("ip route add 10.100.0.0/24 via 10.105.0.2 dev r7-eth2"))
    #info(net['d1'].cmd("cd"))
    #info(net['d1'].cmd("cd ../../../FlowerTest/quickstart_pytorch/"))
    #info(net['d1'].cmd('../../../.local/share/pypoetry/venv/bin/poetry run python3 server.py'))
    #info(net['c1'].cmd("cd"))
    #info(net['c1'].cmd("cd ../../../FlowerTest/quickstart_pytorch/"))
    #info(net['c1'].cmd("../../../.local/share/pypoetry/venv/bin/poetry run python3 client.py &"))
    #info(net['c2'].cmd("cd"))
    #info(net['c2'].cmd("cd ../../../FlowerTest/quickstart_pytorch/"))
    #info(net['c2'].cmd("../../../.local/share/pypoetry/venv/bin/poetry run python3 client.py &"))
    #info(net['c3'].cmd("cd"))
    #info(net['c3'].cmd("cd Área\ de\ Trabalho/FlowerTest/quickstart_pytorch/"))
    #info(net['c3'].cmd('script -c "echo a" saida5.txt &'))
    c1_pcap = net['c1'].popen('tcpdump -w c1_dump.pcap')
    c2_pcap = net['c2'].popen('tcpdump -w c2_dump.pcap')
    d1_pcap = net['d1'].popen('tcpdump -w d1_dump.pcap')


	
    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
