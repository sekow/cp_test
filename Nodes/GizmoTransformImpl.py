from FabricEngine.CreationPlatform.Nodes.Kinematics import *
from FabricEngine.CreationPlatform.RT.Geometry.GizmoTypeImpl import GizmoType
from FabricEngine.CreationPlatform.Nodes.Manipulation.GizmoInstanceImpl import GizmoInstance
from FabricEngine.CreationPlatform.Nodes.Manipulation.GizmoManipulatorImpl import GizmoManipulator

class GizmoTransform(Transform):

  def __init__(self, scene, **options):

    super(GizmoTransform, self).__init__(scene, **options)

    # get the dependency graph node
    dgNode = self.getDGNode()
    dgNode.addMember('gizmo', 'GizmoType')
    dgNode.addMember('gizmoMode', 'Integer', 0)

    # create a gizmo instance to display the gizmos
    self.__gizmoInstance = self.constructSubNode(GizmoInstance,
      source=self, 
      sourceDGNodeName='DGNode',
      sourceMemberName='gizmo'
    )

    # create a manipulator to be able to move the gizmos around
    self.__gizmoManipulator = self.constructSubNode(
      GizmoManipulator,
      threshold = options.setdefault('manipulatorThreshold', 0.2)
    )
    self.__gizmoManipulator.addGizmoNode(self.__gizmoInstance)

    # create the operator to draw the gizmo
    self.bindDGOperator(dgNode.bindings,
      name = 'gizmoTransformOp',
      layout = [
        'self.index',
        'self.globalXfo',
        'self.gizmoMode',
        'self.gizmo'
      ],
      fileName = FabricEngine.CreationPlatform.buildAbsolutePath('GizmoTransform.kl')
    )

    # setup private members
    self.__gizmoHandler = None

  def getGizmoInstance(self):
    return self.__gizmoInstance

  def getGizmoManipulator(self):
    return self.__gizmoManipulator

  def mousePressEvent(self, event):

    # extract the hitData
    hitData = event['hitData']

    # get the transform of the camera
    camXfo = event['viewport'].getCameraNode().getTransformNode().getGlobalXfo()

    # store private members
    self.__gizmoHandler = hitData.gizmoHandler
    self.__bindingId = hitData.bindingId
    self.__parentXfo = hitData.xfo.clone()

    # construct a plane in the camera space
    self.__planePoint = hitData.point.clone()
    self.__parentOffset = self.__parentXfo.tr.subtract(self.__planePoint)

    # construct a plane normal (this should be dependent on the mode)
    self.__planeNormal = camXfo.ori.getZaxis()

  def mouseReleaseEvent(self, event):
    self.__gizmoHandler = None
    return True

  def mouseMoveEvent(self, event):

    # cancel manipulation if no handler present
    if self.__gizmoHandler is None:
      return False

    # compute the new point on the plane (again, dependent on the type of gizmo)
    viewport = event['viewport']
    ray = viewport.calcRayFromMouseEvent(event)
    point = ray.pointFromFactor(ray.intersectPlane(self.__planePoint, self.__planeNormal))  

    # choose the manipulation to perform
    if self.__gizmoHandler == 'redLine':

      # move the transform
      xfo = self.__parentXfo.clone()
      xfo.tr = point.add(self.__parentOffset)

      # set the transform in the DG
      self.getDGNode().setData('localXfo', self.__bindingId, xfo)

    return True