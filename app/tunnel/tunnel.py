import pinggy
import time

class Tunnel:
    _instance  = None
    @staticmethod
    def CreateTunnel(token:str,port:int|None=8000):
        if Tunnel._instance != None:
            if Tunnel._instance.is_active():
                Tunnel._instance.stop()
            Tunnel._instance=None
            time.sleep(5)
        Tunnel._instance = pinggy.start_tunnel(forwardto=f"localhost:{port}", token=token)
        if Tunnel._instance.is_active():
            return Tunnel._instance.urls[0]