# starlette-logging-request-body

FastAPI / Starlette middleware for logging the request and including request body and the response into a JSON object.

Uses a custom route class to achieve this.  Has options to obfuscate data in the request and response body if necessary.  

This is a bit of a hack as usually we should not access the request or response body data in middleware so this is set up as a custom router, which then rebuilds the Response object before returning it to FastAPI.

Inspiration for this is taken from - https://stackoverflow.com/questions/64115628/get-starlette-request-body-in-the-middleware-context


## Licence

Under MIT licence.

This is not set up currently as a package general release as is for a specific use case, but feel free to use if you find it useful.


## Usage

Copy in the `router.py` file class into your project.  I have not released this as a package on PyPI as it is only for a very narrow use case.

Create a custom route class inheriting from the `BaseContextRoute` class.

For example

```python

    class MyDatabaseContextRoute(BaseContextRouter):
        """
        This will obfuscate just the request body.
        The context will be posted to a database
        """

        obfuscate_request_body = True

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.db = # Setup connection to my database here

        def push_log(self, log_data: dict):

            self.db.write(log_data)  # Or whatever you need to write the log to the database
            
```

Then import is custom router into your API on the routes you want to include for logging.

```python
    from fastapi import APIRouter

    router = APIRouter(route_class=MyDatabaseContextRoute)
    ...

```


## Sample API

See the sample FastAPI in the `sample` folder.  
