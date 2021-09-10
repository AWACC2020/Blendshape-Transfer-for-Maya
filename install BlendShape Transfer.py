# Author  : AWACS
# Time    : 2020/08/15

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

def MayaDropinstall():
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


    ContainPath = os.path.join(os.path.dirname(__file__), dic_script["Contain_Folder"])

    if not os.path.exists(ContainPath):
        raise IOError('Cannot find ' + ContainPath)

    User_script_dir =  cmds.internalVar(userScriptDir=1)
    author_folder_dir = os.path.join( User_script_dir , dic_script['author_folder'])

    try:
        os.makedirs( author_folder_dir )
    except:
        # author_folder_dir Already exist
        pass

    # Script_folder_fullpath = os.path.join( author_folder_dir , dic_script["Script_folder"] )
    Script_folder_fullpath =  author_folder_dir +"/"+ dic_script["Script_folder"] 
    # print (Script_folder_fullpath)
    # Script_folder_fullpath = os.path.normpath(Script_folder_fullpath)
    # print (Script_folder_fullpath)    
    # print ("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    # Script_folder_fullpath = os.path.normpath(Script_folder_fullpath)
    # print (Script_folder_fullpath)

    if os.path.isdir( Script_folder_fullpath ):
        print ( str( Script_folder_fullpath ) + " is Already Exist " + " -------------reinstalling")
        shutil.rmtree( Script_folder_fullpath )
    else :
        pass
    #Create Script folder and copy Contains from contain Folder 
    shutil.copytree( ContainPath , Script_folder_fullpath )

    print ('// install success')
    if dic_script["Script_Shelf_icon"]:
        iconPath = os.path.join(Script_folder_fullpath, dic_script["Script_Shelf_icon"])
        iconPath = os.path.normpath(iconPath)
        # module_name = "BlendShape_Transfer"
    else:
        iconPath = "commandButton.png"

    command = '''import sys
script_path = "{path}"
if script_path not in sys.path:
    sys.path.append(script_path)
import {module_name}
if sys.version_info.major > 2 :
    from imp import reload
reload ({module_name})
'''.format(path=Script_folder_fullpath , module_name = dic_script["Script_module_import"] )

    shelf = maya.mel.eval('$gShelfTopLevel=$gShelfTopLevel')
    parent = cmds.tabLayout(shelf, query=True, selectTab=True)
    cmds.shelfButton(
        command=command,
        annotation=dic_script["Script_annotation"] ,
        sourceType='Python',
        image=iconPath,
        image1=iconPath,
        imageOverlayLabel = dic_script["imageOverlayLabel"],
        parent=parent
    )

    print("// {Script_name} has been added to current shelf".format( Script_name = dic_script["Script_name"]))


if isMaya:
    MayaDropinstall()
