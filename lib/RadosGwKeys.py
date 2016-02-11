#!/usr/bin/python

class RadosGwKeys:

    def __init__(self, radosGwCo):
        self.radosGwCo = radosGwCo
    
    def createSubUser(self, accountname, subuser, access):
        self.accountname = accountname
        self.subuser = subuser
        self.access = access
        self.radosGwCo.create_subuser(uid=self.accountname,subuser=self.subuser,access=self.access)
    
    def createKey(self, protocol, secretkey):
        self.protocol = protocol
        self.secretkey = secretkey
        self.radosGwCo.create_key(
                uid=self.accountname,
                subuser=self.subuser,
                key_type=self.protocol,
                access_key=self.subuser,
                secret_key=self.secretkey,
                generate_key=None)
        
        # Return value
        tmpdata = list()
        tmpdata.append(self.protocol.upper()) # S3 or Swift
        tmpdata.append(self.access.upper()) # Permissions
        tmpdata.append(self.subuser) # Accesskey
        tmpdata.append(self.secretkey) # Secretkey
        return tmpdata