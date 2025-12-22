from dotenv import load_dotenv
import os
load_dotenv()
from Controller.comms import publisher, tunnel
import pinggy

class MyTunnelHandler(pinggy.BaseTunnelHandler):
    def disconnected(self, msg):
        print("❌ Tunnel closed")
        initialize()

def initialize() -> bool:
    try:
        pinggyToken = os.getenv("PINGGY_TOKEN")
        if pinggyToken == None:
            return False
        else:
            tunnelUrl = tunnel.Tunnel.CreateTunnel(pinggyToken,MyTunnelHandler)
        githubToken = os.getenv("GITHUB_TOKEN")
        if githubToken != None:
            if tunnelUrl!=None:
                publisher.publish(githubToken,publisher.DomainEndPoint(url=tunnelUrl,active=True))
        return True
    except Exception as e:
        print(e)
        return False