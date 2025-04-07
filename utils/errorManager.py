from attrs import define

@define(kw_only=True)
class Error:
    title: str
    msg: str