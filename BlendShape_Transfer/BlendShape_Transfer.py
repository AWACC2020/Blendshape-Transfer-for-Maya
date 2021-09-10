# -!- coding: utf-8 -!-
# Author  : AWACS
# Time	: 2020/10/20
# version : 0.52 beta

import maya.cmds as cmds
import os

def Question_Button( COMMAND = None , blank_space = 1 ,  btn_label = " ? " ):
    cmds.text( l= " " ,w = blank_space )
    cmds.button( c=lambda *args: eval( COMMAND ) , l= btn_label , w=20 )

def Question_Window( imageNum = 0 , Window_name = 'Question_Window' , w = 540 , h = 540):
    if cmds.window( Window_name , q=1, ex=1 ):
        cmds.deleteUI( Window_name )
    cmds.window( Window_name )
    #cmds.dockControl( area='left', content=myWindow, allowedArea=allowedAreas )
    imagelist = ["Question_BlendShape_Transfer_1.jpg" ,
                 "Question_BlendShape_Transfer_2.jpg" ,
                 "Question_BlendShape_Transfer_3.jpg" ,
                 "Question_BlendShape_Transfer_4.jpg" ,
                 "Question_BlendShape_Transfer_5.jpg" ,
                 ]
    print ( Question_Window_image_path +  "/" + imagelist[ imageNum ] )
    cmds.paneLayout()
    cmds.image( image= Question_Window_image_path +  "/" + imagelist[ imageNum ] )

    cmds.showWindow( Window_name )

def BlendShape_Transfer_GUI():
    if cmds.window('BlendShape_Transfer', q = 1, ex = 1):
        cmds.deleteUI('BlendShape_Transfer')

    cmds.window('BlendShape_Transfer')
    cmds.showWindow('BlendShape_Transfer')
    cmds.columnLayout()

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 1: ")
    cmds.text(label = "Transfer Method XX:  ", w = 200, align = "right")
    cmds.optionMenu( "Transfer_Method" , w = 180 )
    cmds.menuItem( label='Wrap deformer' )
    # cmds.menuItem( label='Sorry,No others yet,I may add more later' )
    # Question_Button("Question_Window( 0 )", 10)
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 2: ")
    cmds.text(label = "Select Original Mesh ( with old BS Node ) :  ", w = 200, align = "right")
    cmds.textField('Input_Source_Mesh', w = 140, h = 24, text = "")
    cmds.button(c = lambda *args: Set_Source_Geo(), label = "Confirm", w = 50)
    # Question_Button("Question_Window( 0 )", 10)
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 3: ")
    cmds.text(label = "Select Target Mesh  ( Transfer to Where ) :  ", w = 200, align = "right")
    cmds.textField('Input_Target_Mesh', w = 140, h = 24, text = "")
    cmds.button(c = lambda *args: Set_Target_Geo(), label = "Confirm", w = 50)
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 4: ")
    cmds.text(label = "Set Source Blendshape (Optional) :  ", w = 200, align = "right")
    cmds.textField('InputBS', w = 140, h = 24, text = "")
    cmds.button(c = lambda *args: Set_Source_BS(), label = "Confirm", w = 50)
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 5: ")
    cmds.text(label = " New Blendshape Name :  ", w = 200, align = "right")
    cmds.textField('New_BS_Name', w = 180, h = 24, text = "BS_Transfered")
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 6: ")
    # cmds.text(label = "Add to Existing Blendshape Node : ", w = 140)
    
    cmds.checkBox( "Add_to_exist_BS" , l ="     Add to existing Blendshape :  ", value = False, w = 200, align = "right")
    # cmds.text(label = " Existing_BS :  " ,w = 80)
    cmds.textField('Existing_BS', w = 140, h = 24, text = "")
    cmds.button(c = lambda *args: Set_Existing_BS(), label = "Confirm", w = 50)
    cmds.setParent('..')

    # cmds.rowLayout(nc = 6)
    # cmds.text(label = " 6: ")
    # cmds.text(label = "Distant threshold : ")
    # cmds.floatField("Distant_threshold", max = 0.1, min = 0.0, value = 0.002)
    # cmds.setParent('..')
    cmds.rowLayout(nc = 6)
    cmds.text(label = " 7: ")
    # cmds.text(label = "Add to Existing Blendshape Node : ", w = 140)
    
    cmds.checkBox( "Append_Driven" , l ="     Append_Driven  ", value = False, w = 200, align = "right")
    # cmds.text(label = " Existing_BS :  " ,w = 80)
    cmds.setParent('..')


    cmds.rowLayout(nc = 6)
    cmds.text(label = " 8: ")
    cmds.button(c = lambda *args: ExecuteTransferBS(), label = "Execute BlendShape Transfer ", w = 180)
    cmds.setParent('..')


def Object_Type_Checker( InputObject, Object_Type ):
    """
    Check node type , check for shape if it is transform
    """
    if cmds.nodeType(InputObject) == Object_Type:
        return True
    else:
        if cmds.nodeType(InputObject) == "transform":
            RelativeNodes = cmds.listRelatives(InputObject)
            if RelativeNodes:
                for indRelative in RelativeNodes:
                    if cmds.nodeType(indRelative) == Object_Type:
                        return True
        return False

def Set_Source_Geo():
    Selection = cmds.ls(selection = True)
    if Object_Type_Checker(Selection[0], "mesh"):
        cmds.textField('Input_Source_Mesh', e = 1, tx = Selection[0])
        print ("//// Source Mesh Selected : " + Selection[0])
    else:
        print ("//// Error Object Select , Please Select A Polygon Mesh ")

def Set_Target_Geo():
    Selection = cmds.ls(selection = True)
    if Object_Type_Checker(Selection[0], "mesh"):
        cmds.textField('Input_Target_Mesh', e = 1, tx = Selection[0])
        print ("//// Target Mesh Selected : " + Selection[0])
    else:
        print ("//// Error Object Select , Please Select A Polygon Mesh ")

def Set_Source_BS():
    Selection = cmds.ls(selection = True)
    if Selection:
        Source_BS_list = []
        for indSel in Selection:
            if Object_Type_Checker(indSel, "blendShape"):
                Source_BS_list.append(indSel)
        print (Source_BS_list)
        if len(Source_BS_list) < 1:
            print ("//// Error Object Select , Please Select A BlendShape Node at least ")
        else:
            BS_Display = ""
            for indBS in Source_BS_list:
                BS_Display += indBS
                BS_Display += " "
            cmds.textField('InputBS', e = 1, tx = BS_Display)
            print ("//// Source BlendShape Selected : " + BS_Display)
    else:
        cmds.textField('InputBS', e = 1, tx = None)
        print ("//// Source BlendShape is empty,I will try to find a existing Blendshape if execute transfering ")

def Set_Existing_BS(  ):
    Selection = cmds.ls(selection = True)
    if Object_Type_Checker(Selection[0], "blendShape"):
        cmds.textField('Existing_BS', e = 1, tx = Selection[0])
        print ("//// Existing Blendshape Selected : " + Selection[0])
    else:
        print ("//// Error Object Select , Please Select A BlendShape Node ")

def SearchingForBlendshape( InputNode ):
    """
    try to find Blendshape node from a mesh
    """
    RelativeNodes = cmds.listRelatives(InputNode ,shapes = True)
    SearchResult = []
    # Result_counter = 0
    if RelativeNodes:
        for indRel in RelativeNodes:
            # print (indRel)
            indRel_Rel_Nodes = cmds.listConnections(indRel)
            if indRel_Rel_Nodes:
                print (indRel_Rel_Nodes)
                for indRel_Rel_Rel in indRel_Rel_Nodes:
                    if Object_Type_Checker(indRel_Rel_Rel, "blendShape"):
                        SearchResult.append(indRel_Rel_Rel)
                        # Result_counter += 1
        print( InputNode + " BS Search Result : " + str(SearchResult) )
        # if Result_counter > 0 :
        print (SearchResult)
        if SearchResult == []:
            return None
        return SearchResult
        # else:
        #     return None
    else:
        return None


def ExecuteTransferBS():
    Source_Geo = cmds.textField('Input_Source_Mesh', query = 1, text = 1)
    Target_Geo = cmds.textField('Input_Target_Mesh', query = 1, text = 1)
    Source_BS_Text = cmds.textField('InputBS', query = 1, text = 1)
    NewBSName = cmds.textField('New_BS_Name', query = 1, text = 1)

    Append_Driven = cmds.checkBox( "Append_Driven" , query = 1, value = 1)
    Add_to_Exist_BS = cmds.checkBox( "Add_to_exist_BS" , query = 1, value = 1)
    Existing_BS = cmds.textField( "Existing_BS" , query = 1, text = 1) 
    if len(Existing_BS) < 1 :
        if Add_to_Exist_BS:
            Existing_BS = SearchingForBlendshape(Target_Geo)

    if Existing_BS is None :
        Add_to_Exist_BS = False


    if len(Source_BS_Text) > 0:
        Source_BS = Source_BS_Text.split(" ")
    else:
        Source_BS = SearchingForBlendshape(Source_Geo)

    print ("-------------------")
    print(Source_BS)

    if Source_BS:
        print ("SSSSSSSSSSSSSSSSSSSSSSSS")
        for IndSrcBS in Source_BS:
            if IndSrcBS == "" :
                continue
            if len(IndSrcBS) > 0 :
                print((Source_Geo, IndSrcBS, Target_Geo, Add_to_Exist_BS , Existing_BS , False, Append_Driven ,NewBSName))
                BlendShape_Transfer_to_Subdivided_geo(Source_Geo, IndSrcBS, Target_Geo, Add_to_Exist_BS , Existing_BS , False, Append_Driven ,NewBSName)
            else:
                print( "No Blendshape Node Found , please select Blendshape Node And Confirm Manually" )

def Create_Wrap( DriveR_Mesh, DriveN_Mesh, name, threshold = 0, maxDistance = 1.0, exclusiveBind = True,
                 autoWeightThreshold = True,
                 falloffMode = 0 ):
    """
    Create Wrap and setting up parameter
    """
    cmds.select(cl = 1)
    cmds.select(DriveN_Mesh)
    cmds.select(DriveR_Mesh, add = 1)
    tempString = cmds.deformer(type = 'wrap', n = name)
    wrapNode = tempString[0]
    cmds.setAttr(wrapNode + ".weightThreshold", threshold)
    cmds.setAttr(wrapNode + ".maxDistance", maxDistance)
    cmds.setAttr(wrapNode + ".exclusiveBind", exclusiveBind)
    cmds.setAttr(wrapNode + ".autoWeightThreshold", autoWeightThreshold)
    cmds.setAttr(wrapNode + ".falloffMode", falloffMode)

    cmds.AddWrapInfluence()
    cmds.select(cl = 1)
    return wrapNode


def Create_BS( SourceGeo, BS_Name ):
    cmds.select(cl = 1)
    cmds.select(SourceGeo)
    BS = cmds.blendShape(automatic = 1)
    renameResult = cmds.rename(BS[0], BS_Name)
    return renameResult


def Initialize_BS( BSNode ):
    """
    Zero out Blendshape attributes
    """
    BS_Node_target_list = cmds.listAttr(BSNode + ".w", k = True, m = True)
    cmds.setAttr(BSNode + ".envelope", 1)
    try:
        for indBS_Node_target in BS_Node_target_list:
            cmds.setAttr(BSNode + '.' + indBS_Node_target, 0)
    except:
        print("Initialize BS Func Failed")


def polySmooth_Custom( InputObject, Level = 1 ):
    cmds.polySmooth(InputObject,
                    constructionHistory = 1,
                    osdSmoothTriangles = 0,
                    keepHardEdge = 0,
                    pushStrength = 0.1,
                    keepMapBorders = 1,
                    boundaryRule = 1,
                    method = 0,
                    smoothUVs = 1,
                    propagateEdgeHardness = 0,
                    keepSelectionBorder = 1,
                    roundness = 1,
                    subdivisionType = 2,
                    osdFvarPropagateCorners = 0,
                    keepTessellation = 1,
                    osdVertBoundary = 1,
                    divisions = 1,
                    osdFvarBoundary = 3,
                    keepBorder = 1,
                    continuity = 1,
                    osdCreaseMethod = 0,
                    divisionsPerEdge = 1,
                    subdivisionLevels = Level)


def Point_distance_Checker ( inputgeoA , inputgeoB , threshold , faster = True ):
    """
    check if mismatch pointpos
    mismatch return True
    match return False
    """
    ptnum = cmds.polyEvaluate( inputgeoA )['vertex']
    cmds.cycleCheck(e=False)

    if faster:
        for i in range( ptnum ):
            VPosA = cmds.xform( inputgeoA + '.vtx[' + str(i) + ']', query = 1, worldSpace = 1, translation = 1)
            VPosB = cmds.xform( inputgeoB + '.vtx[' + str(i) + ']', query = 1, worldSpace = 1, translation = 1)

            if abs( VPosB[0] - VPosA[0] ) > threshold:
                cmds.cycleCheck(e=True)
                return True
            if abs( VPosB[1] - VPosA[1] ) > threshold:
                cmds.cycleCheck(e=True)
                return True
            if abs( VPosB[2] - VPosA[2]) > threshold:
                cmds.cycleCheck(e=True)
                return True
        cmds.cycleCheck(e=True)
        return False
    else:
        for i in range( ptnum ):
            VPosA = cmds.xform( inputgeoA + '.vtx[' + str(i) + ']', query = 1, worldSpace = 1, translation = 1)
            VPosB = cmds.xform( inputgeoB + '.vtx[' + str(i) + ']', query = 1, worldSpace = 1, translation = 1)

            dist3 = ( ( VPosB[0] - VPosA[0] ) ** 2 + ( VPosB[1] - VPosA[1] ) ** 2 + ( VPosB[2] - VPosA[2] ) ** 2 ) 

            if dist3 > threshold**2 :
                cmds.cycleCheck(e=True)
                return True

        cmds.cycleCheck(e=True)
        return False

def BlendShape_Transfer_to_Subdivided_geo( Source_Geo, BS_Node, Target_Geo, Add_to_Existing_BS, Existing_BS,
                                           Subdivided_Transfer, Append_Driven , NewBSName = "" ):
    # LowPolySrc , BS_of_LowPolySrc ):, HighPolyGeo , HighPoly_is_Extended , Transfer_Vertex , Transfer_Method , New_name_list ):
    # transfer the low Poly Mesh Blendshape to a Extended High Poly Mesh
    print ( "Source BS : " + BS_Node )

    BS_Node_target_list = cmds.listAttr(BS_Node + ".w", k = True, m = True)
    print (BS_Node_target_list)

    if not Append_Driven:
        Initialize_BS(BS_Node)

    # Duplicate
    # if Subdivided_Transfer:
    # 	polySmooth_Custom(Source_Geo , 1 )

    # BS_Target_low = []
    # for indBS_Node_target in BS_Node_target_list:
    # 	cmds.setAttr(BS_Node + '.' + indBS_Node_target, 1)
    # 	# tmp_BS_Target = cmds.duplicate( Source_Geo , n = Source_Geo + "_Temp_" + indBS_Node_target )
    # 	cmds.setAttr(BS_Node + '.' + indBS_Node_target, 0)
    # 	# BS_Target_low.append(tmp_BS_Target[0])
    # 	# print (type(tmp_BS_Target))

    # tmp = 50
    # for ind_BS_Target_Low in BS_Target_low:
    # 	cmds.setAttr(ind_BS_Target_Low + '.translateX', tmp)
    # 	tmp += 50

    # Warp Readying
    Target_Geo_Transfer_Ready = cmds.duplicate(Target_Geo, n = Target_Geo + "_Temp_Transfer_Ready")[0]
    # Duplicated_Wrap_Src = cmds.duplicate(Source_Geo, upstreamNodes = True , renameChildren = True )
    Duplicated_Wrap_Src = [ Source_Geo ]

    # return 0
    # Duplicated_Wrap_Src = []

    Wrap_Src_Geo = Duplicated_Wrap_Src[0]

    # ------------------------------------------------------------Search in list of duplicated object
    # aborted
    # Wrap_Src_BS = ""
    # possibleBs = [ ]
    # for indObject in Duplicated_Wrap_Src:
    #     if Object_Type_Checker(indObject, "blendShape"):
    #         # confirming Duplicated Bs Node ##might be some issue
    #         # Wrap_Src_BS = indObject
    #         possibleBs.append ( indObject )
    #         # break
    # for indpossibleBs in possibleBs :
    #     if indpossibleBs.split(":")[-1] == BS_Node.split(":") :
    #         print ("Duplicated BS SRC Located : " + indpossibleBs )
    #         print (indpossibleBs)
    #         Wrap_Src_BS = indpossibleBs


    # print (BS_Node)
    # print (possibleBs)
    # ------------------------------------------------------------Search in list of duplicated object

    # Wrap_Src_BS = "BS_FAC_TEMP1"
    Wrap_Src_BS = BS_Node

    # print("==========================================================================")
    # print (Duplicated_Wrap_Src)
    #
    # if len(Wrap_Src_BS) <1 :
    #     for indObject in Duplicated_Wrap_Src:
    #         Wrap_Src_BS = SearchingForBlendshape( indObject )
    #         if Wrap_Src_BS :
    #             break
    
    print ( "==========================================================================" )
    print ( Wrap_Src_BS )
    # return 0
    # print (Target_Geo_Transfer_Ready)

    WarpNode = Create_Wrap(Wrap_Src_Geo, Target_Geo_Transfer_Ready, "WarpNode", 0, 1.0, False, False, 0)
    Duped_Target_Geo_list = []
    
    driven_source_list = []

    for indTarget in BS_Node_target_list:
        if Append_Driven:
            indTarget_Driven_input = cmds.listConnections(  Wrap_Src_BS + '.' + indTarget  , plugs = True )[0]
            print ( indTarget_Driven_input )
            print ( Wrap_Src_BS + '.' + indTarget )
            cmds.disconnectAttr( indTarget_Driven_input , Wrap_Src_BS + '.' + indTarget )

        cmds.setAttr(Wrap_Src_BS + '.' + indTarget, 1)
        # cmds.setAttr(WarpNode + ".envelope", 0)
        # cmds.setAttr(WarpNode + ".envelope", 1)
        tmp_BS_Target = cmds.duplicate(Target_Geo_Transfer_Ready, n = Target_Geo_Transfer_Ready + "_Temp_" + indTarget)

        cmds.setAttr(Wrap_Src_BS + '.' + indTarget, 0)
        Duped_Target_Geo_list.append(tmp_BS_Target[0])

        if Append_Driven:
            cmds.connectAttr( indTarget_Driven_input , Wrap_Src_BS + '.' + indTarget , f=1)
            driven_source_list.append(indTarget_Driven_input)


    if Add_to_Existing_BS:
        FinalBS = Existing_BS[0]
        Existing_BS_Node_target_list = cmds.listAttr( FinalBS + ".w", k = True, m = True)
        print( Existing_BS_Node_target_list )
    else:
        if len(NewBSName) < 1:
            FinalBS = Create_BS(Target_Geo, Target_Geo + "_BS")
        else:
            FinalBS = Create_BS(Target_Geo, NewBSName)

    # if Subdivided_Transfer:
    #	 for indTarget in Duped_Target_Geo_list:
    #		 cmds.polySmooth( indTarget , constructionHistory = False, ost = 0, khe = 0, ps = 0.1, kmb = 1, bnr = 1, mth = 0,
    #						 suv = 1, peh = 0, ksb = 1, ro = 1, sdt = 2, ofc = 0, kt = 1, ovb = 1, dv = 1, ofb = 3, kb = 1,
    #						 c = 1, ocr = 0, dpe = 1, sl = 1)


    # Stright bs

    Targer_Index = 0
    if Add_to_Existing_BS:
        Targer_Index += len(Existing_BS_Node_target_list) + 2# increaseing after 2
    print (FinalBS)

    cmds.select(cl = 1)
    for indTargetindex in range(len(Duped_Target_Geo_list)):
        BypassUnuseful_target = True
        print("transfering : {Transfering} ".format(Transfering = BS_Node_target_list[indTargetindex] ))
        if BypassUnuseful_target:

            mismatch = Point_distance_Checker( Target_Geo , Duped_Target_Geo_list[indTargetindex] , 0.02 )
            if mismatch is False :
                print("below point distance check threshold , by passed ")
                continue

            Target_Geo_Shape = cmds.listRelatives( Target_Geo , shapes = True )[0]

            cmds.select(Duped_Target_Geo_list[indTargetindex])
            cmds.blendShape( FinalBS , e = 1, tc = True, w = (Targer_Index, 0),
                            t = ( Target_Geo , Targer_Index, Duped_Target_Geo_list[indTargetindex] + 'Shape', 1))

            cmds.aliasAttr(BS_Node_target_list[ indTargetindex ], FinalBS + '.w[' + str(Targer_Index) + ']')
        
        if Append_Driven:
            try:
                # cmds.connectAttr('LeftFoot_poseInterpolatorShape.output[3]', 'KHU_SOC_BS.LeftArm_0_0_30HULL_SUBED_0_0_0', f=1)

                cmds.connectAttr( driven_source_list[indTargetindex] , FinalBS + "." + BS_Node_target_list[ indTargetindex ], f=1)
            except:
                print ( " connectAttr Failed : " + driven_source_list[indTargetindex] +" ------------- "+  FinalBS + "." + BS_Node_target_list[ indTargetindex ] )

        Targer_Index += 1
        cmds.select(cl = 1)

    # clean up
    print ("===================================================")
    return
    print (WarpNode)
    cmds.delete(WarpNode)
    cmds.delete(Target_Geo_Transfer_Ready)
    # cmds.delete(Duplicated_Wrap_Src)
    cmds.delete(Duped_Target_Geo_list)

# From PSD_Point_Snap_GUI_2
# removed AxisLimit input
def SnapToPointBatch_Fullgeo( inputgeoA, inputgeoB, WorldSpace, threshold, VP_Refresh ):
    ptnum = cmds.polyEvaluate(inputgeoA)['vertex']
    cmds.cycleCheck(e = False)
    point_counter = 0
    if WorldSpace:
        for i in range(ptnum):
            Pointid = i

            VPosA = cmds.xform(inputgeoA + '.vtx[' + str(Pointid) + ']', query = 1, worldSpace = 1, translation = 1)
            VPosB = cmds.xform(inputgeoB + '.vtx[' + str(Pointid) + ']', query = 1, worldSpace = 1, translation = 1)
            movedistant = []
            movedistant.append(VPosB[0] - VPosA[0])
            movedistant.append(VPosB[1] - VPosA[1])
            movedistant.append(VPosB[2] - VPosA[2])

            if DistanceMethod_Full(movedistant, threshold):
                continue
            point_counter += 1

            cmds.move(VPosB[0], VPosB[1], VPosB[2], (inputgeoA + '.vtx[' + str(Pointid) + ']'), worldSpace = 1, a = 1)
            if VP_Refresh:
                cmds.refresh()
    else:

        for i in range(ptnum):
            Pointid = i

            VPosA = cmds.xform(inputgeoA + '.vtx[' + str(Pointid) + ']', query = 1, objectSpace = 1, translation = 1)
            VPosB = cmds.xform(inputgeoB + '.vtx[' + str(Pointid) + ']', query = 1, objectSpace = 1, translation = 1)
            movedistant = []
            movedistant.append(VPosB[0] - VPosA[0])
            movedistant.append(VPosB[1] - VPosA[1])
            movedistant.append(VPosB[2] - VPosA[2])

            if DistanceMethod_Full(movedistant, threshold):
                continue
            point_counter += 1

            cmds.move(movedistant[0], movedistant[1], movedistant[2], (inputgeoA + '.vtx[' + str(Pointid) + ']'),
                      objectSpace = 1, r = 1)
            if VP_Refresh:
                cmds.refresh()

    cmds.cycleCheck(e = True)
    print(str(point_counter) + " point Snap to the Target position")


def SnapToPointBatch_Selected_Points_only( inputgeoA, inputgeoB, PointList, WorldSpace, threshold, VP_Refresh ):
    cmds.cycleCheck(e = False)
    point_counter = 0
    if WorldSpace:
        for i in PointList:
            Pointid = int(i[:-1].split("[")[1])

            VPosA = cmds.xform(inputgeoA + '.vtx[' + str(Pointid) + ']', query = 1, worldSpace = 1, translation = 1)
            VPosB = cmds.xform(inputgeoB + '.vtx[' + str(Pointid) + ']', query = 1, worldSpace = 1, translation = 1)
            movedistant = []
            movedistant.append(VPosB[0] - VPosA[0])
            movedistant.append(VPosB[1] - VPosA[1])
            movedistant.append(VPosB[2] - VPosA[2])

            if DistanceMethod_Full(movedistant, threshold):
                continue
            point_counter += 1

            cmds.move(VPosB[0], VPosB[1], VPosB[2], (inputgeoA + '.vtx[' + str(Pointid) + ']'), worldSpace = 1, a = 1)
            if VP_Refresh:
                cmds.refresh()
    else:

        for i in PointList:
            Pointid = int(i[:-1].split("[")[1])

            VPosA = cmds.xform(inputgeoA + '.vtx[' + str(Pointid) + ']', query = 1, objectSpace = 1, translation = 1)
            VPosB = cmds.xform(inputgeoB + '.vtx[' + str(Pointid) + ']', query = 1, objectSpace = 1, translation = 1)
            movedistant = []
            movedistant.append(VPosB[0] - VPosA[0])
            movedistant.append(VPosB[1] - VPosA[1])
            movedistant.append(VPosB[2] - VPosA[2])

            if DistanceMethod_Full(movedistant, threshold):
                continue
            point_counter += 1

            cmds.move(movedistant[0], movedistant[1], movedistant[2], (inputgeoA + '.vtx[' + str(Pointid) + ']'),
                      objectSpace = 1, r = 1)
            if VP_Refresh:
                cmds.refresh()

    cmds.cycleCheck(e = True)
    print(str(point_counter) + " point Snap to the Target position")


def DistanceMethod_Simplify( movedistant, threshold ):
    if abs(movedistant[0]) < threshold:
        if abs(movedistant[1]) < threshold:
            if abs(movedistant[2]) < threshold:
                return False
    return True


def DistanceMethod_Full( movedistant, threshold ):
    dx = movedistant[0]
    dy = movedistant[1]
    dz = movedistant[2]
    Distance = dx * dx + dy * dy + dz * dz
    if Distance > (threshold * threshold * threshold):
        return False
    else:
        return True

global Question_Window_image_path
Question_Window_image_path = os.path.join(os.path.dirname(__file__), 'Question_BlendShape_Transfer')
BlendShape_Transfer_GUI()
