class Fetcher:
    def __init__(self, project):
        self.project = project

    def get_users(self):
        command = 'echo "[$(sacctmgr -np show association where account=p904-24-3 | cut -f3 -d\| | awk \'NF\' | awk \'{printf \\"\\\"%s\\\", \\", $0}\' | sed \'s/, $//\')]"'