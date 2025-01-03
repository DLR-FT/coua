from coua import trace_requirements


@trace_requirements("Req123", "Re234")
def a():
    pass


@trace_requirements("Re234", "Re5")
class B:
    pass
