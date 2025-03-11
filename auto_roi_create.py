import vtk, json

print("====== Auto ROI Create ======")

# Load the configuration from config.json
print("Loading configuration from config.json...")
with open("C:\projects\slicer_auto_roi\config.json", "r") as f:
    data = json.load(f)

print("Data from config.json:")
print(data)

print("Converting IJK to RAS coordinates...")
volumeBaseName = data.get("VolumeBaseName", "DefaultVolume")

# Get the reference volume (scanner)
volumeNode = slicer.util.getNode(volumeBaseName)
if volumeNode is None:
    print("ERROR: Can't find the volume node with base name:", volumeBaseName)
    exit()

ijkPoint = data.get("InitialPointIJK", [0, 0, 0])

ijkToRasMatrix = vtk.vtkMatrix4x4()
volumeNode.GetIJKToRASMatrix(ijkToRasMatrix)

print("Applying IJK to RAS transformation...")
rasPoint = [0, 0, 0, 1]  # Adding 1 for the homogeneous coordinates
ijkToRasMatrix.MultiplyPoint(ijkPoint + [1], rasPoint)

print("Initial IJK point :", ijkPoint)
print("Converted to RAS point :", rasPoint[:3])

print("Creating ROI node...")
roiName = data.get("RoiName", "AutoROI")
roiSize = data.get("RoiSize", [50, 50, 50])
roiInitialCenterRAS = rasPoint[:3]
roiFinalCenterRAS = data.get("RoiFinalCenterRAS", None)

roiNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsROINode")
roiNode.SetName(roiName)
roiNode.SetSize(roiSize)
roiNode.SetCenter(roiInitialCenterRAS)
print("ROI node created with name:", roiName)

# Sélectionner la face sur laquelle centrer le ROI (exemple : face supérieure)
roiCenteringFace = data.get("RoiCenteringFace", "none")
print("Centering ROI on face:", roiCenteringFace)


if roiCenteringFace == "none":
    roiFinalCenterRAS = roiInitialCenterRAS
elif roiCenteringFace == "top":
    roiFinalCenterRAS = [roiInitialCenterRAS[0], roiInitialCenterRAS[1], roiInitialCenterRAS[2] + roiSize[2] / 2]
elif roiCenteringFace == "bottom":
    roiFinalCenterRAS = [roiInitialCenterRAS[0], roiInitialCenterRAS[1], roiInitialCenterRAS[2] - roiSize[2] / 2]
elif roiCenteringFace == "front":
    roiFinalCenterRAS = [roiInitialCenterRAS[0], roiInitialCenterRAS[1] + roiSize[1] / 2, roiInitialCenterRAS[2]]
elif roiCenteringFace == "back":
    roiFinalCenterRAS = [roiInitialCenterRAS[0], roiInitialCenterRAS[1] - roiSize[1] / 2, roiInitialCenterRAS[2]]
elif roiCenteringFace == "right":
    roiFinalCenterRAS = [roiInitialCenterRAS[0] + roiSize[0] / 2, roiInitialCenterRAS[1], roiInitialCenterRAS[2]]
elif roiCenteringFace == "left":
    roiFinalCenterRAS = [roiInitialCenterRAS[0] - roiSize[0] / 2, roiInitialCenterRAS[1], roiInitialCenterRAS[2]]

print("Final ROI center:", roiFinalCenterRAS)
print("Setting final ROI center...")
roiNode.SetCenter(roiFinalCenterRAS)

