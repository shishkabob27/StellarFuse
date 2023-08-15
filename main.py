import dearpygui.dearpygui as dpg
import json
import os

project = {'name': 'No Project Loaded'}

def isProject():
    if project['name'] == 'No Project Loaded':
        return False
    return True
    

def NewProject():
    project['name'] = "New Project"
    project['frames'] = []
    reloadProperties()
    
def NewFrame():
    project['frames'].append({'name': 'New Frame', 'events': []})


def OpenProject():
     with dpg.file_dialog(label="Open", width=640, height=400, callback=lambda sender, data: LoadProject(dpg.get_value(sender))):
        dpg.add_file_extension(".sfp", color=(255, 255, 0, 255))
        dpg.add_file_extension(".*", color=(255, 255, 255, 255))
        
def LoadProject(path):
    if path == "":
        return
    with open(path) as f:
        project.update(json.load(f))
        reloadProperties()
        
def SaveProject():
    with dpg.file_dialog(label="Save", width=640, height=400, callback=lambda sender, data: SaveProjectAs(dpg.get_value(sender))):
        dpg.add_file_extension(".sfp", color=(255, 255, 0, 255))
        
def SaveProjectAs(path):
    if path == "":
        return
    with open(path, 'w') as f:
        json.dump(project, f)
        reloadProperties()

def reloadProperties():
    dpg.set_value("properties_name", project['name'])
    
    #add tree nodes in workspace tree node
    for frame in project['frames']:
        dpg.add_tree_node(label=frame['name'], parent="Workspace Tree")

dpg.create_context()

with dpg.window(tag="Primary Window"):
    #menu bar
    with dpg.menu_bar():
        #file menu
        with dpg.menu(label="File"):
            #file menu items
            dpg.add_menu_item(label="New", callback=NewProject)
            dpg.add_menu_item(label="Open", callback=OpenProject)
            dpg.add_menu_item(label="Save", callback=SaveProject)
            dpg.add_menu_item(label="Exit", callback=dpg.stop_dearpygui)
            
        with dpg.menu(label="Insert"):
            dpg.add_menu_item(label="New Frame")
            pass
            
    #workspace
    with dpg.window(label="Workspace", id="Workspace", width=800, height=500, no_close=True):
        #tabs
        with dpg.tab_bar():
            #tab 1
            with dpg.tab(label="Frame Editor"):
                with dpg.plot(height=-1, width=-1):
                    dpg.add_plot_legend()
                    xaxis = dpg.add_plot_axis(dpg.mvXAxis, label="x")
                    with dpg.plot_axis(dpg.mvYAxis, label="y axis"):
                        dpg.fit_axis_data(dpg.top_container_stack())
                    dpg.fit_axis_data(xaxis)
                pass
            with dpg.tab(label="Event Editor"):
                pass

    with dpg.window(label="Workspace Toolbar", id="Workspace Toolbar", width=200, height=400, no_close=True):
            with dpg.tree_node(label="", id="Workspace Tree"):
                pass
            
    with dpg.window(label="Properties", id="Properties", width=200, height=400, no_close=True):
        dpg.add_text("Name")
        dpg.add_input_text(label="##Name", id="properties_name", default_value=project['name'], callback=lambda sender, data: project.update({'name': dpg.get_value("properties_name")}))
    
                
        
dpg.create_viewport(title='StellarFuse', width=1920, height=1080)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)

while dpg.is_dearpygui_running():

    if isProject():
        dpg.set_viewport_title("StellarFuse - " + project['name'])
        dpg.set_item_label("Workspace Tree", project['name'])
        dpg.show_item("Workspace")
        dpg.show_item("Workspace Toolbar")
        dpg.show_item("Properties")
    else:
        #hide workspace toolbar
        dpg.hide_item("Workspace")
        dpg.hide_item("Workspace Toolbar")
        dpg.hide_item("Properties")
        dpg.set_viewport_title("StellarFuse")
        
        
        
    dpg.render_dearpygui_frame()
    
dpg.destroy_context()