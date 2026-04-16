import os
import glob
import re

methods = [
    "SaveToFile", "LoadFromFile", "UpgradeLegacyData", "LoadEntitiesFromFile",
    "LoadEntitiesFromSlvs", "ReloadAllLinked", "SaveUsingTable", "LoadUsingTable",
    "ExportAsPngTo", "ExportMeshTo", "ExportMeshAsStlTo", "ExportMeshAsObjTo",
    "ExportMeshAsThreeJsTo", "ExportMeshAsVrmlTo", "ExportViewOrWireframeTo",
    "ExportSectionTo", "ExportWireframeCurves", "ExportLinesAndMesh",
    "UndoRemember", "UndoUndo", "UndoRedo", "PushFromCurrentOnto",
    "PopOntoCurrentFrom", "UndoClearState", "UndoClearStack",
    "GroupExists", "PruneOrphans", "EntityExists", "GroupsInOrder",
    "PruneGroups", "PruneRequestsAndConstraints",
    "GenerateAll", "SolveGroup", "SolveGroupAndReport", "TestRankForGroup",
    "WriteEqSystemForGroup", "MarkDraggedParams", "ForceReferences",
    "UpdateCenterOfMass", "ActiveGroupsOkay",
    "Clear", "MmPerUnit", "UnitName", "MmToString", "MmToStringSI",
    "DegreeToString", "ExprToMm", "StringToMm", "ChordTolMm",
    "ExportChordTolMm", "GetMaxSegments", "UnitDigitsAfterDecimal",
    "SetUnitDigitsAfterDecimal", "CameraTangent"
]

cpp_files = glob.glob("src/**/*.cpp", recursive=True)

for file in cpp_files:
    with open(file, "r") as f:
        content = f.read()
    
    changed = False
    for method in methods:
        old_str = f"SolveSpaceUI::{method}"
        new_str = f"SolveSpaceCore::{method}"
        if old_str in content:
            content = content.replace(old_str, new_str)
            changed = True
            
    if changed:
        with open(file, "w") as f:
            f.write(content)
        print(f"Updated {file}")
