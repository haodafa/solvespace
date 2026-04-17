with open("src/solvespace_core.h", "r") as f:
    content = f.read()

# remove from solvespace_core.h
to_remove = r'''    enum class Generate : uint32_t \{[\s\S]*?bool ActiveGroupsOkay\(\);'''
import re
match = re.search(to_remove, content)
if match:
    content = content.replace(match.group(0), "")
else:
    print("Could not find Generate methods in solvespace_core.h")

with open("src/solvespace_core.h", "w") as f:
    f.write(content)

with open("src/solvespace.h", "r") as f:
    content = f.read()

to_add = match.group(0) if match else ""

# add back to solvespace.h right after "void MarkGroupDirtyByEntity(hEntity he);"
content = content.replace("    void MarkGroupDirtyByEntity(hEntity he);", f"    void MarkGroupDirtyByEntity(hEntity he);\n\n{to_add}")

with open("src/solvespace.h", "w") as f:
    f.write(content)
