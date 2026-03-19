from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from .models import Booking, BookableService, Notification, Pastor
from .forms import BookingForm, BookingScheduleForm, BookingEventScheduleForm
from .notifications import notify_parish_staff, NotificationTemplates

@login_required
def submit_booking_request(request, service_id):
    """Submit a booking request without a date (initial step)."""
    service = get_object_or_404(BookableService, id=service_id, is_active=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, service=service, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.church = service.church
            booking.user = request.user
            booking.status = Booking.STATUS_REQUESTED
            booking.save()
            
            # Send notification to staff
            tmpl = NotificationTemplates.booking_requested(booking)
            notify_parish_staff(
                church=booking.church,
                notification_type=Notification.TYPE_BOOKING_REQUESTED,
                title=tmpl['title'],
                message=tmpl['message'],
                required_permission='appointments',
                priority=tmpl['priority'],
                booking=booking
            )
            
            messages.success(request, 'Your appointment request has been submitted. The parish will review it shortly.')
            return redirect('core:appointments')
    else:
        form = BookingForm(service=service, user=request.user)
    
    # If not POST, usually handled via modal in church_detail, but fallback here if needed
    return redirect('core:church_detail', slug=service.church.slug)

@login_required
@require_POST
def admin_approve_request_requirements(request, booking_id):
    """Admin approves request and asks for requirements."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Permission check (simplified, should use decorator or helper)
    if not (request.user == booking.church.owner or request.user.staff_positions.filter(church=booking.church, status='active').exists()):
         return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)

    if booking.status != Booking.STATUS_REQUESTED:
        return JsonResponse({'success': False, 'message': 'Invalid status for this action'}, status=400)

    # Update status
    booking.status = Booking.STATUS_PENDING_REQUIREMENTS
    booking.handled_by = request.user
    booking.form_approval_notes = request.POST.get('notes', '')
    booking.save()

    # Notify User
    Notification.objects.create(
        user=booking.user,
        church=booking.church,
        notification_type=Notification.TYPE_BOOKING_REVIEWED, # Or similar
        title='Appointment Update',
        message=f'Your request for {booking.service.name} has been reviewed. Please check the requirements needed.',
        booking=booking
    )

    return JsonResponse({'success': True, 'message': 'Request approved. Waiting for user requirements.'})

@login_required
@require_POST
def admin_verify_requirements(request, booking_id):
    """Admin verifies requirements and allows scheduling."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Permission check
    if not (request.user == booking.church.owner or request.user.staff_positions.filter(church=booking.church, status='active').exists()):
         return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)

    if booking.status != Booking.STATUS_PENDING_REQUIREMENTS:
        return JsonResponse({'success': False, 'message': 'Invalid status for this action'}, status=400)

    booking.status = Booking.STATUS_READY_TO_SCHEDULE
    booking.save()

    # Notify User
    Notification.objects.create(
        user=booking.user,
        church=booking.church,
        notification_type=Notification.TYPE_BOOKING_APPROVED, # Re-using approved type for "Ready to Schedule"
        title='Requirements Verified',
        message=f'Your requirements for {booking.service.name} have been verified. You may now schedule your date.',
        booking=booking
    )

    return JsonResponse({'success': True, 'message': 'Requirements verified. User can now schedule.'})

@login_required
def schedule_booking_date(request, booking_id):
    """User selects date and priest for approved booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Allow scheduling for both confirmed and ready_to_schedule statuses
    schedulable_statuses = [
        Booking.STATUS_READY_TO_SCHEDULE,
        Booking.STATUS_CONFIRMED,
        Booking.STATUS_RESCHEDULE,
        Booking.STATUS_APPROVED,  # Legacy status
    ]
    
    if booking.status not in schedulable_statuses:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'This appointment is not ready for scheduling.'}, status=400)
        messages.error(request, 'This appointment is not ready for scheduling.')
        return redirect('core:appointments')

    if request.method == 'POST':
        form = BookingScheduleForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = Booking.STATUS_SCHEDULE_REQUESTED
            booking.save()
            
            # Notify Admin
            msg = f'{booking.user.get_full_name()} has requested to schedule their {booking.service.name} for {booking.date}. Please review.'
            if booking.pastor:
                msg = f'{booking.user.get_full_name()} has requested to schedule their {booking.service.name} for {booking.date} with {booking.pastor.full_title}. Please review.'

            notify_parish_staff(
                church=booking.church,
                notification_type=Notification.TYPE_BOOKING_REQUESTED, # Changed to REQUESTED
                title='Schedule Request',
                message=msg,
                required_permission='appointments',
                booking=booking
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': 'Your schedule request has been submitted for approval.',
                    'new_status': booking.get_status_display(),
                    'date': booking.date.strftime('%B %d, %Y') if booking.date else '',
                    'time': booking.start_time.strftime('%I:%M %p') if booking.start_time else (booking.time_slot or ''),
                    'pastor': booking.pastor.full_title if booking.pastor else '',
                })
            
            messages.success(request, 'Your schedule request has been submitted for approval.')
            return redirect('core:appointments')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    return redirect('core:appointments')

@login_required
def api_booking_priests(request, booking_id):
    """Get available priests for a booking's church."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Get all priests for the church that are marked as available
    # Also include the currently assigned pastor if any, even if they are marked unavailable now
    priests = Pastor.objects.filter(church=booking.church, is_available=True)
    if booking.pastor:
        priests = priests | Pastor.objects.filter(id=booking.pastor.id)
    
    priests = priests.distinct().order_by('order', 'name')
    
    priest_list = []
    for p in priests:
        priest_list.append({
            'id': p.id,
            'name': p.full_title,
            'title': p.title,
            'specializations': p.specializations,
            'available_days': p.available_days,
            'available_time_slots': p.available_time_slots,
            'preparation_days': p.preparation_days,
            'display_availability': p.display_availability,
            'photo_url': p.photo.url if p.photo else None
        })
        
    return JsonResponse({
        'success': True, 
        'priests': priest_list,
        'current_pastor_id': booking.pastor.id if booking.pastor else None,
        'service_time_slots': booking.service.available_time_slots if booking.service and hasattr(booking.service, 'available_time_slots') else '',
        'service_advance_booking_days': booking.service.advance_booking_days if booking.service else None,
        'service': {
            'id': booking.service.id,
            'name': booking.service.name,
            'description': booking.service.description,
            'image_url': booking.service.image.url if booking.service.image else None,
            'duration': booking.service.duration,
            'price': str(booking.service.price) if booking.service.price else 'Free',
            'is_free': booking.service.is_free,
        } if booking.service else None
    })

@login_required
@require_POST
def admin_mark_interview_completed(request, booking_id):
    """Admin marks the priest appointment/interview as completed."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Permission check
    if not (request.user == booking.church.owner or request.user.staff_positions.filter(church=booking.church, status='active').exists()):
         return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)

    if booking.status != Booking.STATUS_SCHEDULED:
        return JsonResponse({'success': False, 'message': 'Invalid status for this action'}, status=400)

    booking.status = Booking.STATUS_INTERVIEW_COMPLETED
    booking.save()

    # Notify User
    Notification.objects.create(
        user=booking.user,
        church=booking.church,
        notification_type=Notification.TYPE_BOOKING_APPROVED, # Or similar
        title='Appointment Completed',
        message=f'Your appointment for {booking.service.name} has been marked as completed. You may now schedule your event date.',
        booking=booking
    )

    return JsonResponse({'success': True, 'message': 'Interview marked as completed. User can now schedule event.'})

@login_required
@require_POST
def admin_approve_schedule_request(request, booking_id):
    """Admin approves the schedule request."""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Permission check
    if not (request.user == booking.church.owner or request.user.staff_positions.filter(church=booking.church, status='active').exists()):
         return JsonResponse({'success': False, 'message': 'Permission denied'}, status=403)

    if booking.status != Booking.STATUS_SCHEDULE_REQUESTED:
        return JsonResponse({'success': False, 'message': 'Invalid status for this action'}, status=400)

    booking.status = Booking.STATUS_SCHEDULED
    booking.save()

    # Notify User
    Notification.objects.create(
        user=booking.user,
        church=booking.church,
        notification_type=Notification.TYPE_BOOKING_APPROVED,
        title='Schedule Approved',
        message=f'Your appointment schedule for {booking.service.name} on {booking.date} has been approved.',
        booking=booking
    )

    return JsonResponse({'success': True, 'message': 'Schedule request approved.'})

@login_required
def schedule_event_date(request, booking_id):
    """User selects actual event date after interview."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != Booking.STATUS_INTERVIEW_COMPLETED:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'This appointment is not ready for event scheduling.'}, status=400)
        messages.error(request, 'This appointment is not ready for event scheduling.')
        return redirect('core:appointments')

    if request.method == 'POST':
        form = BookingEventScheduleForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = Booking.STATUS_EVENT_REQUESTED
            booking.save()
            
            # Notify Admin
            msg = f'{booking.user.get_full_name()} has scheduled the event for {booking.service.name} on {booking.event_date}.'
            notify_parish_staff(
                church=booking.church,
                notification_type=Notification.TYPE_BOOKING_COMPLETED,
                title='Event Scheduled',
                message=msg,
                required_permission='appointments',
                booking=booking
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': 'Your event schedule has been submitted and is pending review!',
                    'new_status': booking.get_status_display(),
                    'event_date': booking.event_date.strftime('%B %d, %Y') if booking.event_date else '',
                    'event_time': booking.event_time.strftime('%I:%M %p') if booking.event_time else (booking.event_time_slot or ''),
                })
            
            messages.success(request, 'Your event schedule has been submitted and is pending review!')
            return redirect('core:appointments')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {field: [str(e) for e in errs] for field, errs in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    return redirect('core:appointments')
