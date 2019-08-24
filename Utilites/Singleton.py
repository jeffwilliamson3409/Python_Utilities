class Singleton:

    # Class property that stores instance state to insure  that the class is a singleton
    __instance = None

    def __init__(self, x):

        # Insures that the class is a singleton
        if Singleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self

        # Carry on like a regular class
        self.x = x

    def __call__(self):
        return self.x


p = Singleton(4)()
print(p)

q = Singleton(5)()
print(q)