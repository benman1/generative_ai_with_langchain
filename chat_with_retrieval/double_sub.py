class BaseClass1:
    def __init__(self):
        print('base1 __init__')


class BaseClass2:
    def __init__(self):
        print('base2 __init__')


class Subclass1(BaseClass1, BaseClass2):
    def __init__(self):
        BaseClass1.__init__(self)
        BaseClass2.__init__(self)
        print('subclass1 __init__')

class Parent(object):
    def __init__(self):
        super(Parent, self).__init__()
        print("parent")

class Left(Parent):
    def __init__(self):
        super(Left, self).__init__()
        print("left")

class Right(Parent):
    def __init__(self):
        super(Right, self).__init__()
        print("right")

class Child(Left, Right):
    def __init__(self):
        super(Child, self).__init__()
        print("child")

if __name__ == "__main__":
    # subclass = Subclass1()
    Child()
