import vtk, json

print("====== Auto ROI Center ======")

# Load the configuration from config.json
print("Loading configuration from config.json...")
with open("/Users/paulineberard/workspace/slicer_auto_roi/config.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Data from config.json:")
print(data)

print("Getting ROI node...")
roiName = data.get("RoiName", "AutoROI")

try:
    roiNode = slicer.util.getNode(roiName)
    if roiNode and roiNode.IsA("vtkMRMLMarkupsROINode"):
        print("ROI node found with name:", roiName)
    else:
        print("No ROI node found with name:", roiName)
except slicer.util.MRMLNodeNotFoundException:
    print("No ROI node found with name:", roiName)

roiInitialCenterRAS = roiNode.GetCenter()
roiSize = roiNode.GetSize() 

# Get the ROI centering face
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

