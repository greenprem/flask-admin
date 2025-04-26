import os
from typing import Optional

from libcloud.storage.providers import get_driver
from libcloud.storage.types import Provider
from sqlalchemy_file.storage import StorageManager
from sqlmodel import create_engine
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette_admin import I18nConfig
from starlette_admin.i18n import SUPPORTED_LOCALES
from starlette_admin.contrib.sqla import Admin as BaseAdmin
from starlette_admin.contrib.sqla import Admin, ModelView

from app.config import config
from app.sqla.auth import MyAuthProvider
from app.sqla.models import Client, CycleInfo, EnvData, SensorRange, DiseaseData, BucketValues, PlantWeek, Observation, Grid, GridAnalysis
#from app.sqla.views import ClientView, SymptomThresholdView, CycleInfoView, EnvDataView, FeedbackView, SensorRangeView, DiseaseDataView, BucketValuesView, PlantWeekView, ObservationView, GridView, GridAnalysisView, FeedBackGridImagesView, WeeksView
from app.sqla.views import ClientView, CycleInfoView, EnvDataView, SensorRangeView, DiseaseDataView, BucketValuesView, PlantWeekView, ObservationView, GridView, GridAnalysisView, HomeView
__all__ = ["engine", "admin"]

# Save avatar to local Storage
os.makedirs(f"{config.upload_dir}/avatars", 0o777, exist_ok=True)
container = get_driver(Provider.LOCAL)(config.upload_dir).get_container("avatars")
StorageManager.add_storage("user-avatar", container)

engine = create_engine(config.sqla_engine)


class Admin(BaseAdmin):
    def custom_render_js(self, request: Request) -> Optional[str]:
        return request.url_for("statics", path="js/custom_render.js")


admin = Admin(
    engine,
    title="SQLModel Admin",
    base_url="/admin/sqla",
    route_name="admin-sqla",
    templates_dir="templates/admin/sqla",
    index_view=HomeView(label="Greenhouse Manager", icon="fa fa-id-badge"),
    auth_provider=MyAuthProvider(login_path="/sign-in", logout_path="/sign-out"),
    middlewares=[Middleware(SessionMiddleware, secret_key=config.secret)],
    i18n_config=I18nConfig(default_locale="en", language_switcher=SUPPORTED_LOCALES),
)

# Register only Client view
#admin.add_view(ClientView(Client, icon="fa fa-id-badge", label="Clients"))
#admin.add_view(ModelView(SymptomThreshold, icon="fa fa-id-badge", label="Symptom Threshold"))
admin.add_view(CycleInfoView(CycleInfo, icon="fa fa-id-badge", label="Cycle Info"))
admin.add_view(EnvDataView(EnvData, icon="fa fa-id-badge", label="Env Data"))
#admin.add_view(ModelView(Feedback, icon="fa fa-id-badge", label="Feedback"))
admin.add_view(SensorRangeView(SensorRange, icon="fa fa-id-badge", label="Sensor Range"))
admin.add_view(DiseaseDataView(DiseaseData, icon="fa fa-id-badge", label="Disease Data"))
admin.add_view(BucketValuesView(BucketValues, icon="fa fa-id-badge", label="Bucket Values"))
admin.add_view(PlantWeekView(PlantWeek, icon="fa fa-id-badge", label="Plant Week"))
admin.add_view(ObservationView(Observation, icon="fa fa-id-badge", label="Observation"))
admin.add_view(GridView(Grid, icon="fa fa-id-badge", label="Grid"))
admin.add_view(GridAnalysisView(GridAnalysis, icon="fa fa-id-badge", label="Grid Analysis"))
#admin.add_view(ModelView(FeedBackGridImages, icon="fa fa-id-badge", label="Feedback Grid Images"))
#admin.add_view(ModelView(Weeks, icon="fa fa-id-badge", label="Weeks"))