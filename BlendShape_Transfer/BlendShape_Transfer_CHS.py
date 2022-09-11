# -!- coding: utf-8 -!-
# Author  : AWACS
# Time  : 2022/9/10
# version : 0.56 beta

import maya.cmds as cmds
import os

# def Question_Button( COMMAND = None , blank_space = 1 ,  btn_label = " ? " ):
#     cmds.text( l= " " ,w = blank_space )
#     cmds.button( c=lambda *args: eval( COMMAND ) , l= btn_label , w=20 )

# def Question_Window( imageNum = 0 , Window_name = 'Question_Window' , w = 540 , h = 540):
#     if cmds.window( Window_name , q=1, ex=1 ):
#         cmds.deleteUI( Window_name )
#     cmds.window( Window_name )
#     #cmds.dockControl( area='left', content=myWindow, allowedArea=allowedAreas )
#     imagelist = ["Question_BlendShape_Transfer_1.jpg" ,
#                  "Question_BlendShape_Transfer_2.jpg" ,
#                  "Question_BlendShape_Transfer_3.jpg" ,
#                  "Question_BlendShape_Transfer_4.jpg" ,
#                  "Question_BlendShape_Transfer_5.jpg" ,
#                  ]
#     print ( Question_Window_image_path +  "/" + imagelist[ imageNum ] )
#     cmds.paneLayout()
#     cmds.image( image= Question_Window_image_path +  "/" + imagelist[ imageNum ] )

#     cmds.showWindow( Window_name )

def BlendShape_Transfer_GUI():
    if cmds.window('BlendShape_Transfer', q = 1, ex = 1):
        cmds.deleteUI('BlendShape_Transfer')

    cmds.window('BlendShape_Transfer')
    cmds.showWindow('BlendShape_Transfer')
    cmds.columnLayout()

    textwidth = 300

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 1: ")
    cmds.text(label = u"传递方式 : ", w = textwidth, align = "right")
    cmds.optionMenu( "Transfer_Method" , w = 180 )
    cmds.menuItem( label='Wrap deformer' )
    cmds.menuItem( label=u'目前别的还没写出来咕咕咕' )
    # Question_Button("Question_Window( 0 )", 10)
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 2: ")
    cmds.text(label = u"选择原模型 ( 带有原先BS的模型 ) :  ", w = textwidth, align = "right")
    cmds.textField('Input_Source_Mesh', w = 140, h = 24, text = "")
    cmds.button(c = lambda *args: Set_Source_Geo(), label = u"确认", w = 50)
    # Question_Button("Question_Window( 0 )", 10)
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 3: ")
    cmds.text(label = u"选择新模型 ( 你要传递到的BS的模型 ) :  ", w = textwidth, align = "right")
    cmds.textField('Input_Target_Mesh', w = 140, h = 24, text = "")
    cmds.button(c = lambda *args: Set_Target_Geo(), label = u"确认", w = 50)
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 4: ")
    cmds.text(label = u"选定BS节点 (如未选定，会尝试自动查找模型已有BS节点):  ", w = textwidth, align = "right")
    cmds.textField('InputBS', w = 140, h = 24, text = "")
    cmds.button(c = lambda *args: Set_Source_BS(), label = u"确认", w = 50)
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 5: ")
    cmds.text(label = u" 新的BS的名称 :  ", w = textwidth, align = "right")
    cmds.textField('New_BS_Name', w = 180, h = 24, text = "BS_Transfered")
    cmds.setParent('..')

    cmds.rowLayout(nc = 6)
    cmds.text(label = " 6: ")
    # cmds.text(label = "Add to Existing Blendshape Node : ", w = 140)
    
    cmds.checkBox( "Add_to_exist_BS" , l = u"添加到现有BS节点：  ", value = False, w = textwidth, align = "right")
    # cmds.text(label = " Existing_BS :  " ,w = 80)
    cmds.textField('Existing_BS', w = 140, h = 24, text = "")
    cmds.button(c = lambda *args: Set_Existing_BS(), label = u"确认", w = 50)
    cmds.setParent('..')

    # cmds.rowLayout(nc = 6)
    # cmds.text(label = " 6: ")
    # cmds.text(label = "Distant threshold : ")
    # cmds.floatField("Distant_threshold", max = 0.1, min = 0.0, value = 0.002)
    # cmds.setParent('..')
    cmds.rowLayout(nc = 6)
    cmds.text(label = " 7: ")
    # cmds.text(label = "Add to Existing Blendshape Node : ", w = 140)
    
    cmds.checkBox( "Append_Driven" , l =u"自动链接驱动属性", value = False, w = textwidth, align = "right")
    # cmds.text(label = " Existing_BS :  " ,w = 80)
    cmds.setParent('..')


    cmds.rowLayout(nc = 6)
    cmds.text(label = " 8: ")
    cmds.button(c = lambda *args: ExecuteTransferBS(), label = u"执行 BlendShape Transfer ", w = 180)
    cmds.setParent('..')


    cmds.rowLayout(nc = 6)
    cmds.text(label = u" 注意 : 模型的Scale(尺寸) X,Y,Z 最好冻结到 1.0 ")
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
    if Selection:
        if Object_Type_Checker(Selection[0], "mesh"):
            cmds.textField('Input_Source_Mesh', e = 1, tx = Selection[0])
            print (u"//// 原模型已选 : " + Selection[0])
        else:
            print (u"//// 错误的选择 , 请选择个多边形网格 ")
    else:
        print(u"//// 选择是空的")

def Set_Target_Geo():
    Selection = cmds.ls(selection = True)
    if Selection:
        if Object_Type_Checker(Selection[0], "mesh"):
            cmds.textField('Input_Target_Mesh', e = 1, tx = Selection[0])
            print (u"//// 目标模型已选 : " + Selection[0])
        else:
            print (u"//// 错误的选择 , 请选择个多边形网格 ")
    else:
        print(u"//// 选择是空的")

def Set_Source_BS():
    Selection = cmds.ls(selection = True)
    if Selection:
        Source_BS_list = []
        for indSel in Selection:
            if Object_Type_Checker(indSel, "blendShape"):
                Source_BS_list.append(indSel)
        print (Source_BS_list)
        if len(Source_BS_list) < 1:
            print (u"//// 错误的选择 , 请选择至少一个blendShape节点 ")
        else:
            BS_Display = ""
            for indBS in Source_BS_list:
                BS_Display += indBS
                BS_Display += " "
            cmds.textField('InputBS', e = 1, tx = BS_Display)
            print (u"//// blendShape节点已选 : " +BS_Display)
    else:
        cmds.textField('InputBS', e = 1, tx = None)
        print ("//// 原BlendShape未选定,执行时我会试图找到链接了的现有Blendshape ")

def Set_Existing_BS(  ):
    Selection = cmds.ls(selection = True)
    if Selection:
        if Object_Type_Checker(Selection[0], "blendShape"):
            cmds.textField('Existing_BS', e = 1, tx = Selection[0])
            print (u"//// blendShape节点已选 : " + Selection[0])
        else:
            print (u"//// 错误的选择 , 请选择现有的目标blendShape节点 ")
    else:
        print(u"//// 选择是空的")

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
        SearchResult = list(set(SearchResult))
        print( InputNode + u" blendShape节点查找结果 : " + str(SearchResult) )
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

    if Add_to_Exist_BS:
        if len(Existing_BS) < 1 :
            Existing_BS = SearchingForBlendshape(Target_Geo)

    if Existing_BS is None :
        Add_to_Exist_BS = False

    if len(Source_BS_Text) > 0:
        Source_BS = Source_BS_Text.split(" ")
    else:
        Source_BS = SearchingForBlendshape(Source_Geo)

    print(Source_BS)

    if Source_BS:
        for IndSrcBS in Source_BS:
            if IndSrcBS == "" :
                continue
            if len(IndSrcBS) > 0 :
                print((Source_Geo, IndSrcBS, Target_Geo, Add_to_Exist_BS , Existing_BS , False, Append_Driven ,NewBSName))
                BlendShape_Transfer_Main(Source_Geo, IndSrcBS, Target_Geo, Add_to_Exist_BS , Existing_BS , False, Append_Driven ,NewBSName)
            else:
                print( u"没有找的blendShape节点 , 请手动选择blendShape节点并确认" )

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
    for indBS_Node_target in BS_Node_target_list:
        try:
            cmds.setAttr(BSNode + '.' + indBS_Node_target, 0)
        except:
            print( "Initialize BS Func Failed , Failed to set 0 at ------" + BSNode + '.' + indBS_Node_target)


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

def BlendShape_Transfer_Main( Source_Geo, BS_Node, Target_Geo, Add_to_Existing_BS, Existing_BS,
                                           Subdivided_Transfer, Append_Driven , NewBSName = "BS_Transfered" ):
    # LowPolySrc , BS_of_LowPolySrc ):, HighPolyGeo , HighPoly_is_Extended , Transfer_Vertex , Transfer_Method , New_name_list ):
    # transfer the low Poly Mesh Blendshape to a Extended High Poly Mesh
    #=====================initialize===================
    BS_Node_target_list = cmds.listAttr(BS_Node + ".w", k = True, m = True)
    print (BS_Node_target_list)
    #=====================initialize===================


    # ----- recording input Connection of Source BS
    Target_input_Connections = {}
    for indTarget in BS_Node_target_list:
        indTarget_plugs = BS_Node + '.' + indTarget
        try:
            indTarget_Driven_input = cmds.listConnections( indTarget_plugs , plugs = True )[0]
            Target_input_Connections[indTarget] = indTarget_Driven_input
        except:
            Target_input_Connections[indTarget] = False

    # ----- disconnectAttr Source BS
    for indTarget , indInput_connection in Target_input_Connections.items():
        indTarget_plugs = BS_Node + '.' + indTarget
        if indInput_connection :
            try:
                cmds.disconnectAttr( indInput_connection , indTarget_plugs)
            except:
                print( u"未成功断开属性 ：  {} ---- {} ".format( indTarget_plugs , indInput_connection))

    Initialize_BS(BS_Node)

    #=====================initialize End===================

    #=====================Wraping Start===================
    #1first Duplicate a Target Geo
    Target_Geo_Transfer_Ready = cmds.duplicate(Target_Geo, n = Target_Geo + "_Temp_Transfer_Ready")[0]

    # ----------- duplicate entire Source geometry with upstreamNodes is safer ?
    # Duplicated_Wrap_Src = cmds.duplicate(Source_Geo, upstreamNodes = True , renameChildren = True )
    # Duplicated_Wrap_Src = [ Source_Geo ]


    Wrap_Src_Geo = Source_Geo
    Wrap_Src_BS = BS_Node

    WarpNode = Create_Wrap(Wrap_Src_Geo, Target_Geo_Transfer_Ready, "WarpNode_Temp_For_BS_Transfer", 0, 1.0, False, False, 0)


    # try update?????????????
    # there may be some issue about maya dont update deformer before first time executing duplicate command 
    cmds.setAttr(Wrap_Src_BS + '.' + indTarget, 1)
    Temp_duplicateFirst = cmds.duplicate( Target_Geo_Transfer_Ready, n = Target_Geo_Transfer_Ready + "_Temp_" + "duplicateFirst_" + indTarget)
    cmds.setAttr(Wrap_Src_BS + '.' + indTarget, 0)
    cmds.delete(Temp_duplicateFirst)
    # try update Finished ?????????????--------------


    # --------- get individual wrap result
    Duped_Target_Geo_list = []
    for indTarget in BS_Node_target_list:

        cmds.setAttr(Wrap_Src_BS + '.' + indTarget, 1)
        cmds.setAttr(Wrap_Src_BS + '.' + indTarget, 1)
        # cmds.setAttr(WarpNode + ".envelope", 0)
        # cmds.setAttr(WarpNode + ".envelope", 1)
        # cmds.refresh( f = 1 )
        # cmds.refresh( f = 1 )
        ind_tmp_BS_Target = cmds.duplicate( Target_Geo_Transfer_Ready, n = Target_Geo_Transfer_Ready + "_Temp_" + indTarget)


        Duped_Target_Geo_list.append(ind_tmp_BS_Target[0])
        cmds.setAttr(Wrap_Src_BS + '.' + indTarget, 0)

    # ----- reconnectAttr Source BS
    for indTarget , indInput_connection in Target_input_Connections.items():
        indTarget_plugs = Wrap_Src_BS + '.' + indTarget
        if indInput_connection :
            try:
                cmds.connectAttr( indInput_connection , indTarget_plugs , f=1)
            except:
                print( u"未成功链接属性 ：  {} ---- {} ".format( indTarget_plugs , indInput_connection))
                pass

    cmds.delete(WarpNode)
    cmds.delete(Target_Geo_Transfer_Ready)
    #=====================Wraping End===================
    #=====================Target BS setting up Start===================
    Target_Index = 0

    if Add_to_Existing_BS:
        FinalBS = Existing_BS[0]
        Existing_BS_Node_target_list = cmds.listAttr( FinalBS + ".w", k = True, m = True)
        print( Existing_BS_Node_target_list )
        # ----- increaseing after 2
        Target_Index += len(Existing_BS_Node_target_list) + 2
    else:
        if len(NewBSName) < 1:
            FinalBS = Create_BS(Target_Geo, Target_Geo + "_BS")
        else:
            FinalBS = Create_BS(Target_Geo, NewBSName)

    print (u"传递到Blendshape : Blendshape 名称 : {}".format (FinalBS) )
    #=====================Target BS setting up End===================
    
    #=====================Add Target to New BS Start===================
    cmds.select(cl = 1)
    for indTargetindex in range(len(Duped_Target_Geo_list)):
        print(u"传递中 : {} ".format( BS_Node_target_list[indTargetindex] ))
        ind_tmp_BS_Target = Duped_Target_Geo_list[indTargetindex]
        BypassUnuseful_target = False
        
        if BypassUnuseful_target:
            mismatch = Point_distance_Checker( Target_Geo , ind_tmp_BS_Target , 0.02 )
            if mismatch is False :
                print(u" 低于点距离检查阈值  , 跳过")
                continue

        Target_Geo_Shape = cmds.listRelatives( Target_Geo , shapes = True )[0]

        cmds.select( ind_tmp_BS_Target )
        cmds.blendShape( FinalBS , e = 1, tc = True, w = (Target_Index, 0),
                        t = ( Target_Geo , Target_Index, ind_tmp_BS_Target + 'Shape', 1))

        indTarget = BS_Node_target_list[ indTargetindex ]
        indTarget_name = indTarget
        try:
            cmds.aliasAttr(indTarget_name, FinalBS + '.w[' + str(Target_Index) + ']')
        except:
            print( u"有命名冲突！ : " + indTarget_name )
            indTarget_name = indTarget_name + '_Name_Conflict'
            cmds.aliasAttr(indTarget_name , FinalBS + '.w[' + str(Target_Index) + ']')
            
        #=====================Addend driven attr Start===================
        if Append_Driven:
            indTarget_plugs = FinalBS + '.' + indTarget
            if Target_input_Connections[ indTarget ] :
                try:
                    cmds.connectAttr( Target_input_Connections[ indTarget ] , indTarget_plugs , f=1)
                except:
                    print( u"未成功链接属性 ：  ---- {} ".format( Target_input_Connections[ indTarget ] , indTarget_plugs))
                    pass
        #=====================Addend driven attr End===================

        Target_Index += 1
        cmds.select(cl = 1)
    #=====================Add Target to New BS End ===================

    #===================== clean up ===================
    print (u"清理节点中 ===================================================")
    
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

# global Question_Window_image_path
# Question_Window_image_path = os.path.join(os.path.dirname(__file__), 'Question_BlendShape_Transfer')
BlendShape_Transfer_GUI()
