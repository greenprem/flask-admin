from starlette_admin.contrib.sqlmodel import ModelView
from starlette_admin.exceptions import FormValidationError
from starlette_admin import RowActionsDisplayType
from starlette.requests import Request
from typing import Any, Dict

# from app.sqla.models import Client, SymptomThreshold, CycleInfo, Greenhouse, EnvData, Feedback, SensorRange, DiseaseData, BucketValues, PlantWeek, Observation, Grid, GridAnalysis, FeedBackGridImages, Weeks

from app.sqla.models import Client

class ClientView(ModelView):
    page_size = 10

    # Fields to show in the table view
    fields = [
        "id", "client_name", "username", "password", "site_name", "greenhouse_name"
    ]

    # Fields to search and sort by
    searchable_fields = ["client_name", "username"]
    sortable_fields = ["id", "client_name"]

    # Make fields read-only in edit form
    exclude_fields_from_edit = ["client_name", "username", "password"]

# class SymptomThresholdView(ModelView):
#     page_size = 10
#     fields = ["id", "disease", "val"]
#     searchable_fields = [SymptomThreshold.disease]
#     sortable_fields = [SymptomThreshold.id, SymptomThreshold.disease]

# class CycleInfoView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client_name", "site", "greenhouse", "name",
#         "date", "startDate", "observationPending",
#         "comparedTo", "reportwriting"
#     ]
#     searchable_fields = [CycleInfo.client_name, CycleInfo.name]
#     sortable_fields = [CycleInfo.id, CycleInfo.date, CycleInfo.startDate]



# class EnvDataView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client_name", "site", "greenhouse_id", "item_id",
#         "date", "time", "json_data"
#     ]
#     searchable_fields = [EnvData.client_name, EnvData.site]
#     sortable_fields = [EnvData.id, EnvData.date, EnvData.time]

# class FeedbackView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client_name", "selected_cycle", "selected_greenhouse",
#         "selected_grid", "selected_site", "message", "fileName",
#         "video_status", "video_url"
#     ]
#     searchable_fields = [Feedback.client_name, Feedback.selected_site]
#     sortable_fields = [Feedback.id, Feedback.video_status]

# class SensorRangeView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client", "greenhouse", "site",
#         "temp_optimal", "humidity_risky", "ec_risky", "ph_risky"
#     ]
#     searchable_fields = [SensorRange.client, SensorRange.site]
#     sortable_fields = [SensorRange.id]

# class DiseaseDataView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "location", "crop", "disease",
#         "temp_range", "humid_range", "ec_range", "ph_range",
#         "temp_range2", "humid_range2", "ec_range2", "ph_range2",
#         "visual_symptom"
#     ]
#     searchable_fields = [DiseaseData.crop, DiseaseData.disease]
#     sortable_fields = [DiseaseData.id]

# class BucketValuesView(ModelView):
#     page_size = 10
#     fields = ["id", "client_name", "site", "greenhouse", "json_data", "flagarray"]
#     searchable_fields = [BucketValues.client_name, BucketValues.site]
#     sortable_fields = [BucketValues.id]

# class PlantWeekView(ModelView):
#     page_size = 10
#     fields = ["id", "client_name", "site", "greenhouse", "weekday"]
#     searchable_fields = [PlantWeek.client_name]
#     sortable_fields = [PlantWeek.id, PlantWeek.weekday]

# class ObservationView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client_name", "site", "greenhouse", "cycle_name",
#         "comparison_cycle_name", "delta_t_id", "data", "message",
#         "temp_optimal", "humidity_optimal", "ec_risky", "ph_risky",
#         "copy", "env_data", "grid_data", "plant_data"
#     ]
#     searchable_fields = [Observation.client_name, Observation.cycle_name]
#     sortable_fields = [Observation.id]

# class GridView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client_name", "selected_greenhouse",
#         "selected_site", "grid_format"
#     ]
#     searchable_fields = [Grid.client_name]
#     sortable_fields = [Grid.id]

# class GridAnalysisView(ModelView):
#     page_size = 10
#     fields = [
#         "id", "client_name", "selected_greenhouse",
#         "selected_site", "selected_cycle", "json_data"
#     ]
#     searchable_fields = [GridAnalysis.client_name]
#     sortable_fields = [GridAnalysis.id]

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
