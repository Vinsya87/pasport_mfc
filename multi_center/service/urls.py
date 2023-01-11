from django.urls import path

from . import views

app_name = 'service_url'

urlpatterns = [
    # path('', views.index, name='service_index'),
    path('', views.IndexView.as_view(), name='service_index'),
    path(
        'filter_extra/',
        views.FilterExtraView.as_view(),
        name='filter_extra'),
    path(
        'filter_service/',
        views.FilterServiceView.as_view(),
        name='filter_service'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path('create/', views.service_create, name='service_create'),
    path('create_extra/', views.extra_create, name='extra_create'),
    path(
        'extradite_extra_yes/<int:post_id>/',
        views.extradite_extra_yes,
        name='extradite_extra_yes'),
    path(
        'extradite_service_yes/<int:post_id>/',
        views.extradite_service_yes,
        name='extradite_service_yes'),
    path(
        'review_extra_yes/<int:post_id>/',
        views.review_extra_yes,
        name='review_extra_yes'),
    path(
        'review_extra_no/<int:post_id>/',
        views.review_extra_no,
        name='review_extra_no'),
    path(
        'review_service_yes/<int:post_id>/',
        views.review_service_yes,
        name='review_service_yes'),
    path(
        'review_service_no/<int:post_id>/',
        views.review_service_no,
        name='review_service_no'),
]
