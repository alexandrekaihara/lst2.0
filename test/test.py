from host import Host
from switch import Switch
from controller import Controller

h1 = Host("h1")
h1.instantiate()
h2 = Host("h2")
h2.instantiate()
s1 = Switch("s1")
s1.instantiate()
c1 = Controller("c1")
c1. instantiate()

c1.connect(s1)
c1.setIp("192.168.200.3", 24, s1)
c1.initController('192.168.200.3', 100)

h1.connect(s1)
s1.setIp('192.168.200.1', 24, h1)
s1.connectToInternet('192.168.200.4',24)
s1.setController('192.168.200.3', 100)
h1.setIp('192.168.200.2', 24, s1)
h1._Node__addRoute('192.168.100.0', 24, s1)
h1.setDefaultGateway('192.168.200.4', s1)

h2.connect(s1)
h2.setIp('192.168.100.1', 24, s1)
h2._Node__addRoute('192.168.200.0', 24, s1)
h2.setDefaultGateway('192.168.200.4', s1)
s1.setIp('192.168.100.2', 24, h2)


s1.delete()
h1.delete()
h2.delete()
c1.delete()




Host(0) -> Connect -> Switch(0) -> Switch adc port -> Host definir gateway
Host(0) -> Connect -> Switch(+1) -> Swith adc port -> Host definir gateway
Host(+1) -> Connect -> Switch(+1) -> Swith adc port -> Host definir gateway
Switch(0) -> Connect -> Switch(0) -> Switch adc port -> Switch adc port 
Switch(0) -> Connect -> Switch(+1) -> Switch adc port -> Switch adc port -> Switch adc rota -> Propagar rota
Switch(+1) -> Connect -> Switch(+1)
Switch(0) -> Connect -> Host(0) -> Switch adc port
Switch(0) -> Connect -> Host(+1) -> Swith Ad
Switch(+1) -> Connect -> Host(+1) -> 



c1 = Controller("c1")
c2 = Controller("c2")

h1 = Host("h1")
h1.instantiate()
h2 = Host("h2")
h2.instantiate()
h3 = Host("h3")
h3.instantiate()
h4 = Host("h4")
h4.instantiate()
h5 = Host("h5")
h5.instantiate()

s1 = Switch("s1")
s1.instantiate()
ls1 = Link(c1, s1)
ls1.setIp("192.168.100.100", 32)

s2 = Switch("s2")
s2.instantiate()

# Server subnet
l1 = Link(s1, h1)
l1.setIp(h1, "192.168.100.2", 24)
l1.setIp(s1, "192.168.100.1", 24)

l2 = Link(s1, h2)
l2.setIp(h2, "192.168.200.2", 24)
l1.setIp(s1, "192.168.200.1", 24)

l3 = Link(s1, h3)
l3.setIp(h3, "192.168.210.2", 24)
l3.setIp(s1, "192.168.210.1", 24)

l4 = Link(s1, h4)
l4.setIp(h4, "192.168.220.2", 24)
l4.setIp(s1, "192.168.220.1", 24)

l5 = Link(s1,s2)

l6 = Link(s2, h5)
l6.setIp(h5, "192.168.50.2", 24)
l6.setIp(s2, "192.168.50.1", 24)
