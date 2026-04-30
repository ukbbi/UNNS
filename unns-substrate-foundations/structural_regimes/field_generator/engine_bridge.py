import subprocess
import json

class StrucPercEngine:
    def __init__(self):
        self.proc = subprocess.Popen(
            ["node", "engine_server.js"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # wait for READY
        while True:
            line = self.proc.stdout.readline().strip()
            if line == "READY":
                break

    def run(self, ladder):
        request = json.dumps({"ladder": ladder.tolist()})
        self.proc.stdin.write(request + "\n")
        self.proc.stdin.flush()

        response = self.proc.stdout.readline()
        return json.loads(response)

engine = StrucPercEngine()

def run_struc_perc(ladder, config):
    return engine.run(ladder)