import json
from types import SimpleNamespace

from pythonmiscscripts.opts.user_opts import UserOpts
from pythonmiscscripts.os_io.system_data import SystemData


class InstallData(object):
    def __init__(self, opts: UserOpts, system_data: SystemData):
        self.user_opts = opts
        self.system_data = system_data

    @staticmethod
    def default():
        opts = UserOpts.default_opts()
        system_data = SystemData(opts.user_name)
        return InstallData(opts, system_data)

    def to_json(self) -> str:
        return json.dumps(self, default=nested_handler)

    def as_dict(self):
        return self.__dict__

    @staticmethod
    def from_json(j: str):
        return json.loads(j, object_hook=lambda d: SimpleNamespace(**d))

    def __repr__(self) -> str:
        return str(self.__dict__)


def nested_handler(obj):
    if hasattr(obj, 'as_dict'):
        return obj.as_dict()
    raise TypeError("Cant parse obj=%s" % obj)


if __name__ == "__main__":
    data = InstallData.default()
    print(data.to_json())
    parsed = InstallData.from_json(data.to_json())
    print(parsed)
    pass
