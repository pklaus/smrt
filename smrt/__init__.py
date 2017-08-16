
class SmrtPyException(Exception): pass

class ConnectionException(SmrtPyException): pass

class IncompatiblePlatformException(SmrtPyException): pass

#from . import protocol
#from . import operations
#from . import network
#from . import discovery
#from . import smrt
