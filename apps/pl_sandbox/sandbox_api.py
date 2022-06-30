from typing import BinaryIO, Optional, Union
from sandbox_api import ASandbox
from sandbox_api.exceptions import status_exceptions
import aiohttp
import json
import os

class ASandbox2(ASandbox):
    
    async def assetor(self, config: Union[dict]) -> dict:
        """New assetor."""
        data = aiohttp.FormData()
        data.add_field("config", json.dumps(config))
        
        async with self.session.post(os.path.join(self.url, "assets/"), data=data) as response:
            if response.status != 200:
                raise status_exceptions(response)
            
            return await response.json()