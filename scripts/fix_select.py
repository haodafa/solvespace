with open("src/solvespace_core.cpp", "r") as f:
    content = f.read()

content = content.replace('static std::pair<int, std::string> SelectSIPrefixInch(int deg) {\n         if(deg >=  0) return {  0, "in"  }', 'static std::pair<int, std::string> SelectSIPrefixInch(int deg) {\n         if(deg >=  0) return {  0, "in"  };\n    else if(deg >= -3) return { -3, "mil" };\n    else               return { -6, "µin" };\n}')

with open("src/solvespace_core.cpp", "w") as f:
    f.write(content)
