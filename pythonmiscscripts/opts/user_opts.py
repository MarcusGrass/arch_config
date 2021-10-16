from pythonmiscscripts.input_utils.parse_input import request_str, confirm


class UserOpts(object):
    def __init__(self, host_name: str, user_name: str, git_user: str, email: str, xmonad: bool, programming: bool,
                 nvidia: bool, yay: bool):
        self.host_name = host_name
        self.user_name = user_name
        self.git_user = git_user
        self.email = email
        self.xmonad = xmonad
        self.programming = programming
        self.nvidia = nvidia
        self.yay = yay

    @staticmethod
    def from_dict(**kwargs):
        opts = UserOpts.default_opts()
        for key, value in kwargs.items():
            opts.__setattr__(key, value)
        return opts

    @staticmethod
    def default_opts():
        return UserOpts("grarch", "gramar", "MarcusGrass", "marcus.grass@gmail.com", True, True, False, True)

    @staticmethod
    def prompt_for_opts(depth: int):
        opts = UserOpts.default_opts()
        if not confirm(depth, "Use default user [%s]? " % opts.user_name):
            opts.user_name = request_str(depth, "Enter username: ")
        if not confirm(depth, "Use default host name [%s]? " % opts.host_name):
            opts.host_name = request_str(depth, "Enter host name: ")
        if not confirm(depth, "Use default git user [%s]? " % opts.git_user):
            opts.host_name = request_str(depth, "Enter git user: ")
        if not confirm(depth, "Use default email [%s]? " % opts.email):
            opts.email = request_str(depth, "Enter email: ")
        opts.xmonad = confirm(depth, "With xmonad? ")
        opts.programming = confirm(depth, "With programming deps? ")
        opts.nvidia = confirm(depth, "Using nvidia graphics? ")
        opts.yay = confirm(depth, "Install Yay? ")
        return opts

    def as_dict(self):
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.__dict__)


if __name__ == "__main__":
    print(UserOpts.prompt_for_opts(0))
