import FabricEngine.CreationPlatform
from FabricEngine.CreationPlatform.PySide import *


class app(CreationPlatformApplication):

  def __init__(self):

    super(CreationPlatformApplication, self).__init__()


# launch app
app().exec_()