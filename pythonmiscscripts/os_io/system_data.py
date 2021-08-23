import multiprocessing


class SystemData(object):
    def __init__(self, user: str):
        self.num_cpus = multiprocessing.cpu_count()
        self.home = "/home/%s" % user

    def append_to_base(self, dirs: str):
        if dirs.startswith("/"):
            return self.home + dirs
        raise ValueError("Supplied directory doesn't start with a slash")

    def append_to_config_location(self, dirs: str):
        if dirs.startswith("/"):
            return self.append_to_base("/code/arch_config") + dirs
        raise ValueError("Supplied directory doesn't start with a slash")

    def as_dict(self):
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.__dict__)


if __name__ == "__main__":
    data = SystemData("gramar")
    print(data.append_to_base("/.ssh"))
    print(data.append_to_config_location("/.xmonad"))
