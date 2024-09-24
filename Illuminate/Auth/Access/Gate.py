from Illuminate.Contracts.Auth.Access.Gate import Gate as GateContract


class Gate(GateContract):
    def __init__(self) -> None:
        pass

    def define(self):
        print("hello from gate")
