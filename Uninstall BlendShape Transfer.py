# Author  : AWACS
# Time    : 2020/09/03

import os
import shutil

try:
    import maya.mel
    import maya.cmds as cmds
    isMaya = True
except ImportError:
    isMaya = False

def onMayaDroppedPythonFile(*args, **kwargs):
    pass

def MayaDropRemove():
    """Drag and drop this file into the scene executes the file."""
    dic_script = {
        "author_folder" : "AWACS",
        "Contain_Folder" : "BlendShape_Transfer",
        "Script_folder" : "BlendShape_Transfer",
        "Script_module_import" : "BlendShape_Transfer",

        "Script_name" : "BlendShape_Transfer",
        "Script_Shelf_icon" : None ,
        "imageOverlayLabel":"BsTransfer",
        "Script_annotation" : 
        "Transfer Blendshape between meshes with different topology",
    }
    Popup_Dialog = True

    User_script_dir =  cmds.internalVar(userScriptDir=1)
    author_folder_dir = os.path.join( User_script_dir , dic_script["author_folder"])

    Script_folder_fullpath = os.path.join( author_folder_dir , dic_script["Script_folder"])

    if os.path.isdir( Script_folder_fullpath ):
        shutil.rmtree( Script_folder_fullpath )
        confirmDialog_message = "{Script_name} has been Removed From your software, \
you can remove the command from shelf now".format( Script_name = dic_script["Script_name"])
        print (confirmDialog_message)
        if Popup_Dialog:
            cmds.confirmDialog( title='Uninstall Success', message=confirmDialog_message, button=['OK'] )
    else :
        confirmDialog_message = "No such path , Nothing good to remove or unistall or whatever"
        print (confirmDialog_message)
        if Popup_Dialog:
            
            cmds.confirmDialog( title='Uninstall Failed', message=confirmDialog_message, button=['OK']  )
        return

    # check if there is any thing ,if not remove entire author_folder
    # print (os.listdir ( author_folder_dir ) )
    if len( os.listdir ( author_folder_dir ) ) < 1:
        shutil.rmtree( author_folder_dir )




if isMaya:
    MayaDropRemove()
