//-----------------------------------------------------------------------------
// Core business logic, configuration, and document state.
//
// Copyright 2008-2013 Jonathan Westhues.
//-----------------------------------------------------------------------------

#include "solvespace.h"

namespace SolveSpace {

double SolveSpaceCore::MmPerUnit() {
    switch(viewUnits) {
        case Unit::INCHES: return 25.4;
        case Unit::FEET_INCHES: return 25.4; // The 'unit' is still inches
        case Unit::METERS: return 1000.0;
        case Unit::MM: return 1.0;
    }
    return 1.0;
}

const char *SolveSpaceCore::UnitName() {
    switch(viewUnits) {
        case Unit::INCHES: return "in";
        case Unit::FEET_INCHES: return "in";
        case Unit::METERS: return "m";
        case Unit::MM: return "mm";
    }
    return "";
}

std::string SolveSpaceCore::MmToString(double v, bool editable) {
    v /= MmPerUnit();
    // The syntax 2' 6" for feet and inches is not something we can (currently)
    // parse back from a string so if editable is true, we treat FEET_INCHES the
    // same as INCHES and just return the unadorned decimal number of inches.
    if(viewUnits == Unit::FEET_INCHES && !editable) {
        // Now convert v from inches to 64'ths of an inch, to make rounding easier.
        v = floor((v + (1.0 / 128.0)) * 64.0);
        int feet = (int)(v / (12.0 * 64.0));
        v = v - (feet * 12.0 * 64.0);
        // v is now the feet-less remainder in 1/64 inches
        int inches = (int)(v / 64.0);
        int numerator = (int)(v - ((double)inches * 64.0));
        int denominator = 64;
        // Divide down to smallest denominator where the numerator is still a whole number
        while ((numerator != 0) && ((numerator & 1) == 0)) {
            numerator /= 2;
            denominator /= 2;
        }
        std::ostringstream str;
        if(feet != 0) {
            str << feet << "'-";
        }
        // For something like 0.5, show 1/2" rather than 0 1/2"
        if(!(feet == 0 && inches == 0 && numerator != 0)) {
            str << inches;
        }
        if(numerator != 0) {
            str << " " << numerator << "/" << denominator;
        }
        str << "\"";
        return str.str();
    }

    int digits = UnitDigitsAfterDecimal();
    double minimum = 0.5 * pow(10,-digits);
    while ((v < minimum) && (v > LENGTH_EPS)) {
        digits++;
        minimum *= 0.1;
    }
    return ssprintf("%.*f", digits, v);
}

static const char *DimToString(int dim) {
    switch(dim) {
        case 3: return "³";
        case 2: return "²";
        case 1: return "";
        default: ssassert(false, "Unexpected dimension");
    }
}

static std::pair<int, std::string> SelectSIPrefixMm(int ord, int dim) {
// decide what units to use depending on the order of magnitude of the
// measure in meters and the dimension (1,2,3 lenear, area, volume)
    switch(dim) {
        case 0:
        case 1:
                 if(ord >=  3) return {  3, "km" };
            else if(ord >=  0) return {  0, "m"  };
            else if(ord >= -2) return { -2, "cm" };
            else if(ord >= -3) return { -3, "mm" };
            else if(ord >= -6) return { -6, "µm" };
            else               return { -9, "nm" };
            break;
        case 2:
                 if(ord >=  5) return {  3, "km" };
            else if(ord >=  0) return {  0, "m"  };
            else if(ord >= -2) return { -2, "cm" };
            else if(ord >= -6) return { -3, "mm" };
            else if(ord >= -13) return { -6, "µm" };
            else               return { -9, "nm" };
            break;
        case 3:
                 if(ord >=  7) return {  3, "km" };
            else if(ord >=  0) return {  0, "m"  };
            else if(ord >= -5) return { -2, "cm" };
            else if(ord >= -11) return { -3, "mm" };
            else                return { -6, "µm" };
            break;
        default:
            dbp ("dimensions over 3 not supported");
            break;
    }
    return {0, "m"};
}

static std::pair<int, std::string> SelectSIPrefixInch(int deg) {
         if(deg >=  0) return {  0, "in"  };
    else if(deg >= -3) return { -3, "mil" };
    else               return { -6, "µin" };
}

std::string SolveSpaceCore::MmToStringSI(double v, int dim) {
    bool compact = false;
    if(dim == 0) {
        if(!useSIPrefixes) return MmToString(v);
        compact = true;
        dim = 1;
    }

    bool inches = (viewUnits == Unit::INCHES) || (viewUnits == Unit::FEET_INCHES);
    v /= pow(inches ? 25.4 : 1000, dim);
    int vdeg = (int)(log10(fabs(v)));
    std::string unit;
    if(fabs(v) > 0.0) {
        int sdeg = 0;
        std::tie(sdeg, unit) =
            inches
            ? SelectSIPrefixInch(vdeg/dim)
            : SelectSIPrefixMm(vdeg, dim);
        v /= pow(10.0, sdeg * dim);
    }
    if(viewUnits == Unit::FEET_INCHES && fabs(v) > pow(12.0, dim)) {
        unit = "ft";
        v /= pow(12.0, dim);
    }
    int pdeg = (int)ceil(log10(fabs(v) + 1e-10));
    return ssprintf("%.*g%s%s%s", pdeg + UnitDigitsAfterDecimal(), v,
                    compact ? "" : " ", unit.c_str(), DimToString(dim));
}

std::string SolveSpaceCore::DegreeToString(double v) {
    if(fabs(v - floor(v)) > 1e-10) {
        return ssprintf("%.*f", afterDecimalDegree, v);
    } else {
        return ssprintf("%.0f", v);
    }
}

double SolveSpaceCore::ExprToMm(Expr *e) {
    return (e->Eval()) * MmPerUnit();
}

double SolveSpaceCore::StringToMm(const std::string &str) {
    return std::stod(str) * MmPerUnit();
}

double SolveSpaceCore::ChordTolMm() {
    if(exportMode) return ExportChordTolMm();
    return chordTolCalculated;
}

double SolveSpaceCore::ExportChordTolMm() {
    return exportChordTol / exportScale;
}

int SolveSpaceCore::GetMaxSegments() {
    if(exportMode) return exportMaxSegments;
    return maxSegments;
}

int SolveSpaceCore::UnitDigitsAfterDecimal() {
    return (viewUnits == Unit::INCHES || viewUnits == Unit::FEET_INCHES) ?
           afterDecimalInch : afterDecimalMm;
}

void SolveSpaceCore::SetUnitDigitsAfterDecimal(int v) {
    if(viewUnits == Unit::INCHES || viewUnits == Unit::FEET_INCHES) {
        afterDecimalInch = v;
    } else {
        afterDecimalMm = v;
    }
}

double SolveSpaceCore::CameraTangent() {
    if(!usePerspectiveProj) {
        return 0;
    } else {
        return cameraTangent;
    }
}

void SolveSpaceCore::Clear() {
    sys.Clear();
    for(int i = 0; i < MAX_UNDO; i++) {
        if(i < undo.cnt) undo.d[i].Clear();
        if(i < redo.cnt) redo.d[i].Clear();
    }
}

} // namespace SolveSpace
