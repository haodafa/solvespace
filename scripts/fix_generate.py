with open("src/generate.cpp", "r") as f:
    content = f.read()

content = content.replace("SolveSpaceCore::GenerateAll", "SolveSpaceUI::GenerateAll")
content = content.replace("SolveSpaceCore::SolveGroup", "SolveSpaceUI::SolveGroup")
content = content.replace("SolveSpaceCore::SolveGroupAndReport", "SolveSpaceUI::SolveGroupAndReport")
content = content.replace("SolveSpaceCore::TestRankForGroup", "SolveSpaceUI::TestRankForGroup")
content = content.replace("SolveSpaceCore::WriteEqSystemForGroup", "SolveSpaceUI::WriteEqSystemForGroup")
content = content.replace("SolveSpaceCore::MarkDraggedParams", "SolveSpaceUI::MarkDraggedParams")
content = content.replace("SolveSpaceCore::ForceReferences", "SolveSpaceUI::ForceReferences")
content = content.replace("SolveSpaceCore::UpdateCenterOfMass", "SolveSpaceUI::UpdateCenterOfMass")
content = content.replace("SolveSpaceCore::ActiveGroupsOkay", "SolveSpaceUI::ActiveGroupsOkay")

with open("src/generate.cpp", "w") as f:
    f.write(content)
