from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    CaseViewSet,
    DocChangeLogView, 
    FileViewSet, 
    CaseChangelogViewSet, 
    DocChangelogViewSet, 
    UserCaseAccessRecordViewSet,
    UserViewSet,
    CaseChangelogView,
    UpdatedCasesView,
    upload_file, 
    list_files,
    serve_file,
    get_analysis,
    update_analysis,
    documents_to_review,
    sign_up,
    get_user_info,
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='case')
router.register(r'dashboard', CaseViewSet, basename='dashboard')
router.register(r'files', FileViewSet, basename='file')
router.register(r'users', UserViewSet, basename='users')
router.register(r'case-changes', CaseChangelogViewSet, basename='case-changelog')
router.register(r'doc-changes', DocChangelogViewSet, basename='doc-changelog')
router.register(r'user-case-access', UserCaseAccessRecordViewSet, basename='user-case-access')

# URL patterns
urlpatterns = [
    # Authentication
    path('signup/', sign_up, name='sign_up'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/info/', get_user_info, name='user-info'),

    # Changelog
    path('cases/<int:case_id>/change-log/', CaseChangelogView.as_view(), name='case-change-log'),
    path('updated-cases/', UpdatedCasesView.as_view(), name='updated-cases'), 
    path('files/<int:file_id>/change-log/', DocChangeLogView.as_view(), name='doc-change-log'),

    # File handling
    path('upload/', upload_file, name='upload_file'), 
    path('files/', list_files, name='list_files'),
    path('files/<int:pk>/', serve_file, name='serve_file'),
    path('cases/<int:case_id>/files/', FileViewSet.as_view({'get': 'list_by_case'}), name='case-files'),
    

    # Analysis & Reviewal
    path('get-analysis/<int:pk>/', get_analysis, name='get_analysis'),
    path('update-analysis/<int:pk>/', update_analysis, name='update_analysis'),
    path('documents-to-review/', documents_to_review, name='documents_to_review'),

    # Include router endpoints
    path('', include(router.urls)), 
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
