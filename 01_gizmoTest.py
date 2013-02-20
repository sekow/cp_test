import FabricEngine.CreationPlatform
from FabricEngine.CreationPlatform.PySide import *


class app(CreationPlatformApplication):

  def __init__(self, **options):

    super(app, self).__init__(**options)

    self.constructionCompleted()

# launch app
app().exec_()