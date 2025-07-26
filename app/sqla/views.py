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


class ActivitiesView(ModelView):
    page_size = 10
    fields = [
        "id", "client_name", "site", "greenhouse",
        "activity_type", "date", "time", "description"
    ]


    exclude_fields_from_edit = [
        "client_name", "site", "greenhouse"
    ]  # Optional: adjust according to your use case


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
        "id", "client", "greenhouse", "site", "location",
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

class UserManagementView(ModelView):
    """
    View for managing user credentials (username and password only).
    Client name is automatically set to match the username.
    """
    
    # Basic view configuration
    row_actions = ["view", "edit", "delete"]
    row_actions_display_type = RowActionsDisplayType.ICON_LIST
    page_size = 15
    
    # Only show username and password fields
    fields = ["id", "username", "password"]
    
    # Make fields searchable and sortable
    searchable_fields = ["username"]
    sortable_fields = ["id", "username"]
    
    # Don't allow editing of ID (auto-generated)
    exclude_fields_from_edit = ["id"]
    exclude_fields_from_create = ["id"]
    
    # Labels for better UX
    labels = {
        "username": "Username",
        "password": "Password"
    }
    
    async def create(self, request: Request, data: Dict[str, Any]) -> Any:
        """
        Override create method to automatically set client_name to username
        and provide default values for required JSON fields
        """
        # Set client_name to match username
        data["client_name"] = data.get("username", "")
        
        # Set default empty JSON arrays for required fields
        if "site_name" not in data:
            data["site_name"] = []
        if "greenhouse_name" not in data:
            data["greenhouse_name"] = []
            
        # Validate required fields
        if not data.get("username"):
            raise FormValidationError([
                {"loc": ["username"], "msg": "Username is required", "type": "value_error"}
            ])
        if not data.get("password"):
            raise FormValidationError([
                {"loc": ["password"], "msg": "Password is required", "type": "value_error"}
            ])
            
        # Check if username already exists
        async with self.session_maker() as session:
            existing_user = await session.execute(
                select(self.model).where(self.model.username == data["username"])
            )
            if existing_user.scalar_one_or_none():
                raise FormValidationError([
                    {"loc": ["username"], "msg": "Username already exists", "type": "value_error"}
                ])
        
        return await super().create(request, data)
    
    async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
        """
        Override edit method to automatically update client_name when username changes
        """
        # Set client_name to match username
        if "username" in data:
            data["client_name"] = data["username"]
            
            # Check if new username already exists (excluding current record)
            async with self.session_maker() as session:
                existing_user = await session.execute(
                    select(self.model).where(
                        self.model.username == data["username"],
                        self.model.id != pk
                    )
                )
                if existing_user.scalar_one_or_none():
                    raise FormValidationError([
                        {"loc": ["username"], "msg": "Username already exists", "type": "value_error"}
                    ])
        
        # Validate required fields
        if not data.get("username"):
            raise FormValidationError([
                {"loc": ["username"], "msg": "Username is required", "type": "value_error"}
            ])
        if not data.get("password"):
            raise FormValidationError([
                {"loc": ["password"], "msg": "Password is required", "type": "value_error"}
            ])
            
        return await super().edit(request, pk, data)
    
    def get_list_query(self):
        """
        Override to only show relevant columns in list view
        """
        query = super().get_list_query()
        return query
    
    async def serialize_field_value(self, value: Any, field: str) -> Any:
        """
        Override to handle password display (mask it for security)
        """
        if field == "password":
            # Mask password in list view for security
            return "*" * min(len(str(value)), 8) if value else ""
        return await super().serialize_field_value(value, field)
    
    @row_action(
        name="reset_password",
        text="Reset Password",
        confirmation="Are you sure you want to reset this user's password?",
        icon_class="fas fa-key",
        submit_btn_text="Reset Password",
        submit_btn_class="btn-warning",
        action_btn_class="btn-warning",
        form="""
        <div class="mb-3">
            <label for="new_password" class="form-label">New Password:</label>
            <input type="password" id="new_password" name="new_password" class="form-control" required>
        </div>
        <div class="mb-3">
            <label for="confirm_password" class="form-label">Confirm Password:</label>
            <input type="password" id="confirm_password" name="confirm_password" class="form-control" required>
        </div>
        <script>
            document.querySelector('form').addEventListener('submit', function(e) {
                var newPassword = document.getElementById('new_password').value;
                var confirmPassword = document.getElementById('confirm_password').value;
                
                if (newPassword !== confirmPassword) {
                    e.preventDefault();
                    alert('Passwords do not match!');
                    return false;
                }
                
                if (newPassword.length < 4) {
                    e.preventDefault();
                    alert('Password must be at least 4 characters long!');
                    return false;
                }
            });
        </script>
        """,
    )
    async def reset_password_action(self, request: Request, pk: Any) -> str:
        """
        Action to reset a user's password
        """
        try:
            from starlette.datastructures import FormData
            data: FormData = await request.form()
            new_password = data.get("new_password")
            confirm_password = data.get("confirm_password")
            
            # Validate passwords match
            if new_password != confirm_password:
                raise ActionFailed("Passwords do not match!")
            
            if not new_password or len(new_password) < 4:
                raise ActionFailed("Password must be at least 4 characters long!")
            
            # Update password in database
            async with self.session_maker() as session:
                user = await session.get(self.model, pk)
                if not user:
                    raise ActionFailed("User not found!")
                
                user.password = new_password
                await session.commit()
            
            return f"Password successfully reset for user: {user.username}"
            
        except Exception as e:
            raise ActionFailed(f"Failed to reset password: {str(e)}")
    
    @action(
        name="bulk_password_reset",
        text="Bulk Password Reset",
        confirmation="Reset passwords for selected users?",
        icon_class="fas fa-users-cog",
        submit_btn_text="Reset All",
        submit_btn_class="btn-danger",
        form="""
        <div class="mb-3">
            <label for="default_password" class="form-label">Default Password:</label>
            <input type="password" id="default_password" name="default_password" class="form-control" 
                   placeholder="Enter default password for all selected users" required>
        </div>
        <div class="alert alert-warning">
            <strong>Warning:</strong> This will reset passwords for ALL selected users to the same default password.
            Users should change their passwords after login.
        </div>
        """,
    )
    async def bulk_password_reset_action(self, request: Request, pks: list[Any]) -> str:
        """
        Bulk action to reset multiple users' passwords
        """
        try:
            from starlette.datastructures import FormData
            data: FormData = await request.form()
            default_password = data.get("default_password")
            
            if not default_password or len(default_password) < 4:
                raise ActionFailed("Default password must be at least 4 characters long!")
            
            updated_count = 0
            async with self.session_maker() as session:
                for pk in pks:
                    user = await session.get(self.model, pk)
                    if user:
                        user.password = default_password
                        updated_count += 1
                
                await session.commit()
            
            return f"Successfully reset passwords for {updated_count} users"
            
        except Exception as e:
            raise ActionFailed(f"Failed to reset passwords: {str(e)}")


# Alternative simplified view if you want even less features
# class SimpleUserView(ModelView):
#     """
#     Simplified user management view with minimal features
#     """
    
#     row_actions = ["edit", "delete"]
#     page_size = 20
    
#     fields = ["username", "password"]
#     searchable_fields = ["username"]
#     sortable_fields = ["username"]
    
#     labels = {
#         "username": "Username",
#         "password": "Password"
#     }
    
#     async def create(self, request: Request, data: Dict[str, Any]) -> Any:
#         """Set client_name to username and provide defaults"""
#         data["client_name"] = data.get("username", "")
#         data["site_name"] = []
#         data["greenhouse_name"] = []
#         return await super().create(request, data)
    
#     async def edit(self, request: Request, pk: Any, data: Dict[str, Any]) -> Any:
#         """Update client_name when username changes"""
#         if "username" in data:
#             data["client_name"] = data["username"]
#         return await super().edit(request, pk, data)
    
#     async def serialize_field_value(self, value: Any, field: str) -> Any:
#         """Mask passwords in list view"""
#         if field == "password":
#             return "*" * min(len(str(value)), 6) if value else ""
#         return await super().serialize_field_value(value, field)