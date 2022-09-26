import os
import json
import aiohttp
from sandbox_api import ASandbox
from typing import Optional, BinaryIO, Union
from sandbox_api.exceptions import status_exceptions

class ASandBox2(ASandbox):
    
    def __init__(self, url: str, total: Optional[float] = 60, connect: Optional[float] = None,
                sock_connect: Optional[float] = None, sock_read: Optional[float] = None):
        super().__init__(url, total, connect, sock_connect, sock_read)
    
    async def runner(self, config: Union[dict], loader: Union[dict], environ: Optional[BinaryIO] = None) -> dict:
        data = aiohttp.FormData()
        data.add_field("config", json.dumps(config))
        data.add_field("loader", json.dumps(loader))
        if environ is not None:
            data.add_field("environment", environ)
        
        
        async with self.session.post(os.path.join(self.url, "runner/"), data=data) as response:
            
            if response.status != 200:
                raise status_exceptions(response)

            return await response.json()