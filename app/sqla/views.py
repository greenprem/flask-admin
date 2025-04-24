from starlette_admin.contrib.sqlmodel import ModelView
from starlette_admin.exceptions import FormValidationError
from starlette.requests import Request
from typing import Any, Dict
from starlette.responses import JSONResponse, RedirectResponse
from sqlalchemy import func, select
from starlette_admin import action
from typing import Any

from starlette.datastructures import FormData
from starlette.requests import Request

from starlette_admin._types import RowActionsDisplayType
from starlette_admin.actions import link_row_action, row_action
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import ActionFailed
from starlette.requests import Request
from starlette.responses import PlainTextResponse
import json
import httpx
from typing import Any

# from app.sqla.models import Client, SymptomThreshold, CycleInfo, Greenhouse, EnvData, Feedback, SensorRange, DiseaseData, BucketValues, PlantWeek, Observation, Grid, GridAnalysis, FeedBackGridImages, Weeks

from app.sqla.models import Client

class ClientView(ModelView):
    row_actions = ["view", "edit", "edit_greenhouse", "delete"]
    row_actions_display_type = RowActionsDisplayType.ICON_LIST
    page_size = 10

    fields = [
        "id", "client_name", "username", "password", "site_name", "greenhouse_name"
    ]

    searchable_fields = ["client_name", "username"]
    sortable_fields = ["id", "client_name"]
    exclude_fields_from_edit = ["client_name", "username", "password", "site_name", "greenhouse_name"]

    @row_action(
        name="edit_greenhouse",
        text="Edit Greenhouse",
        confirmation=None,  # Removed confirmation as we'll use the form directly
        icon_class="fas fa-leaf",  # Changed to a greenhouse-like icon
        submit_btn_text="Save Changes",
        submit_btn_class="btn-success",
        action_btn_class="btn-info",
        form="""
        <div>
            <h4>Greenhouse Manager for <span id="current-client"></span></h4>
            
            <div id="greenhouseFields" class="mb-3">
                <!-- Greenhouse fields will be dynamically populated here -->
            </div>
            
            <div class="mt-3 mb-3">
                <h5>Add New Field</h5>
                <div class="input-group mb-3">
                    <input type="text" class="form-control" id="newKey" name="newKey" placeholder="Field Name">
                    <input type="text" class="form-control" id="newValue" name="newValue" placeholder="Value">
                    <button class="btn btn-outline-secondary" type="button" onclick="addNewGreenhouseField()">Add</button>
                </div>
            </div>

            <input type="hidden" id="greenhouseData" name="greenhouseData">
            
            <script>
                let greenhouseData = {};
                
                async function loadGreenhouseData() {
                    const clientName = document.getElementById('current-client').textContent;
                    const res = await fetch(`/get-greenhouses?client_name=${clientName}`);
                    greenhouseData = await res.json();
                    renderFields();
                }
                
                function renderFields() {
                    const fieldsContainer = document.getElementById('greenhouseFields');
                    fieldsContainer.innerHTML = '';
                    
                    const data = greenhouseData[0]; // access the object inside the array
                    
                    for (const key in data) {
                        const entryDiv = document.createElement('div');
                        entryDiv.className = 'input-group mb-2';
                        
                        entryDiv.innerHTML = `
                            <span class="input-group-text" style="width: 30%;">${key}</span>
                            <input type="text" class="form-control gh-field" data-key="${key}" value="${data[key]}" style="width: 60%;">
                            <button class="btn btn-outline-danger" type="button" onclick="removeField('${key}')">Remove</button>
                        `;
                        
                        fieldsContainer.appendChild(entryDiv);
                    }
                    
                    // Update hidden field with current data
                    document.getElementById('greenhouseData').value = JSON.stringify(greenhouseData);
                }
                
                function addNewGreenhouseField() {
                    const key = document.getElementById('newKey').value;
                    const value = document.getElementById('newValue').value;
                    
                    if (key && value) {
                        greenhouseData[0][key] = value;
                        renderFields();
                        document.getElementById('newKey').value = '';
                        document.getElementById('newValue').value = '';
                    }
                }
                
                function removeField(key) {
                    delete greenhouseData[0][key];
                    renderFields();
                }
                
                // Update data when any field changes
                document.addEventListener('change', function(e) {
                    if (e.target.classList.contains('gh-field')) {
                        const key = e.target.dataset.key;
                        greenhouseData[0][key] = e.target.value;
                        document.getElementById('greenhouseData').value = JSON.stringify(greenhouseData);
                    }
                });
                
                // Set the client name and load data when the form opens
                document.addEventListener('DOMContentLoaded', function() {
                    setTimeout(loadGreenhouseData, 500); // Give a moment for the form to initialize
                });
            </script>
        </div>
        """,
    )
    async def edit_greenhouse_row_action(self, request: Request, pk: Any) -> str:
        try:
            # Get the client record first
            client = await self.find_by_pk(request, pk)
            
            # Set the current client name in the response context
            response = PlainTextResponse(f"""
                <script>
                    document.getElementById('current-client').textContent = '{client.client_name}';
                </script>
            """)
            
            # Process form submission
            if request.method == "POST":
                data = await request.form()
                greenhouse_data = json.loads(data.get("greenhouseData", "{}"))
                
                # Call your greenhouse update endpoint/function
                await update_greenhouses(client.client_name, greenhouse_data)
                
                return "Greenhouse data successfully updated!"
            
            return response
            
        except Exception as e:
            raise ActionFailed(f"Error updating greenhouse: {str(e)}")

# Helper function to update greenhouses (implement based on your backend)
async def update_greenhouses(client_name, greenhouse_data):
    # Make API call or database update as needed
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "/update-greenhouses",
            json={
                "client_name": client_name,
                "greenhouses": greenhouse_data
            }
        )
        if response.status_code != 200:
            raise Exception(f"Failed to update: {response.text}")

    

# class SymptomThresholdView(ModelView):
#     page_size = 10
#     fields = ["id", "disease", "val"]
#     searchable_fields = [SymptomThreshold.disease]
#     sortable_fields = [SymptomThreshold.id, SymptomThreshold.disease]

class CycleInfoView(ModelView):
    page_size = 10
    fields = [
        "id", "client_name", "site", "greenhouse", "name",
        "date_date", "startdate_date", "observationPending",
        "comparedTo", "reportwriting"
    ]
    exclude_fields_from_edit = ["client_name", "site", "greenhouse"]



class EnvDataView(ModelView):
    page_size = 10
    fields = [
        "id", "client_name", "site", "greenhouse_id", "item_id",
        "date", "time", "json_data"
    ]
    exclude_fields_from_edit = ["client_name", "site", "greenhouse_id","item_id"]
# class FeedbackView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client_name", "selected_cycle", "selected_greenhouse",
#         "selected_grid", "selected_site", "message", "fileName",
#         "video_status", "video_url"
#     ]
#     searchable_fields = [Feedback.client_name, Feedback.selected_site]
#     sortable_fields = [Feedback.id, Feedback.video_status]

class SensorRangeView(ModelView):
    page_size = 10
    fields = [
        "id", "client", "greenhouse", "site",
        "temp_optimal", "humidity_risky", "ec_risky", "ph_risky"
    ]
    exclude_fields_from_edit = ["client_name", "site", "greenhouse"]

class DiseaseDataView(ModelView):
    page_size = 10
    fields = [
        "id", "location", "crop", "disease",
        "temp_range", "humid_range", "ec_range", "ph_range",
        "temp_range2", "humid_range2", "ec_range2", "ph_range2",
        "visual_symptom"
    ]
    exclude_fields_from_edit = ["location", "crop", "disease"]

class BucketValuesView(ModelView):
    page_size = 10
    fields = ["id", "client_name", "site", "greenhouse", "json_data", "flagarray"]
    exclude_fields_from_edit = ["client_name", "site", "greenhouse"]

class PlantWeekView(ModelView):
    page_size = 10
    fields = ["id", "client_name", "site", "greenhouse", "weekday"]
    exclude_fields_from_edit = ["client_name", "site", "greenhouse"]

class ObservationView(ModelView):
    page_size = 10
    fields = [
        "id", "client_name", "site", "greenhouse", "cycle_name",
        "comparison_cycle_name", "delta_t_id", "data", "message",
        "temp_optimal", "humidity_optimal", "ec_risky", "ph_risky",
        "copy", "env_data", "grid_data", "plant_data"
    ]
    exclude_fields_from_edit = ["client_name", "site", "greenhouse", "cycle_name"]
    
    
    
    # Define form fields for the action
    def get_actions(self):
        actions = super().get_actions()
        for action in actions:
            if action.name == "highest_copy":
                # Define form fields for this action
                action.form_fields = [
                    {
                        "name": "client_name",
                        "label": "Client Name",
                        "type": "select",
                        "options": [("", "-- Select Client --")],  # Will be populated dynamically
                        "required": False
                    },
                    {
                        "name": "site",
                        "label": "Site",
                        "type": "select",
                        "options": [("", "-- Select Site --")],  # Will be populated dynamically
                        "required": False
                    },
                    {
                        "name": "greenhouse",
                        "label": "Greenhouse",
                        "type": "select",
                        "options": [("", "-- Select Greenhouse --")],  # Will be populated dynamically
                        "required": False
                    },
                    {
                        "name": "cycle_name",
                        "label": "Cycle Name",
                        "type": "select",
                        "options": [("", "-- Select Cycle --")],  # Will be populated dynamically
                        "required": False
                    }
                ]
        return actions
    
    async def render_action_form(self, request, action_name):
        """Override to populate select options dynamically"""
        if action_name == "highest_copy":
            form = await super().render_action_form(request, action_name)
            
            # Populate options for selects
            async with self.context.get_session() as session:
                # Get client options
                result = await session.execute(select(self.model.client_name).distinct().order_by(self.model.client_name))
                client_options = [("", "-- Select Client --")] + [(c, c) for c in result.scalars().all() if c]
                
                # Get site options
                result = await session.execute(select(self.model.site).distinct().order_by(self.model.site))
                site_options = [("", "-- Select Site --")] + [(s, s) for s in result.scalars().all() if s]
                
                # Get greenhouse options
                result = await session.execute(select(self.model.greenhouse).distinct().order_by(self.model.greenhouse))
                greenhouse_options = [("", "-- Select Greenhouse --")] + [(g, g) for g in result.scalars().all() if g]
                
                # Get cycle options
                result = await session.execute(select(self.model.cycle_name).distinct().order_by(self.model.cycle_name))
                cycle_options = [("", "-- Select Cycle --")] + [(c, c) for c in result.scalars().all() if c]
            
            # Update options in form fields
            for field in form["fields"]:
                if field["name"] == "client_name":
                    field["options"] = client_options
                elif field["name"] == "site":
                    field["options"] = site_options
                elif field["name"] == "greenhouse":
                    field["options"] = greenhouse_options
                elif field["name"] == "cycle_name":
                    field["options"] = cycle_options
            
            return form
        return await super().render_action_form(request, action_name)
    
class GridView(ModelView):
    page_size = 10
    fields = [
        "id", "client_name", "selected_greenhouse",
        "selected_site", "grid_format"
    ]
    exclude_fields_from_edit = ["client_name", "selected_greenhouse", "selected_site"]

class GridAnalysisView(ModelView):
    page_size = 10
    fields = [
        "id", "client_name", "selected_greenhouse",
        "selected_site", "selected_cycle", "json_data"
    ]
    exclude_fields_from_edit = ["client_name", "selected_greenhouse", "selected_site", "selected_cycle"]

# class FeedBackGridImagesView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client_name", "selected_greenhouse",
#         "selected_site", "selected_cycle", "selected_grid",
#         "json_data"
#     ]
#     searchable_fields = [FeedBackGridImages.client_name]
#     sortable_fields = [FeedBackGridImages.id]

# class WeeksView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client_name", "selected_greenhouse", "selected_site",
#         "start_cycle", "end_cycle", "number"
#     ]
#     searchable_fields = [Weeks.client_name]
#     sortable_fields = [Weeks.id, Weeks.number]
