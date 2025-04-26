from starlette_admin.contrib.sqlmodel import ModelView
from starlette_admin.exceptions import FormValidationError
from starlette.requests import Request
from typing import Any, Dict
from starlette.responses import JSONResponse, RedirectResponse
from sqlalchemy import func, select
from starlette_admin import action, CustomView
from typing import Any
from starlette.templating import Jinja2Templates
from starlette.datastructures import FormData
from starlette.requests import Request

from starlette_admin._types import RowActionsDisplayType
from starlette_admin.actions import link_row_action, row_action
from starlette_admin.contrib.sqla import ModelView
from starlette_admin.exceptions import ActionFailed
from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import PlainTextResponse
import json
import httpx
from typing import Any

# from app.sqla.models import Client, SymptomThreshold, CycleInfo, Greenhouse, EnvData, Feedback, SensorRange, DiseaseData, BucketValues, PlantWeek, Observation, Grid, GridAnalysis, FeedBackGridImages, Weeks

from app.sqla.models import Client

class ClientView(ModelView):
    row_actions = ["view", "edit", "make_published", "delete"]
    row_actions_display_type = RowActionsDisplayType.ICON_LIST
    page_size = 10

    fields = [
        "id", "client_name", "username", "password", "site_name", "greenhouse_name"
    ]

    searchable_fields = ["client_name", "username"]
    sortable_fields = ["id", "client_name"]
    exclude_fields_from_edit = ["client_name", "username", "password", "site_name", "greenhouse_name"]

    @row_action(
        name="make_published",
        text="Mark as published",
        confirmation="Edit Greenhouses of clients",
        icon_class="fas fa-check-circle",
        submit_btn_text="Yes, proceed",
        submit_btn_class="btn-success",
        action_btn_class="btn-info",
        form="""
        <style>
    .modal-footer button[data-bs-dismiss="modal"] {
        display: none !important;
    }
</style>

                <!-- Greenhouse Manager Content -->
<div id="manager-content" class="feature-content active card p-4">
    <form id="clientSelectForm">
        <div class="form-group mb-3">
            <label for="clientSelect" class="form-label">Select Client:</label>
            <div class="d-flex align-items-center">
                <select id="clientSelect" name="client" class="form-select me-2">
                    <!-- Options will be populated dynamically -->
                </select>
                <button type="submit" class="btn btn-primary">Load Greenhouses</button>
            </div>
        </div>
    </form>

    <form id="greenhouseForm" class="mt-4" style="display:none;">
        <div id="greenhouseFields" class="mb-4"></div>

        <h3 class="mb-3">Add New Greenhouse</h3>
        <div class="new-greenhouse row g-3 mb-3">
            <div class="col-md-4">
                <input type="text" id="newKey" placeholder="Key" class="form-control">
            </div>
            <div class="col-md-4">
                <input type="text" id="newValue" placeholder="Name" class="form-control">
            </div>
            <div class="col-md-4">
                <button type="button" onclick="addNewGreenhouse()" class="btn btn-success">Add</button>
            </div>
        </div>

        <button type="submit" class="btn btn-primary mt-3">Save Changes</button>
        
    </form>
    <button class="btn btn-primary mt-3" onclick="window.location.reload()">Close</button>
</div>
        <script>
        // Function to dynamically add greenhouse fields (placeholder for your implementation)
        function addNewGreenhouse() {
            var newKey = document.getElementById('newKey').value;
            var newValue = document.getElementById('newValue').value;
            
            if (newKey && newValue) {
                var greenhouseFields = document.getElementById('greenhouseFields');
                var entryDiv = document.createElement('div');
                entryDiv.className = 'greenhouse-entry';
                
                entryDiv.innerHTML = `
                    <input type="text" value="${newKey}" readonly style="width: 40%;">
                    <input type="text" value="${newValue}" style="width: 50%;">
                    <button type="button" class="secondary" onclick="this.parentElement.remove()">Remove</button>
                `;
                
                greenhouseFields.appendChild(entryDiv);
                
                // Clear input fields
                document.getElementById('newKey').value = '';
                document.getElementById('newValue').value = '';
            }
        }
        
        // This is where your original script would go
        // ...some script...
        var clientSelect = document.getElementById('clientSelect');
        var clientSelectForm = document.getElementById('clientSelectForm');
        var greenhouseForm = document.getElementById('greenhouseForm');
        var greenhouseFields = document.getElementById('greenhouseFields');

        let currentClient = null;
        let greenhouseData = {};

        async function fetchClients() {
            var res = await fetch('/clients');
            var clients = await res.json();
            clients.forEach(client => {
                console.log(clients);
                console.log(client);
                var option = document.createElement('option');
                option.value = client;
                option.textContent = client;
                clientSelect.appendChild(option);
            });
        }

        clientSelectForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            currentClient = clientSelect.value;
            var res = await fetch(`/get-greenhouses?client_name=${currentClient}`);
            greenhouseData = await res.json();
            greenhouseForm.style.display = 'block';
            renderFields();
        });

        function renderFields() {
    greenhouseFields.innerHTML = '';

    var data = greenhouseData[0]; // access the object inside the array

    for (var key in data) {
        var input = document.createElement('input');
        input.name = key;
        input.value = data[key];
        input.placeholder = key;
        input.className = 'form-control';
        greenhouseFields.appendChild(document.createTextNode(`${key}: `));
        greenhouseFields.appendChild(input);
        greenhouseFields.appendChild(document.createElement('br'));
    }
}


function addNewGreenhouse() {
    var key = document.getElementById('newKey').value;
    var value = document.getElementById('newValue').value;

    if (key && value) {
        greenhouseData[0][key] = value; // update the object inside the array
        renderFields();
        document.getElementById('newKey').value = '';
        document.getElementById('newValue').value = '';
    }
}


greenhouseForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    var formData = new FormData(greenhouseForm);
    var updatedData = {};

    for (var [key, value] of formData.entries()) {
        updatedData[key] = value;
    }

    var res = await fetch('/update-greenhouses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            client_name: currentClient,
            greenhouses: [updatedData]  // wrap it back into an array
        })
    });

    var result = await res.json();
    alert(result.message);
});


        fetchClients();
    </script>
        """,
    )
    async def make_published_row_action(self, request: Request, pk: Any) -> str:
        # Write your logic here

        data: FormData = await request.form()
        user_input = data.get("example-text-input")

        if ...:
            # Display meaningfully error
            raise ActionFailed("Sorry, We can't proceed this action now.")
        # Display successfully message
        return "The article was successfully marked as published"

    

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

class HomeView(CustomView):
    async def render(self, request: Request, templates: Jinja2Templates) -> Response:

        return templates.TemplateResponse(
            "home.html", {"request": request}
        )