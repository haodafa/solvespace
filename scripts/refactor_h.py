import re

with open('src/solvespace.h', 'r') as f:
    content = f.read()

# We need to insert `#include "solvespace_core.h"` right before `class SolveSpaceUI {`
content = content.replace('class SolveSpaceUI {', '#include "solvespace_core.h"\n\nclass SolveSpaceUI : public SolveSpaceCore {')

# Remove the extracted members from SolveSpaceUI
to_remove = [
    r'    // The state for undo/redo[\s\S]*?UndoStack   redo;',
    r'    // Little bits of extra configuration state[\s\S]*?double   explodeDistance;',
    r'    std::string MmToString\(double v, bool editable=false\);[\s\S]*?double CameraTangent\(\);',
    r'    // Some stuff relating to the tangent arcs created non-parametrically[\s\S]*?bool tangentArcModify;',
    r'    // File load/save routines, including the additional files that get[\s\S]*?std::vector<Platform::Path> recentFiles;',
    r'    bool SaveToFile\(const Platform::Path &filename\);',
    r'    bool LoadFromFile\(const Platform::Path &filename, bool canCancel = false\);',
    r'    void UpgradeLegacyData\(\);',
    r'    bool LoadEntitiesFromFile\(const Platform::Path &filename, EntityList \*le,[\s\S]*?SMesh \*m, SShell \*sh\);',
    r'    bool LoadEntitiesFromSlvs\(const Platform::Path &filename, EntityList \*le,[\s\S]*?SMesh \*m, SShell \*sh\);',
    r'    bool ReloadAllLinked\(const Platform::Path &filename, bool canCancel = false\);',
    r'    // And the various export options[\s\S]*?VectorFileWriter \*out\);',
    r'    class Clipboard \{[\s\S]*?Clipboard clipboard;',
    r'    // Consistency checking on the sketch: stuff with missing dependencies[\s\S]*?bool PruneRequestsAndConstraints\(hGroup hg\);',
    r'    enum class Generate : uint32_t \{[\s\S]*?bool ActiveGroupsOkay\(\);',
    r'    // The system to be solved\.[\s\S]*?System     &sys;',
    r'    // All the TrueType fonts in memory\s*TtfFontList fonts;',
    r'    // Everything has been pruned, so we know there\'s no dangling references[\s\S]*?bool allConsistent;',
    r'    void UndoRemember\(\);\s*void UndoUndo\(\);\s*void UndoRedo\(\);\s*void PushFromCurrentOnto\(UndoStack \*uk\);\s*void PopOntoCurrentFrom\(UndoStack \*uk\);\s*void UndoClearState\(UndoState \*ut\);\s*void UndoClearStack\(UndoStack \*uk\);'
]

for pat in to_remove:
    content = re.sub(pat, '', content)

# Remove 'delete pSys;' from ~SolveSpaceUI and 'pSys(new System()), sys(*pSys)'
content = re.sub(r'pSys\(new System\(\)\), sys\(\*pSys\)', '', content)
content = re.sub(r'delete pSys;', '', content)
content = re.sub(r',\s*\{\}', ' {}', content) # Clean up empty initializer list comma
content = re.sub(r':\s*\{\}', '{}', content)

with open('src/solvespace.h', 'w') as f:
    f.write(content)
