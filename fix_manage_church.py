
import os

content = r"""{% extends 'layouts/app_base.html' %}
{% load static %}

{% block title %}Manage Church - ChurchConnect{% endblock %}

{% block body_class %}page-manage-church{% endblock %}

{% block extra_css %}
<link rel="stylesheet" href="{% static 'css/variables/blue-sky-vars.css' %}?v={{ STATIC_VERSION }}">
<link rel="stylesheet" href="{% static 'css/themes/blue-sky-theme.css' %}?v={{ STATIC_VERSION }}">
<link rel="stylesheet" href="{% static 'css/components/buttons.css' %}?v={{ STATIC_VERSION }}">
<link rel="stylesheet" href="{% static 'css/components/cards.css' %}?v={{ STATIC_VERSION }}">
<link rel="stylesheet" href="{% static 'css/components/forms.css' %}?v={{ STATIC_VERSION }}">
<link rel="stylesheet" href="{% static 'css/components/post_analytics_modal.css' %}?v={{ STATIC_VERSION }}">
<link rel="stylesheet" href="{% static 'css/components/post_creation_modal.css' %}?v={{ STATIC_VERSION }}">
<link rel="stylesheet" href="{% static 'css/pages/manage-church.css' %}?v={{ STATIC_VERSION }}">
<link rel="stylesheet" href="{% static 'css/create_booking_manual.css' %}?v={{ STATIC_VERSION }}">
<link rel="stylesheet" href="https://unpkg.com/cropperjs@1.5.13/dist/cropper.min.css">
{% endblock %}

{% block sidebar %}
{% include 'partials/sidebar.html' %}
{% endblock %}
{% block topbar %}
{% include 'partials/topbar.html' %}
{% endblock %}

{% block content %}
<div class="manage-church-page blue-sky page-container" data-church-id="{{ church.id }}">
  {% include 'partials/manage/page_header.html' %}
  {% include 'partials/manage/verification_banner.html' with church=church latest_verification=latest_verification %}
  {% include 'partials/manage/church_preview.html' with church=church %}

  <div class="management-tabs">
    <div class="tabs-container">
      {% include 'partials/manage/tab_navigation.html' %}

      <div class="tabs-content">
        {% include 'partials/manage/overview_tab.html' with church=church follower_count=follower_count analytics=analytics bookings=bookings booking_counts=booking_counts donations=donations %}
        {% include 'partials/manage/appointments_tab.html' with bookings=bookings booking_counts=booking_counts appt_status=appt_status %}
        {% include 'partials/manage/services_tab.html' with church=church %}
        {% include 'partials/manage/availability_tab.html' with church=church %}
        {% include 'partials/manage/priests_tab.html' with church=church priests=priests %}
        {% include 'partials/manage/events_tab.html' with event_posts=event_posts event_posts_count=event_posts_count follower_count=follower_count church=church %}
        {% include 'partials/manage/content_tab.html' with analytics=analytics follower_count=follower_count posts=posts posts_count=posts_count church=church %}
        {% include 'partials/manage/donations_tab.html' %}
        {% include 'partials/manage/transactions_tab.html' %}
        {% include 'partials/manage/followers_tab.html' with recent_followers=recent_followers follower_count=follower_count %}
        {% include 'partials/manage/admins_tab.html' with church=church %}
        {% include 'partials/manage/settings_tab.html' with church=church form=form verif_form=verif_form decline_reasons=decline_reasons %}
      </div>
    </div>
  </div>
</div>

{% include 'partials/manage/modals.html' with church=church %}
{% endblock %}

{% block extra_js %}
<script>
  const csrfToken = '{{ csrf_token }}';
  window.csrfToken = '{{ csrf_token }}';
  const CURRENT_CHURCH_ID = "{{ church.id }}";
  window.CURRENT_CHURCH_ID = "{{ church.id }}";
</script>
<script src="https://unpkg.com/cropperjs@1.5.13/dist/cropper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script>
  window.djangoUrls = {
    updateChurchLogo: "{% url 'core:update_church_logo' %}",
    updateChurchCover: "{% url 'core:update_church_cover' %}",
    createAvailability: "{% url 'core:create_availability' %}?church_id={{ church.id }}&date=0",
    manageServiceImages: "{% url 'core:manage_service_images' 0 %}",
    serviceGallery: "{% url 'core:service_gallery' 0 %}",
    requestVerification: "{% url 'core:request_verification' %}",
    createDeclineReason: "{% url 'core:create_decline_reason' %}"
  };
  window.manageServiceImagesUrl = window.djangoUrls.manageServiceImages;
  window.serviceGalleryUrl = window.djangoUrls.serviceGallery;
  window.createDeclineReasonUrl = "{% url 'core:create_decline_reason' %}";
</script>
<script defer src="{% static 'js/core/tabs.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/core/forms.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/core/image-cropper.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/core/calendar.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/core/settings.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/app/manage_church_new.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/manage/post-management.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/dashboard/dashboard-posts.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/components/expandable-posts.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/components/post-view-tracker.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/components/post_analytics_modal.js' %}?v={{ STATIC_VERSION }}&t=20251031"></script>
<script defer src="{% static 'js/followers.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/sticky-tabs.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/settings-navigation.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/settings-section-edit.js' %}?v={{ STATIC_VERSION }}"></script>
<script defer src="{% static 'js/create_booking_manual.js' %}?v={{ STATIC_VERSION }}"></script>
{% endblock %}
"""

with open('templates/core/manage_church.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('File written successfully')
