from .traces import trace_requirements


@trace_requirements("Req67")
class CouaException(Exception):
    pass
