import FabricEngine.CreationPlatform
from FabricEngine.CreationPlatform.PySide import *
from Nodes import *

class app(CreationPlatformApplication):

  def __init__(self, **options):

    super(app, self).__init__(**options)

    # get the main objects
    scene = self.getScene()
    viewport = self.getViewport()

    # create a transform
    gizmoTransform = GizmoTransform(scene, manipulatorThreshold = 0.25)

    # make the gizmo manipulator a child of the camera manipulator
    self.getCameraManipulator().setChildManipulatorNode(
      gizmoTransform.getGizmoManipulator()
    )

    # show the application on screen
    self.constructionCompleted()

# launch app
app().exec_()