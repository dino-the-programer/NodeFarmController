from nicegui import app as nicegui_app, ui

workerListUI:dict = {}

@ui.refreshable
def worker_list_ui():
    if not workerListUI:
        ui.label('No workers connected.').classes('text-gray-400 italic')
        return
    
    ui.label(str(len(workerListUI)))
    with ui.column().classes('w-full border p-4'):
        for conn_id in workerListUI:
            with ui.row().classes('items-center justify-between w-full'):
                ui.label(f"Worker ID: {conn_id}").classes('font-bold')
                ui.label(f"Worker Email: {workerListUI[conn_id]}").classes('font-bold')
                ui.badge('Online', color='green')

@ui.page('/admindashboard', dark=True)
def show():
    heading = ui.label('Controller Dashboard')
    worker_list_ui()