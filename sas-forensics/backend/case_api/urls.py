from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    CaseViewSet,
    DocChangeLogView, 
    FileViewSet, 
    CaseChangelogViewSet, 
    DocChangelogViewSet, 
    UserCaseAccessRecordViewSet,
    CaseListCreateView, 
    CaseListView,
    UserViewSet,
    UpdatedCasesView,
    CaseChangeLogView,
    upload_file, 
    list_files,
    serve_file,
    get_analysis,
    update_analysis,
    documents_to_review,
    login_view, 
    register_user,
)

router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'files', FileViewSet, basename='file')
router.register(r'users', UserViewSet, basename='users')
router.register(r'case-changes', CaseChangelogViewSet, basename='case-changelog')
router.register(r'doc-changes', DocChangelogViewSet, basename='doc-changelog')
router.register(r'user-case-access', UserCaseAccessRecordViewSet, basename='user-case-access')
router.register(r'recent-cases', CaseViewSet, basename='recent-cases')

# URL patterns
urlpatterns = [
    path('upload/', upload_file, name='upload_file'), 
    path('files/', list_files, name='list_files'),
    path('cases/', CaseListCreateView.as_view(), name='case-list-create'),
    path('cases/', CaseListView.as_view(), name='case-list'),
    path('api/cases/<int:case_id>/files/', FileViewSet.as_view({'get': 'list_by_case'}), name='case-files'),
    path('updated-cases/', UpdatedCasesView.as_view(), name='updated-cases'),
    path('files/<int:pk>/', views.serve_file, name='serve_file'),
    path('cases/<int:case_id>/change-log/', CaseChangeLogView.as_view(), name='case-change-log'),
    path('files/<int:file_id>/change-log/', DocChangeLogView.as_view(), name='doc-change-log'),
    path('api/cases/<int:case_id>/change-log/', CaseChangeLogView.as_view(), name='case-change-log'),
    path('api/get-analysis/<int:pk>/', get_analysis, name='get_analysis'),
    path('api/update-analysis/<int:pk>/', update_analysis, name='update_analysis'),
    path('api/documents-to-review/', documents_to_review, name='documents_to_review'),
    path('api/', include(router.urls)), 
    path('login/', login_view, name='login'),
    path('signup/', register_user, name = 'sign_up'),
]
