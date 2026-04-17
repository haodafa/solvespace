with open("src/solvespace.cpp", "r") as f:
    content = f.read()

core_clear = """void SolveSpaceCore::Clear() {
    sys.Clear();
    for(int i = 0; i < MAX_UNDO; i++) {
        if(i < undo.cnt) undo.d[i].Clear();
        if(i < redo.cnt) redo.d[i].Clear();
    }
}

void SolveSpaceUI::Clear() {
    SolveSpaceCore::Clear();
    TW.window = NULL;"""

content = content.replace("""void SolveSpaceCore::Clear() {
    sys.Clear();
    for(int i = 0; i < MAX_UNDO; i++) {
        if(i < undo.cnt) undo.d[i].Clear();
        if(i < redo.cnt) redo.d[i].Clear();
    }
    TW.window = NULL;""", core_clear)

with open("src/solvespace.cpp", "w") as f:
    f.write(content)
