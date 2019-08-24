class Singleton:

   __instance = None

   def __init__(self, x):

      """ Virtually private constructor. """
      if Singleton.__instance != None:
         raise Exception("This class is a singleton!")
      else:
         Singleton.__instance = self

      self.instance_var1 = x

