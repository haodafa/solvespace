//-----------------------------------------------------------------------------
// Core business logic, configuration, and document state.
//
// Copyright 2008-2013 Jonathan Westhues.
//-----------------------------------------------------------------------------

#ifndef SOLVESPACE_CORE_H
#define SOLVESPACE_CORE_H


#include "ui.h"

class SolveSpaceCore {
public:
    mutable std::mutex stateMutex;

    GraphicsWindow              GW;
    TextWindow                 *pTW;
    TextWindow                 &TW;

    // The state for undo/redo
    typedef struct UndoState {
        IdList<Group,hGroup>            group;
        List<hGroup>                    groupOrder;
        IdList<Request,hRequest>        request;
        IdList<Constraint,hConstraint>  constraint;
        ParamList                       param;
        IdList<Style,hStyle>            style;
        hGroup                          activeGroup;

        void Clear() {
            group.Clear();
            request.Clear();
            constraint.Clear();
            param.Clear();
            style.Clear();
        }
    } UndoState;
    enum { MAX_UNDO = 100 };
    typedef struct {
        UndoState   d[MAX_UNDO];
        int         cnt;
        int         write;
    } UndoStack;
    UndoStack   undo;
    UndoStack   redo;

    class Clipboard {
    public:
        List<ClipboardRequest>  r;
        List<Constraint>        c;

        void Clear();
        bool ContainsEntity(hEntity old);
        hEntity NewEntityFor(hEntity old);
    };
    Clipboard clipboard;

    // Little bits of extra configuration state
    enum { MODEL_COLORS = 8 };
    RgbaColor modelColor[MODEL_COLORS];
    Vector   lightDir[2];
    double   lightIntensity[2];
    double   ambientIntensity;
    double   chordTol;
    double   chordTolCalculated;
    int      maxSegments;
    double   exportChordTol;
    int      exportMaxSegments;
    int      timeoutRedundantConstr; //milliseconds
    int      animationSpeed; //milliseconds
    double   cameraTangent;
    double   gridSpacing;
    double   exportScale;
    double   exportOffset;
    bool     arcDimDefaultDiameter;
    bool     showFullFilePath;
    bool     fixExportColors;
    bool     exportBackgroundColor;
    bool     drawBackFaces;
    bool     showContourAreas;
    bool     checkClosedContour;
    bool     cameraNav;
    bool     turntableNav;
    bool     immediatelyEditDimension;
    bool     automaticLineConstraints;
    bool     showToolbar;
    Platform::Path screenshotFile;
    RgbaColor backgroundColor;
    bool     exportShadedTriangles;
    bool     exportPwlCurves;
    bool     exportCanvasSizeAuto;
    bool     exportMode;
    struct {
        double  left;
        double  right;
        double  bottom;
        double  top;
    }        exportMargin;
    struct {
        double  width;
        double  height;
        double  dx;
        double  dy;
    }        exportCanvas;
    struct {
        double  depth;
        double  safeHeight;
        int     passes;
        double  feed;
        double  plungeFeed;
    }        gCode;

    Unit     viewUnits;
    int      afterDecimalMm;
    int      afterDecimalInch;
    int      afterDecimalDegree;
    bool     useSIPrefixes;
    int      autosaveInterval; // in minutes
    bool     explode;
    double   explodeDistance;

    std::string MmToString(double v, bool editable=false);
    std::string MmToStringSI(double v, int dim = 0);
    std::string DegreeToString(double v);
    double ExprToMm(Expr *e);
    double StringToMm(const std::string &s);
    const char *UnitName();
    double MmPerUnit();
    int UnitDigitsAfterDecimal();
    void SetUnitDigitsAfterDecimal(int v);
    double ChordTolMm();
    double ExportChordTolMm();
    int GetMaxSegments();
    bool usePerspectiveProj;
    double CameraTangent();

    // Some stuff relating to the tangent arcs created non-parametrically
    // as special requests.
    double tangentArcRadius;
    bool tangentArcManual;
    bool tangentArcModify;

    // File load/save routines, including the additional files that get
    // loaded when we have link groups.
    FILE        *fh;
    Platform::Path saveFile;
    bool        fileLoadError;
    bool        unsaved;
    typedef struct {
        char        type;
        const char *desc;
        char        fmt;
        void       *ptr;
    } SaveTable;
    static const SaveTable SAVED[];
    void SaveUsingTable(const Platform::Path &filename, int type);
    void LoadUsingTable(const Platform::Path &filename, char *key, char *val);
    struct {
        Group        g;
        Request      r;
        Entity       e;
        Param        p;
        Constraint   c;
        Style        s;
    } sv;

    static constexpr size_t MAX_RECENT = 8;
    static constexpr const char *SKETCH_EXT = "slvs";
    static constexpr const char *BACKUP_EXT = "slvs~";
    std::vector<Platform::Path> recentFiles;
    
    // I/O methods
    bool SaveToFile(const Platform::Path &filename);
    bool LoadFromFile(const Platform::Path &filename, bool canCancel = false);
    void UpgradeLegacyData();
    bool LoadEntitiesFromFile(const Platform::Path &filename, EntityList *le,
                              SMesh *m, SShell *sh);
    bool LoadEntitiesFromSlvs(const Platform::Path &filename, EntityList *le,
                              SMesh *m, SShell *sh);
    bool ReloadAllLinked(const Platform::Path &filename, bool canCancel = false);

    // Export methods
    void ExportAsPngTo(const Platform::Path &filename);
    void ExportMeshTo(const Platform::Path &filename);
    void ExportMeshAsStlTo(FILE *f, SMesh *sm);
    void ExportMeshAsObjTo(FILE *fObj, FILE *fMtl, SMesh *sm);
    void ExportMeshAsThreeJsTo(FILE *f, const Platform::Path &filename,
                               SMesh *sm, SOutlineList *sol);
    void ExportMeshAsVrmlTo(FILE *f, const Platform::Path &filename, SMesh *sm);
    void ExportViewOrWireframeTo(const Platform::Path &filename, bool exportWireframe);
    void ExportSectionTo(const Platform::Path &filename);
    void ExportWireframeCurves(SEdgeList *sel, SBezierList *sbl,
                               VectorFileWriter *out);
    void ExportLinesAndMesh(SEdgeList *sel, SBezierList *sbl, SMesh *sm,
                            Vector u, Vector v,
                            Vector n, Vector origin,
                            double cameraTan,
                            VectorFileWriter *out);

    void UndoRemember();
    void UndoUndo();
    void UndoRedo();
    void PushFromCurrentOnto(UndoStack *uk);
    void PopOntoCurrentFrom(UndoStack *uk);
    void UndoClearState(UndoState *ut);
    void UndoClearStack(UndoStack *uk);

    // Consistency checking
    struct {
        int     requests;
        int     groups;
        int     constraints;
        int     nonTrivialConstraints;
    } deleted;
    bool GroupExists(hGroup hg);
    bool PruneOrphans();
    bool EntityExists(hEntity he);
    bool GroupsInOrder(hGroup before, hGroup after);
    bool PruneGroups(hGroup hg);
    bool PruneRequestsAndConstraints(hGroup hg);



    // The system to be solved.
    System     *pSys;
    System     &sys;

    // The sketch
    Sketch     sketch;

    // All the TrueType fonts in memory
    TtfFontList fonts;

    bool allConsistent;
    virtual void ClearExisting() {}
    virtual void UndoEnableMenus() {}
    virtual void NewFile() {}
    virtual bool ReloadLinkedImage(const Platform::Path &saveFile, Platform::Path *filename, bool canCancel) { return false; }

    void Clear();

    SolveSpaceCore()
        : pTW(new TextWindow()), TW(*pTW), pSys(new System()), sys(*pSys) {}

    ~SolveSpaceCore() {
        delete pTW;
        delete pSys;
    }
};

extern SolveSpaceCore &CORE;
extern Sketch &SK;


#endif
