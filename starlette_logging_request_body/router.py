import json
from datetime import datetime
from typing import Callable, Optional
import logging
from fastapi import Request, Response
from fastapi.routing import APIRoute


def reformat_body(body: bin, obfuscate: bool = False):
    """
    Decodes the binary body into something more useful for logging.

    - body - the binary body object from the request or response
    - obfuscate (default=False) - will obfuscate all the values in the key-value pairs in the body data.
    """
    if body:
        try:
            # Try to parse as a JSON object and return as a Dict (obfuscated if required)
            data = json.loads(body.decode())
            if obfuscate:
                data = {k: "***" for k, v in data.items()}
            return data
        except:
            # Obfuscate if a body exits and is not JSON
            if obfuscate:
                return "***"
            else:
                return body.decode()
    else:
        return None


class BaseContextRoute(APIRoute):
    """
    A router that will log request and response information.

    Note that it will only log successful requests.

    Inspiration taken from Yagiz's solution
    - https://stackoverflow.com/questions/64115628/get-starlette-request-body-in-the-middleware-context

    Usage example:

    router = APIRouter(route_class=LogContextRout)

    @router.post("/endpoint")
    async def my_endpoint(body: List[str] = Body(...)):
        ...

    To adjust parameterisation, subclass this and change the parameters.
    """

    obfuscate_request_body = False
    obfuscate_response_body = False

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            start = datetime.utcnow()

            response: Response = await original_route_handler(request)

            # Decode the request and response body so we can push to the logging
            request_content = reformat_body(
                await request.body(), obfuscate=self.obfuscate_request_body
            )
            response_content = reformat_body(
                response.body, obfuscate=self.obfuscate_response_body
            )

            log_data = {
                "utc": str(start),
                "duration": (datetime.utcnow() - start).total_seconds(),
                "ip": request.client.host,
                "request": {
                    "method": request.method,
                    "hostname": request.url.hostname,
                    "path": request.url.path,
                    "querystring": request.url.query,
                    "body": request_content,
                },
                "response": {
                    "status": response.status_code,
                    "body": response_content,
                },
            }
            self.push_log(log_data)

            return response

        return custom_route_handler

    def push_log(self, log_data: dict):
        """
        Method to push the log to wherever you wish.
        This by default prints to the console.
        Overwrite this method to push the log to where you wish it to go.
        """
        print(log_data)


class LogContextRoute(BaseContextRoute):
    """This ContextRoute class pushes the log data to a logger."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._logger = logging.getLogger(__name__)
        self._logger.addHandler(logging.NullHandler())

    def push_log(self, log_data: dict):
        self._logger.info(log_data)


class ObfuscatedRequestContextRoute(BaseContextRoute):
    """This ContextRoute obfuscates the request object only."""

    obfuscate_request_body = True
