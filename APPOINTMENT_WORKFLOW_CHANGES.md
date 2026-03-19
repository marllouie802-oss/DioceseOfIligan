# Appointment System Workflow Changes

## Overview
The appointment booking system has been restructured to follow the correct multi-step workflow as required by your professor.

## Old Workflow (Incorrect)
1. User selects date
2. User selects time
3. Submit request
4. Parish approves/declines

## New Workflow (Correct)
1. **User requests form** from parish
2. **Parish reviews** and provides form to user
3. **User fills out form** and submits required documents
4. **Parish processes** form and completes proceedings
5. **User selects available pastor** for the service
6. **User schedules date** for the event
7. **Parish confirms** the appointment

## Changes Made

### 1. Database Models (`core/models.py`)

#### New Model: `Pastor`
- Represents pastors/ministers available in each parish
- Fields: name, title, email, phone, photo, bio, specializations, is_available
- Allows users to select which pastor will handle their service

#### Updated Model: `Booking`
**New Status Flow:**
- `form_requested` - User requests the form (Step 1)
- `form_provided` - Parish provides the form
- `form_submitted` - User submits filled form with documents
- `form_processing` - Parish is processing the form
- `form_approved` - Form approved, user can proceed
- `pastor_selection` - User needs to select a pastor
- `pastor_assigned` - Pastor has been assigned (Step 4)
- `scheduling` - User needs to schedule a date
- `scheduled` - Date has been scheduled (Step 5)
- `confirmed` - Parish confirms the appointment
- `completed` - Service completed
- `declined` - Request declined
- `canceled` - Request canceled

**New Fields:**
- `pastor` - ForeignKey to Pastor model
- `form_request_notes` - Initial notes when requesting form
- `form_provided_at` - Timestamp when parish provided form
- `form_submitted_at` - Timestamp when user submitted form
- `form_documents` - Description of submitted documents
- `form_approval_notes` - Notes from parish when approving
- `date` - Now nullable, set only after form approval
- `start_time` - Now nullable, set only after form approval

### 2. Views (`core/views.py`)

#### Updated: `book_service(request, service_id)`
- Now only handles Step 1: Form Request
- Creates booking with status `form_requested`
- No date/time selection at this stage
- User provides initial message/questions

#### New: `select_pastor(request, booking_id)`
- Step 4: User selects a pastor
- Only accessible when status is `form_approved`
- Shows available pastors for the church
- Updates booking status to `pastor_assigned`

#### New: `schedule_date(request, booking_id)`
- Step 5: User schedules appointment date
- Only accessible when status is `pastor_assigned`
- User selects date and time
- Updates booking status to `scheduled`

### 3. Templates

#### Updated: `book_service.html`
- Removed date/time selection wizard
- Shows new 5-step workflow indicator
- Simple form for requesting the required form
- User can add initial message/questions
- Shows service information and preparation notes

#### New Templates Needed:
- `select_pastor.html` - For pastor selection (Step 4)
- `schedule_date.html` - For date scheduling (Step 5)

### 4. URL Patterns (`core/urls.py`)
Added new URL patterns:
- `/booking/<id>/select-pastor/` - Pastor selection view
- `/booking/<id>/schedule-date/` - Date scheduling view

## Parish Management Requirements

The parish staff will need views to:
1. **Review form requests** - View and provide forms to users
2. **Process submitted forms** - Review documents and approve/decline
3. **Manage pastors** - Add/edit/remove available pastors
4. **Confirm scheduled appointments** - Final confirmation

## Next Steps

### High Priority:
1. **Create database migrations** for new models and fields
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Create missing templates:**
   - `templates/core/select_pastor.html`
   - `templates/core/schedule_date.html`

3. **Update `my_appointments.html`** to show current workflow step

4. **Create parish management views** for:
   - Providing forms to users
   - Reviewing submitted forms
   - Approving/declining forms
   - Managing pastors
   - Confirming scheduled appointments

### Medium Priority:
5. **Update manage_booking view** to handle new statuses
6. **Add pastor management interface** in parish dashboard
7. **Create notifications** for each workflow step
8. **Update email templates** for new workflow

### Recommendations:
- Add file upload capability for users to submit form documents
- Create a document management system for parishes to track submitted forms
- Add calendar integration for pastor availability
- Implement automated reminders for pending actions
- Add workflow progress tracking in user dashboard

## Migration Notes

**IMPORTANT:** Before running migrations:
1. Backup your database
2. Existing bookings will need data migration to new status values
3. Consider creating a data migration script to convert old statuses to new ones:
   - `requested` → `form_requested`
   - `reviewed` → `form_processing`
   - `approved` → `scheduled`
   - etc.

## Testing Checklist

- [ ] User can request a form for a service
- [ ] Parish can view form requests
- [ ] Parish can provide forms to users
- [ ] User can submit filled forms
- [ ] Parish can approve/decline forms
- [ ] User can select a pastor after approval
- [ ] User can schedule a date after pastor selection
- [ ] Parish can confirm scheduled appointments
- [ ] All status transitions work correctly
- [ ] Notifications are sent at each step
- [ ] Email notifications work
- [ ] User can cancel at any step
- [ ] Parish can decline at any step

## Benefits of New Workflow

1. **Compliance** - Follows proper church procedures
2. **Documentation** - Better tracking of required documents
3. **Flexibility** - Users can choose their preferred pastor
4. **Transparency** - Clear workflow steps for users
5. **Control** - Parish has more control over the process
6. **Accountability** - Clear audit trail of all steps
