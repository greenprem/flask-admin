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

# from app.sqla.models import Client, SymptomThreshold, CycleInfo, Greenhouse, EnvData, Feedback, SensorRange, DiseaseData, BucketValues, PlantWeek, Observation, Grid, GridAnalysis, FeedBackGridImages, Weeks

from app.sqla.models import Client

class ClientView(ModelView):
    row_actions = ["view", "edit", "go_to_example", "make_published",
                   "delete"]  # edit, view and delete are provided by default
    row_actions_display_type = RowActionsDisplayType.ICON_LIST  # RowActionsDisplayType.DROPDOWN
    page_size = 10

    # Fields to show in the table view
    fields = [
        "id", "client_name", "username", "password", "site_name", "greenhouse_name"
    ]

    # Fields to search and sort by
    searchable_fields = ["client_name", "username"]
    sortable_fields = ["id", "client_name"]

    # Make fields read-only in edit form
    exclude_fields_from_edit = ["client_name", "username", "password", "site_name", "greenhouse_name"]

    @row_action(
        name="make_published",
        text="Mark as published",
        confirmation="Are you sure you want to mark this article as published ?",
        icon_class="fas fa-check-circle",
        submit_btn_text="Yes, proceed",
        submit_btn_class="btn-success",
        action_btn_class="btn-info",
        form="""
        <form>
            <div class="mt-3">
                <input type="text" class="form-control" name="example-text-input" placeholder="Enter value">
            </div>
        </form>
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

    @link_row_action(
        name="go_to_example",
        text="Go to example.com",
        icon_class="fas fa-arrow-up-right-from-square",
    )
    def go_to_example_row_action(self, request: Request, pk: Any) -> str:
        return f"https://example.com/?pk={pk}"

    

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
