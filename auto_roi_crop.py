import vtk, json

print("====== Auto ROI Crop & Resample ======")
# Load the configuration from config.json
print("Loading configuration from config.json...")
with open("C:\\projects\\slicer_auto_roi\\config.json", "r") as f:
    data = json.load(f)
print("Data from config.json:")
print(data)

# Get the patient number
patientNumber = data.get("PatientNbr", "Unknown")
print("Patient number:", patientNumber)

# Get the reference volume (scanner)
volumeBaseName = data.get("VolumeBaseName", "DefaultVolume")
volumeNode = slicer.util.getNode(volumeBaseName)
if volumeNode is None:
    print("ERROR: Can't find the volume node with base name:", volumeBaseName)
    exit()
print("Reference volume node found with name:", volumeBaseName)

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


# Create cropped volume node
print("Creating cropped volume node...")
croppedVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "CroppedVolume")

# Configure the cropping parameters
print("Configuring cropping parameters...")
cropVolumeLogic = slicer.modules.cropvolume.logic()
cropVolumeParameters = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLCropVolumeParametersNode")
cropVolumeParameters.SetInputVolumeNodeID(volumeNode.GetID())
cropVolumeParameters.SetROINodeID(roiNode.GetID())
cropVolumeParameters.SetOutputVolumeNodeID(croppedVolumeNode.GetID())

#  Apply the cropping operation
cropVolumeLogic.Apply(cropVolumeParameters)
cleaned_volumeBaseName = volumeBaseName.replace(":", "_").replace(" ", "_").replace(".", "")
croppedVolumeNode.SetName(f"{patientNumber}_{cleaned_volumeBaseName}_Cropped")
print("Cropped volume created with name:", croppedVolumeNode.GetName())
