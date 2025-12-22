from dotenv import load_dotenv
import os
load_dotenv()
from Controller.comms import publisher, tunnel
import pinggy

class MyTunnelHandler(pinggy.BaseTunnelHandler):
    def on_tunnel_ready(self, url):
        print(f"🚀 Public URL is live: {url}")

    def on_connection(self, remote_addr):
        print(f"🌐 New visitor from: {remote_addr}")

    def on_error(self, error):
        print(f"❌ Tunnel error: {error}")
    def on_tunnel_closed(self):
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