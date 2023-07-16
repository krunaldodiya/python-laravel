class Parent:
    def get(self):
        print("test", self.test)


class Child(Parent):
    def __init__(self) -> None:
        super().__init__()

        self.test = "test"


child = Child()

child.get()
