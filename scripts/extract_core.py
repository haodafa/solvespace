import re

with open("src/solvespace.cpp", "r") as f:
    content = f.read()

# Define the regex for extracting the methods
methods_to_extract = [
    r'double SolveSpaceCore::MmPerUnit\(\) \{[\s\S]*?return 1\.0;\n\}',
    r'const char \*SolveSpaceCore::UnitName\(\) \{[\s\S]*?return "";\n\}',
    r'std::string SolveSpaceCore::MmToString\(double v, bool editable\) \{[\s\S]*?return ssprintf\("%.*f", digits, v\);\n\}',
    r'static const char \*DimToString\(int dim\) \{[\s\S]*?\}\n\}',
    r'static std::pair<int, std::string> SelectSIPrefixMm\(int ord, int dim\) \{[\s\S]*?return \{0, "m"\};\n\}',
    r'static std::pair<int, std::string> SelectSIPrefixInch\(int deg\) \{[\s\S]*?\}',
    r'std::string SolveSpaceCore::MmToStringSI\(double v, int dim\) \{[\s\S]*?compact \? "" : " ", unit\.c_str\(\), DimToString\(dim\)\);\n\}',
    r'std::string SolveSpaceCore::DegreeToString\(double v\) \{[\s\S]*?return ssprintf\("%.0f", v\);\n    \}\n\}',
    r'double SolveSpaceCore::ExprToMm\(Expr \*e\) \{[\s\S]*?return \(e->Eval\(\)\) \* MmPerUnit\(\);\n\}',
    r'double SolveSpaceCore::StringToMm\(const std::string &str\) \{[\s\S]*?return std::stod\(str\) \* MmPerUnit\(\);\n\}',
    r'double SolveSpaceCore::ChordTolMm\(\) \{[\s\S]*?return chordTolCalculated;\n\}',
    r'double SolveSpaceCore::ExportChordTolMm\(\) \{[\s\S]*?return exportChordTol / exportScale;\n\}',
    r'int SolveSpaceCore::GetMaxSegments\(\) \{[\s\S]*?return maxSegments;\n\}',
    r'int SolveSpaceCore::UnitDigitsAfterDecimal\(\) \{[\s\S]*?afterDecimalInch : afterDecimalMm;\n\}',
    r'void SolveSpaceCore::SetUnitDigitsAfterDecimal\(int v\) \{[\s\S]*?afterDecimalMm = v;\n    \}\n\}',
    r'double SolveSpaceCore::CameraTangent\(\) \{[\s\S]*?return cameraTangent;\n    \}\n\}',
    r'void SolveSpaceCore::Clear\(\) \{[\s\S]*?if\(i < redo\.cnt\) redo\.d\[i\]\.Clear\(\);\n    \}\n\}'
]

extracted = []
for pat in methods_to_extract:
    match = re.search(pat, content)
    if match:
        extracted.append(match.group(0))
        content = content.replace(match.group(0), "")
    else:
        print(f"Warning: Could not match {pat[:20]}")

with open("src/solvespace.cpp", "w") as f:
    f.write(content)

with open("src/solvespace_core.cpp", "w") as f:
    f.write("""//-----------------------------------------------------------------------------
// Core business logic, configuration, and document state.
//
// Copyright 2008-2013 Jonathan Westhues.
//-----------------------------------------------------------------------------

#include "solvespace.h"

namespace SolveSpace {

""")
    f.write("\n\n".join(extracted))
    f.write("\n\n} // namespace SolveSpace\n")

print("Done extracting core methods.")
