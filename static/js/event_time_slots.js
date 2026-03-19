// Event Time Slots Management
// This file provides time slot functionality for event scheduling

// Helper function to reset the event schedule modal UI to loading state
function resetEventScheduleModalUI() {
    // Reset priest info to loading state
    const priestName = document.getElementById('event-priest-name');
    const priestTitle = document.getElementById('event-priest-title');
    const priestPhoto = document.getElementById('event-priest-photo');
    
    if (priestName) priestName.textContent = 'Loading priest information...';
    if (priestTitle) priestTitle.textContent = 'Loading...';
    if (priestPhoto) {
        priestPhoto.innerHTML = '<i data-feather="user" style="width: 24px; height: 24px; color: #9CA3AF;"></i>';
    }
    
    // Reset service info to loading state
    const serviceName = document.getElementById('event-service-name');
    const serviceDescription = document.getElementById('event-service-description');
    const servicePhoto = document.getElementById('event-service-photo');
    
    if (serviceName) serviceName.textContent = 'Loading service information...';
    if (serviceDescription) serviceDescription.textContent = 'Loading...';
    if (servicePhoto) {
        servicePhoto.innerHTML = '<i data-feather="image" style="width: 32px; height: 32px; color: #9CA3AF;"></i>';
    }
    
    // Re-initialize feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

// Helper function to populate priest information
function populateEventPriestInfo(priests, currentPastorId) {
    const priestName = document.getElementById('event-priest-name');
    const priestTitle = document.getElementById('event-priest-title');
    const priestPhoto = document.getElementById('event-priest-photo');
    
    if (!priests || priests.length === 0) {
        if (priestName) priestName.textContent = 'No priest assigned';
        if (priestTitle) priestTitle.textContent = 'Please contact the church';
        return;
    }
    
    // Find the assigned priest
    let assignedPriest = null;
    if (currentPastorId) {
        assignedPriest = priests.find(p => p.id === currentPastorId);
    }
    
    // If no assigned priest, use the first available one
    const priest = assignedPriest || priests[0];
    
    if (priest) {
        if (priestName) priestName.textContent = priest.name || 'Unknown Priest';
        if (priestTitle) priestTitle.textContent = priest.title || 'Priest';
        
        if (priestPhoto) {
            if (priest.photo_url) {
                priestPhoto.innerHTML = `<img src="${priest.photo_url}" alt="${priest.name}" style="width: 100%; height: 100%; object-fit: cover;">`;
            } else {
                priestPhoto.innerHTML = '<i data-feather="user" style="width: 24px; height: 24px; color: #9CA3AF;"></i>';
            }
        }
    }
    
    // Re-initialize feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

// Helper function to populate service information
function populateEventServiceInfo(service) {
    const serviceName = document.getElementById('event-service-name');
    const serviceDescription = document.getElementById('event-service-description');
    const servicePhoto = document.getElementById('event-service-photo');
    
    if (!service) {
        if (serviceName) serviceName.textContent = 'Service information unavailable';
        if (serviceDescription) serviceDescription.textContent = 'Please contact the church for details';
        return;
    }
    
    if (serviceName) serviceName.textContent = service.name || 'Unknown Service';
    if (serviceDescription) serviceDescription.textContent = service.description || 'No description available';
    
    if (servicePhoto) {
        if (service.image_url) {
            servicePhoto.innerHTML = `<img src="${service.image_url}" alt="${service.name}" style="width: 100%; height: 100%; object-fit: cover;">`;
        } else {
            servicePhoto.innerHTML = '<i data-feather="image" style="width: 32px; height: 32px; color: #9CA3AF;"></i>';
        }
    }
    
    // Re-initialize feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

// Helper function to show error message in the modal
function showEventScheduleError(message) {
    const priestName = document.getElementById('event-priest-name');
    const serviceName = document.getElementById('event-service-name');
    
    if (priestName) priestName.textContent = 'Error loading data';
    if (serviceName) serviceName.textContent = message || 'An error occurred';
}

// Helper function to enhance date input restrictions
function enhanceDateInputRestrictions(dateInput, minDate, preparationDays) {
    // Add CSS class for styling
    dateInput.classList.add('restricted-date-input');
    
    // Add title attribute for hover tooltip
    dateInput.title = `Event requires ${preparationDays} days preparation. Earliest date: ${minDate.toLocaleDateString()}`;
    
    // Add visual indicator for preparation period
    const today = new Date();
    const daysUntilMin = Math.ceil((minDate - today) / (1000 * 60 * 60 * 24));
    
    if (daysUntilMin > 0) {
        dateInput.setAttribute('data-preparation-days', preparationDays);
        dateInput.setAttribute('data-earliest-date', minDate.toLocaleDateString());
    }
}

// Helper function to validate event date with enhanced feedback
function validateEventDate(dateInput, minDate, preparationDays, helpText) {
    const selectedDate = new Date(dateInput.value);
    const today = new Date();
    const daysUntilSelected = Math.ceil((selectedDate - today) / (1000 * 60 * 60 * 24));
    
    if (!dateInput.value || isNaN(selectedDate.getTime())) {
        // No date selected
        dateInput.setCustomValidity('');
        helpText.textContent = `Event requires ${preparationDays} days preparation (earliest: ${minDate.toLocaleDateString()})`;
        helpText.className = 'text-muted';
        return false;
    }
    
    if (daysUntilSelected < preparationDays) {
        // Too soon - doesn't meet preparation days requirement
        dateInput.setCustomValidity(`This event requires ${preparationDays} days preparation. Please select a date on or after ${minDate.toLocaleDateString()}.`);
        helpText.textContent = `❌ Too soon. Event requires ${preparationDays} days preparation (earliest: ${minDate.toLocaleDateString()})`;
        helpText.className = 'text-danger';
        dateInput.classList.add('invalid-date');
        dateInput.classList.remove('valid-date');
        return false;
    } else {
        // Valid date and meets preparation requirement
        dateInput.setCustomValidity('');
        if (preparationDays > 0) {
            helpText.textContent = `✓ Valid date. ${preparationDays} days preparation required`;
        } else {
            helpText.textContent = '✓ Valid date';
        }
        helpText.className = 'text-success';
        dateInput.classList.add('valid-date');
        dateInput.classList.remove('invalid-date');
        return true;
    }
}

// Function to load event time slots
function loadEventTimeSlots(timeSlotsString) {
    const container = document.getElementById('event-time-slots-container');
    const timeSelectionContainer = document.getElementById('event-time-selection-container');
    
    if (!container || !timeSelectionContainer) return;
    
    container.innerHTML = '';
    
    // Parse time slots (format: "9:00 AM, 11:00 AM, 2:00 PM, 4:00 PM")
    const slots = timeSlotsString.split(',').map(slot => slot.trim()).filter(slot => slot);
    
    slots.forEach(slot => {
        const slotBtn = document.createElement('div');
        slotBtn.className = 'time-slot-btn';
        slotBtn.textContent = slot;
        
        slotBtn.onclick = () => {
                // Remove active class from all time slots
                document.querySelectorAll('#event-time-slots-container .time-slot-btn').forEach(btn => btn.classList.remove('active'));
                // Add active class to selected time slot
                slotBtn.classList.add('active');
                
                // Convert time slot to 24-hour format for event_time
                const startTime = convertTo24Hour(slot);
                
                document.getElementById('event-time-input').value = startTime;
                document.getElementById('event-time-slot').value = slot;
                
                // Add the time field that the form expects
                const timeInput = document.createElement('input');
                timeInput.type = 'hidden';
                timeInput.name = 'time';
                timeInput.value = slot;
                
                // Remove any existing time input
                const existingTimeInput = document.querySelector('input[name="time"]');
                if (existingTimeInput) {
                    existingTimeInput.remove();
                }
                
                // Add the new time input to the form
                document.getElementById('eventScheduleForm').appendChild(timeInput);
                
                document.getElementById('submit-event-schedule-btn').disabled = false;
            };
        
        container.appendChild(slotBtn);
    });
    
    // Show the time selection container
    timeSelectionContainer.style.display = 'block';
}

// Update to openEventScheduleModal function to load service time slots
function updateEventScheduleModal() {
    // Store the original function
    const originalOpenEventScheduleModal = window.openEventScheduleModal;
    
    // Replace with enhanced version
    window.openEventScheduleModal = function(id, code, service) {
        document.getElementById('event-booking-id').value = id;
        document.getElementById('eventScheduleModal').style.display = 'flex';
        
        // Reset the UI to loading state
        resetEventScheduleModalUI();
        
        // Fetch the booking to get the assigned priest's preparation days and service time slots
        fetch(`/app/api/booking/${id}/priests/`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Populate priest information
                    populateEventPriestInfo(data.priests, data.current_pastor_id);
                    
                    // Populate service information
                    populateEventServiceInfo(data.service);
                    
                    if (data.priests) {
                        // Find the assigned priest (if any)
                        const assignedPriestId = data.current_pastor_id;
                        let preparationDays = 30; // Default fallback
                        
                        if (assignedPriestId) {
                            const assignedPriest = data.priests.find(p => p.id === assignedPriestId);
                            if (assignedPriest && assignedPriest.preparation_days) {
                                preparationDays = assignedPriest.preparation_days;
                            }
                        }
                        
                        // Set minimum date based on preparation days
                        const eventDateInput = document.getElementById('event-date-input');
                        const today = new Date();
                        const minDate = new Date(today);
                        minDate.setDate(minDate.getDate() + preparationDays);
                        
                        // Set minimum date - this prevents selection in most browsers
                        eventDateInput.min = minDate.toISOString().split('T')[0];
                        
                        // Add visual date picker restrictions
                        enhanceDateInputRestrictions(eventDateInput, minDate, preparationDays);
                        
                        // Add help text to show preparation requirement
                        let helpText = document.getElementById('event-date-help-text');
                        if (!helpText) {
                            helpText = document.createElement('small');
                            helpText.id = 'event-date-help-text';
                            helpText.className = 'text-muted';
                            eventDateInput.parentNode.appendChild(helpText);
                        }
                        
                        if (preparationDays > 0) {
                            helpText.textContent = `Event requires ${preparationDays} days preparation (earliest: ${minDate.toLocaleDateString()})`;
                        } else {
                            helpText.textContent = 'Select your preferred event date';
                        }
                        
                        // Enhanced validation with better feedback
                        eventDateInput.addEventListener('input', function() {
                            validateEventDate(this, minDate, preparationDays, helpText);
                        });
                        
                        // Add change event for additional validation
                        eventDateInput.addEventListener('change', function() {
                            validateEventDate(this, minDate, preparationDays, helpText);
                        });
                        
                        // Load service time slots
                        loadEventTimeSlots(data.service_time_slots || '9:00 AM, 11:00 AM, 2:00 PM, 4:00 PM');
                    }
                }
            })
            .catch(error => {
                console.error('Error fetching booking data:', error);
                showEventScheduleError('Failed to load booking data. Please try again.');
                // Fallback: set minimum date to tomorrow and load default time slots
                const eventDateInput = document.getElementById('event-date-input');
                const tomorrow = new Date();
                tomorrow.setDate(tomorrow.getDate() + 1);
                eventDateInput.min = tomorrow.toISOString().split('T')[0];
                
                // Apply enhanced restrictions for fallback
                enhanceDateInputRestrictions(eventDateInput, tomorrow, 1);
                
                // Add help text for fallback
                let helpText = document.getElementById('event-date-help-text');
                if (!helpText) {
                    helpText = document.createElement('small');
                    helpText.id = 'event-date-help-text';
                    helpText.className = 'text-muted';
                    eventDateInput.parentNode.appendChild(helpText);
                }
                helpText.textContent = 'Select your preferred event date (earliest: tomorrow)';
                
                // Add validation for fallback
                eventDateInput.addEventListener('input', function() {
                    validateEventDate(this, tomorrow, 1, helpText);
                });
                
                eventDateInput.addEventListener('change', function() {
                    validateEventDate(this, tomorrow, 1, helpText);
                });
                
                // Load default time slots
                loadEventTimeSlots('9:00 AM, 11:00 AM, 2:00 PM, 4:00 PM');
            });
    };
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Wait for the main script to load, then update the function
    setTimeout(updateEventScheduleModal, 100);
    
    // Add event form submission handler
    const eventForm = document.getElementById('eventScheduleForm');
    if (eventForm) {
        eventForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const bookingId = formData.get('booking_id');
            const submitBtn = document.getElementById('submit-event-schedule-btn');
            const originalText = submitBtn.textContent;
            
            // Debug: Log all form data
            console.log('Event form data being submitted:');
            for (let [key, value] of formData.entries()) {
                console.log(`${key}: ${value}`);
            }
            
            // Check if all required fields are present
            const requiredFields = ['booking_id', 'event_date'];
            const missingFields = requiredFields.filter(field => !formData.get(field));
            if (missingFields.length > 0) {
                console.error('Missing required fields:', missingFields);
                alert(`Missing required fields: ${missingFields.join(', ')}`);
                return;
            }
            
            // Disable button and show loading state
            submitBtn.disabled = true;
            submitBtn.textContent = 'Scheduling...';
            
            // Set the form action dynamically
            this.action = `/app/booking/${bookingId}/schedule-event/`;
            console.log('Submitting to:', this.action);
            
            // Submit via fetch for better error handling
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                console.log('Response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                if (data.success) {
                    alert(data.message || 'Your event schedule has been submitted!');
                    closeEventScheduleModal();
                    // Reload page to show updated status
                    window.location.reload();
                } else {
                    alert(data.message || 'Error submitting event schedule. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error submitting event schedule:', error);
                alert('Error submitting event schedule. Please try again.');
            })
            .finally(() => {
                // Re-enable button
                submitBtn.disabled = false;
                submitBtn.textContent = originalText;
            });
        });
    }
});
