/**
 * My Appointments Page JavaScript
 * Handles review modal and appointment summary functionality
 */

let currentServiceId = null;
let currentBookingId = null;
let currentServicePrice = 0;
let currentServiceIsFree = false;
let stripe = null;
let stripeElements = null;
let stripeCardElement = null;
let cancelBookingId = null;

/**
 * Open the appointment summary modal with booking information
 */
/**
 * Open the appointment summary modal with booking information
 * @param {Object} data - Booking data object (from dataset or constructed)
 */
function openAppointmentSummary(data) {
    // Extract data from the object (could be dataset or plain object)
    const bookingId = data.id || data.bookingId;
    const code = data.code;
    const serviceName = data.serviceName;
    const churchName = data.churchName;
    const churchAddress = data.churchAddress;
    const churchEmail = data.churchEmail;
    const churchPhone = data.churchPhone;
    const churchPaypal = data.churchPaypal;
    const date = data.date;
    const time = data.time;
    const statusDisplay = data.statusDisplay;
    const status = data.status;
    const createdDate = data.createdDate;
    const updatedDate = data.updatedDate;
    const userName = data.userName;
    const userEmail = data.userEmail;
    const userPhone = data.userPhone;
    const userAddress = data.userAddress;
    const notes = data.notes;
    const servicePrice = data.servicePrice;
    const isFree = data.isFree === 'true' || data.isFree === true; // Handle string 'true' from dataset
    const paymentStatus = data.paymentStatus;
    const paymentAmount = data.paymentAmount;
    const paymentMethod = data.paymentMethod;
    const paymentDate = data.paymentDate;
    const paymentTransactionId = data.paymentTransactionId;
    const categoryName = data.categoryName;
    const categoryIcon = data.categoryIcon;
    const categoryColor = data.categoryColor;
    const declineReason = data.declineReason;
    const handlerName = data.handlerName;
    const timeSlot = data.timeSlot;
    const eventDate = data.eventDate;
    const eventTime = data.eventTime;
    const eventTimeSlot = data.eventTimeSlot;
    const pastorName = data.pastorName;

    // Store current booking info for cancel functionality
    currentBookingId = bookingId;

    // Basic info
    document.getElementById('summary-code').textContent = code;
    document.getElementById('summary-service').textContent = serviceName;

    // Date and Time - only show if actually set
    const dateRow = document.getElementById('summary-date-row');
    const timeRow = document.getElementById('summary-time-row');
    const dateEl = document.getElementById('summary-date');
    const timeEl = document.getElementById('summary-time');

    if (dateEl && date && date.trim() && date.trim() !== 'Not set' && date.trim() !== 'None') {
        dateEl.textContent = date;
        if (dateRow) dateRow.style.display = 'table-row';
    } else if (dateRow) {
        dateRow.style.display = 'none';
    }

    if (timeEl && time && time.trim() && time.trim() !== 'Not set' && time.trim() !== 'None') {
        timeEl.textContent = time;
        if (timeRow) timeRow.style.display = 'table-row';
    } else if (timeEl && timeSlot && timeSlot.trim()) {
        timeEl.textContent = timeSlot;
        if (timeRow) timeRow.style.display = 'table-row';
    } else if (timeRow) {
        timeRow.style.display = 'none';
    }

    // Pastor info
    const pastorRow = document.getElementById('summary-pastor-row');
    const pastorEl = document.getElementById('summary-pastor');
    if (pastorRow && pastorEl) {
        if (pastorName && pastorName.trim()) {
            pastorEl.textContent = pastorName;
            pastorRow.style.display = 'table-row';
        } else {
            pastorRow.style.display = 'none';
        }
    }

    // Event Date and Time
    const eventDateRow = document.getElementById('summary-event-date-row');
    const eventTimeRow = document.getElementById('summary-event-time-row');
    const eventDateEl = document.getElementById('summary-event-date');
    const eventTimeEl = document.getElementById('summary-event-time');

    if (eventDateRow && eventDateEl) {
        if (eventDate && eventDate.trim()) {
            eventDateEl.textContent = eventDate;
            eventDateRow.style.display = 'table-row';
        } else {
            eventDateRow.style.display = 'none';
        }
    }

    if (eventTimeRow && eventTimeEl) {
        if (eventTime && eventTime.trim()) {
            eventTimeEl.textContent = eventTime;
            eventTimeRow.style.display = 'table-row';
        } else if (eventTimeSlot && eventTimeSlot.trim()) {
            eventTimeEl.textContent = eventTimeSlot;
            eventTimeRow.style.display = 'table-row';
        } else {
            eventTimeRow.style.display = 'none';
        }
    }
    const createdDateEl = document.getElementById('summary-created');
    const updatedDateEl = document.getElementById('summary-updated');
    if (createdDateEl) createdDateEl.textContent = createdDate;
    if (updatedDateEl) updatedDateEl.textContent = updatedDate;

    // Handler name for signature
    const handlerNameEl = document.getElementById('summary-handler-name');
    if (handlerNameEl && handlerName && handlerName.trim()) {
        handlerNameEl.textContent = handlerName;
    } else if (handlerNameEl) {
        handlerNameEl.textContent = 'Parish Administrator';
    }

    // Category badge
    const categoryRow = document.getElementById('summary-category-row');
    const categoryBadge = document.getElementById('summary-category-badge');
    const categoryNameEl = document.getElementById('summary-category-name');
    const categoryIconEl = document.getElementById('summary-category-icon');
    const hasCategory = categoryName && categoryName.trim().length > 0;

    if (categoryRow && categoryBadge) {
        if (hasCategory) {
            const color = (categoryColor && categoryColor.trim()) ? categoryColor.trim() : '#3B82F6';
            categoryRow.style.display = 'table-row';
            categoryBadge.style.display = 'inline-flex';
            categoryBadge.style.backgroundColor = color + '20';
            categoryBadge.style.borderColor = color + '40';
            categoryBadge.style.color = color;
            if (categoryNameEl) categoryNameEl.textContent = categoryName;
            if (categoryIconEl) categoryIconEl.textContent = (categoryIcon && categoryIcon.trim()) ? categoryIcon : '📁';
        } else {
            categoryRow.style.display = 'none';
            categoryBadge.style.display = 'none';
        }
    }

    // Church info
    const churchNameEl = document.getElementById('summary-church');
    const churchAddressEl = document.getElementById('summary-church-address');
    const churchEmailEl = document.getElementById('summary-church-email');
    const churchPhoneEl = document.getElementById('summary-church-phone');
    
    if (churchNameEl) churchNameEl.textContent = churchName;
    if (churchAddressEl) churchAddressEl.textContent = churchAddress || 'Address not available';
    if (churchEmailEl) churchEmailEl.textContent = churchEmail ? `Email: ${churchEmail}` : '';
    if (churchPhoneEl) churchPhoneEl.textContent = churchPhone ? `Phone: ${churchPhone}` : '';

    // User info
    const userNameEl = document.getElementById('summary-user-name');
    const userEmailEl = document.getElementById('summary-user-email');
    const userPhoneEl = document.getElementById('summary-user-phone');
    const userAddressEl = document.getElementById('summary-user-address');
    
    if (userNameEl) userNameEl.textContent = userName;
    if (userEmailEl) userEmailEl.textContent = `Email: ${userEmail}`;
    if (userPhoneEl) userPhoneEl.textContent = userPhone ? `Phone: ${userPhone}` : '';
    if (userAddressEl) userAddressEl.textContent = userAddress && userAddress.trim() ? userAddress.trim() : 'Address not provided';

    // Notes
    const notesSection = document.getElementById('summary-notes-section');
    const notesContent = document.getElementById('summary-notes');
    if (notesContent && notes && notes.trim()) {
        notesContent.textContent = notes;
        if (notesSection) notesSection.style.display = 'block';
    } else if (notesSection) {
        notesSection.style.display = 'none';
    }

    // Decline Reason
    const declineReasonSection = document.getElementById('summary-decline-reason-section');
    const declineReasonContent = document.getElementById('summary-decline-reason');
    if (declineReasonContent && status === 'declined' && declineReason && declineReason.trim()) {
        declineReasonContent.textContent = declineReason;
        if (declineReasonSection) declineReasonSection.style.display = 'block';
    } else if (declineReasonSection) {
        declineReasonSection.style.display = 'none';
    }

    // Requirements
    const requirements = data.requirements;
    const requirementsSection = document.getElementById('summary-requirements-section');
    const requirementsList = document.getElementById('summary-requirements-list');
    if (requirementsList && requirements && requirements.trim()) {
        requirementsList.innerHTML = '';
        const reqLines = requirements.split('\n').filter(line => line.trim());
        reqLines.forEach(req => {
            const li = document.createElement('li');
            li.textContent = req.trim();
            li.style.marginBottom = '4px';
            requirementsList.appendChild(li);
        });
        if (requirementsSection) requirementsSection.style.display = reqLines.length > 0 ? 'block' : 'none';
    } else if (requirementsSection) {
        requirementsSection.style.display = 'none';
    }

    // Preparation Notes
    const preparationNotes = data.preparationNotes;
    const prepNotesSection = document.getElementById('summary-preparation-notes-section');
    const prepNotesContent = document.getElementById('summary-preparation-notes');
    if (prepNotesContent && preparationNotes && preparationNotes.trim()) {
        prepNotesContent.textContent = preparationNotes;
        if (prepNotesSection) prepNotesSection.style.display = 'block';
    } else if (prepNotesSection) {
        prepNotesSection.style.display = 'none';
    }

    // Cancellation Policy
    const cancellationPolicy = data.cancellationPolicy;
    const cancelPolicySection = document.getElementById('summary-cancellation-policy-section');
    const cancelPolicyContent = document.getElementById('summary-cancellation-policy');
    if (cancelPolicyContent && cancellationPolicy && cancellationPolicy.trim()) {
        cancelPolicyContent.textContent = cancellationPolicy;
        if (cancelPolicySection) cancelPolicySection.style.display = 'block';
    } else if (cancelPolicySection) {
        cancelPolicySection.style.display = 'none';
    }

    // Store service price and free status
    currentServicePrice = parseFloat(servicePrice) || 0;
    currentServiceIsFree = isFree;

    // Payment Information
    const paymentStatusEl = document.getElementById('summary-payment-status');
    const paymentAmountEl = document.getElementById('summary-payment-amount');
    const paymentMethodEl = document.getElementById('summary-payment-method');
    const paymentDateEl = document.getElementById('summary-payment-date');
    const paymentTransactionEl = document.getElementById('summary-payment-transaction');

    // Set payment status with color
    if (paymentStatusEl) {
        if (paymentStatus === 'paid') {
            paymentStatusEl.innerHTML = '<span style="color:#16a34a; font-weight:600;">✓ Paid</span>';
        } else if (paymentStatus === 'pending') {
            paymentStatusEl.innerHTML = '<span style="color:#ca8a04; font-weight:600;">⏳ Pending</span>';
        } else if (paymentStatus === 'failed') {
            paymentStatusEl.innerHTML = '<span style="color:#dc2626; font-weight:600;">✗ Failed</span>';
        } else if (paymentStatus === 'canceled') {
            paymentStatusEl.innerHTML = '<span style="color:#6b7280; font-weight:600;">✗ Canceled</span>';
        } else if (paymentStatus === 'refunded') {
            paymentStatusEl.innerHTML = '<span style="color:#3b82f6; font-weight:600;">↩ Refunded</span>';
        } else {
            paymentStatusEl.textContent = paymentStatus || 'N/A';
        }
    }

    // Set payment amount
    if (paymentAmountEl) paymentAmountEl.textContent = '₱' + (parseFloat(paymentAmount) || 0).toFixed(2);

    // Show/hide additional payment details based on status
    const methodRow = document.getElementById('summary-payment-method-row');
    const paymentDateRow = document.getElementById('summary-payment-date-row');
    const transactionRow = document.getElementById('summary-payment-transaction-row');

    if (paymentStatus === 'paid') {
        // Show payment method
        if (paymentMethod && paymentMethodEl) {
            paymentMethodEl.textContent = paymentMethod;
            if (methodRow) methodRow.style.display = 'table-row';
        } else if (methodRow) {
            methodRow.style.display = 'none';
        }

        // Show payment date
        if (paymentDate && paymentDateEl) {
            paymentDateEl.textContent = paymentDate;
            if (paymentDateRow) paymentDateRow.style.display = 'table-row';
        } else if (paymentDateRow) {
            paymentDateRow.style.display = 'none';
        }

        // Show transaction ID
        if (paymentTransactionId && paymentTransactionEl) {
            paymentTransactionEl.textContent = paymentTransactionId;
            if (transactionRow) transactionRow.style.display = 'table-row';
        } else if (transactionRow) {
            transactionRow.style.display = 'none';
        }
    } else {
        if (methodRow) methodRow.style.display = 'none';
        if (paymentDateRow) paymentDateRow.style.display = 'none';
        if (transactionRow) transactionRow.style.display = 'none';
    }

    // Payment section - show only for requested status and paid services
    const paymentSection = document.getElementById('summary-payment-section');
    if (paymentSection && status === 'requested' && !currentServiceIsFree && currentServicePrice > 0 && paymentStatus !== 'paid') {
        paymentSection.style.display = 'block';
        currentBookingId = bookingId;

        // Initialize PayPal button
        initializePayPalButton(bookingId, churchPaypal);

        // Initialize Stripe (will be done when user switches to Stripe tab)
    } else if (paymentSection) {
        paymentSection.style.display = 'none';
    }

    // Hide print button for canceled or declined bookings
    const printBtn = document.getElementById('print-summary-btn');
    const modalFooter = document.getElementById('summary-footer');

    if (status === 'canceled' || status === 'cancelled' || status === 'declined') {
        if (printBtn) {
            printBtn.style.setProperty('display', 'none', 'important');
            printBtn.disabled = true;
        }
        // Make close button full width when print is hidden
        if (modalFooter) {
            modalFooter.style.justifyContent = 'center';
        }
    } else {
        if (printBtn) {
            printBtn.style.setProperty('display', 'block', 'important');
            printBtn.disabled = false;
        }
        if (modalFooter) {
            modalFooter.style.justifyContent = 'space-between';
        }
    }

    // Set status badge
    const statusBadge = document.getElementById('summary-status-badge');
    if (statusBadge) {
        statusBadge.textContent = statusDisplay;
        statusBadge.className = 'badge badge-' + status;
    }

    // Normalize status for comparisons
    const normalizedStatus = (status || '').toString().trim().toLowerCase();

    // Show/hide cancel button based on status (only for pending/requested, not canceled/approved/declined/completed)
    const cancelBtn = document.getElementById('cancel-booking-btn');
    if (cancelBtn) {
        const cancellableStatuses = ['pending', 'requested'];
        const nonCancellableStatuses = ['canceled', 'cancelled', 'approved', 'declined', 'completed'];

        // Explicitly hide for non-cancellable statuses; use !important to override CSS
        if (nonCancellableStatuses.includes(normalizedStatus)) {
            cancelBtn.style.setProperty('display', 'none', 'important');
        } else if (cancellableStatuses.includes(normalizedStatus)) {
            cancelBtn.style.setProperty('display', 'flex', 'important');
        } else {
            // Default to hide if status is unknown
            cancelBtn.style.setProperty('display', 'none', 'important');
        }
    }

    const modal = document.getElementById('appointmentSummaryModal');
    if (modal) modal.style.display = 'flex';

    // Re-initialize Feather icons for the modal
    setTimeout(() => {
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }, 100);
}

/**
 * Close the appointment summary modal
 */
function closeAppointmentSummary() {
    document.getElementById('appointmentSummaryModal').style.display = 'none';
}

/**
 * Print the appointment summary
 */
function printAppointmentSummary() {
    // Get the modal body content
    const modalBody = document.querySelector('#appointmentSummaryModal .modal-body');
    const paymentSection = document.getElementById('summary-payment-section');

    if (!modalBody) return;

    // Clone the content
    const printContent = modalBody.cloneNode(true);

    // Remove payment method section from clone
    const clonedPaymentSection = printContent.querySelector('#summary-payment-section');
    if (clonedPaymentSection) {
        clonedPaymentSection.remove();
    }

    // Create a new window for printing
    const printWindow = window.open('', '_blank');

    // Write the content
    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Appointment Confirmation - Print</title>
            <style>
                @page {
                    margin: 0.5in;
                }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: white;
                }
                
                * {
                    box-sizing: border-box;
                }
                
                .invoice-header {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 30px;
                    padding-bottom: 20px;
                    border-bottom: 2px solid #e5e7eb;
                }
                
                .invoice-title {
                    font-size: 28px;
                    font-weight: 700;
                    margin: 0 0 10px 0;
                }
                
                .invoice-parties {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 30px;
                    margin-bottom: 30px;
                }
                
                .party-box {
                    padding: 20px;
                    background: #f9fafb;
                    border-radius: 8px;
                }
                
                .party-title {
                    font-size: 12px;
                    font-weight: 600;
                    color: #6b7280;
                    margin: 0 0 10px 0;
                }
                
                .party-name {
                    font-size: 16px;
                    font-weight: 600;
                    margin-bottom: 5px;
                }
                
                .party-detail {
                    font-size: 14px;
                    color: #6b7280;
                    margin: 3px 0;
                }
                
                .invoice-details {
                    margin-bottom: 30px;
                }
                
                .section-title {
                    font-size: 14px;
                    font-weight: 600;
                    color: #374151;
                    margin: 0 0 15px 0;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
                
                .details-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                
                .details-table tr {
                    border-bottom: 1px solid #e5e7eb;
                }
                
                .details-table td {
                    padding: 12px 0;
                }
                
                .detail-label {
                    font-weight: 600;
                    color: #6b7280;
                    width: 200px;
                }
                
                .detail-value {
                    color: #111827;
                }
                
                .invoice-notes {
                    margin-top: 30px;
                    padding: 20px;
                    background: #f9fafb;
                    border-radius: 8px;
                }
                
                .notes-content {
                    margin: 10px 0 0 0;
                    color: #374151;
                }
                
                .invoice-footer-note {
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #e5e7eb;
                    font-size: 12px;
                    color: #6b7280;
                }
                
                .badge {
                    display: inline-block;
                    padding: 4px 12px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                }
                
                /* Remove inline styles for print - clean text only */
                #summary-category-badge,
                #summary-payment-status span {
                    background: none !important;
                    border: none !important;
                    color: #111827 !important;
                    padding: 0 !important;
                    font-weight: 500 !important;
                }
                
                /* Hide emoji icons in print */
                #summary-category-icon,
                #summary-payment-status span::before {
                    display: none !important;
                }
            </style>
        </head>
        <body>
            ${printContent.innerHTML}
        </body>
        </html>
    `);

    printWindow.document.close();

    // Wait for content to load, then print
    printWindow.onload = function () {
        printWindow.focus();
        printWindow.print();
        printWindow.close();
    };
}

/**
 * Switch between payment method tabs
 */
function switchPaymentTab(method) {
    // Update tab buttons
    document.querySelectorAll('.payment-tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-method="${method}"]`).classList.add('active');

    // Show/hide payment sections
    const paypalSection = document.getElementById('paypal-booking-section');
    const stripeSection = document.getElementById('stripe-booking-section');

    if (method === 'paypal') {
        paypalSection.style.display = 'block';
        stripeSection.style.display = 'none';
    } else if (method === 'stripe') {
        paypalSection.style.display = 'none';
        stripeSection.style.display = 'block';

        // Initialize Stripe if not already done
        if (!stripeCardElement && currentBookingId) {
            initializeStripeElement();
        }
    }

    // Re-initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

/**
 * Initialize PayPal button for booking payment
 */
function initializePayPalButton(bookingId, churchPaypal) {
    const container = document.getElementById('paypal-booking-button');
    if (!container) return;

    // Clear existing button
    container.innerHTML = '';

    if (typeof paypal === 'undefined') {
        container.innerHTML = '<p style="color: #DC2626;">PayPal SDK not loaded. Please refresh the page.</p>';
        return;
    }

    paypal.Buttons({
        createOrder: function (data, actions) {
            // Call backend to create PayPal order with service price
            return fetch(`/app/api/booking/${bookingId}/payment/create/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `amount=${currentServicePrice.toFixed(2)}`
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        return data.order_id;
                    } else {
                        throw new Error(data.message || 'Failed to create order');
                    }
                })
                .catch(error => {
                    console.error('Error creating order:', error);
                    document.getElementById('booking-payment-error').textContent = error.message;
                    document.getElementById('booking-payment-error').style.display = 'block';
                    throw error;
                });
        },
        onApprove: function (data, actions) {
            // Call backend to capture payment
            return fetch(`/app/api/booking/${bookingId}/payment/capture/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `order_id=${data.orderID}`
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Payment successful! Your booking has been updated.');
                        window.location.reload();
                    } else {
                        throw new Error(data.message || 'Payment failed');
                    }
                })
                .catch(error => {
                    console.error('Error capturing payment:', error);
                    document.getElementById('booking-payment-error').textContent = error.message;
                    document.getElementById('booking-payment-error').style.display = 'block';
                });
        },
        onError: function (err) {
            console.error('PayPal error:', err);
            document.getElementById('booking-payment-error').textContent = 'Payment failed. Please try again.';
            document.getElementById('booking-payment-error').style.display = 'block';
        }
    }).render('#paypal-booking-button');
}

/**
 * Initialize Stripe card element
 */
function initializeStripeElement() {
    if (typeof Stripe === 'undefined') {
        console.error('Stripe.js not loaded');
        return;
    }

    const stripeKey = window.STRIPE_PUBLISHABLE_KEY;
    if (!stripeKey) {
        console.error('Stripe publishable key not found');
        return;
    }

    stripe = Stripe(stripeKey);
    stripeElements = stripe.elements();

    stripeCardElement = stripeElements.create('card', {
        style: {
            base: {
                fontSize: '16px',
                color: '#32325d',
                fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        }
    });

    stripeCardElement.mount('#stripe-booking-card');

    // Handle card errors
    stripeCardElement.on('change', function (event) {
        const errorElement = document.getElementById('stripe-booking-errors');
        if (event.error) {
            errorElement.textContent = event.error.message;
            errorElement.style.display = 'block';
        } else {
            errorElement.style.display = 'none';
        }
    });

    // Handle payment button click
    const submitBtn = document.getElementById('stripe-booking-btn');
    if (submitBtn) {
        submitBtn.onclick = async function () {
            const btn = this;
            const btnText = btn.querySelector('span');
            const originalText = btnText.textContent;

            try {
                // Disable button
                btn.disabled = true;
                btnText.textContent = 'Processing...';

                // Create payment intent with service price
                const response = await fetch(`/app/api/booking/${currentBookingId}/payment/stripe/create/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: `amount=${currentServicePrice.toFixed(2)}`
                });

                const data = await response.json();

                if (!data.success) {
                    throw new Error(data.message || 'Failed to create payment');
                }

                // Confirm payment with Stripe
                const result = await stripe.confirmCardPayment(data.client_secret, {
                    payment_method: {
                        card: stripeCardElement
                    }
                });

                if (result.error) {
                    throw new Error(result.error.message);
                }

                // Confirm payment on backend
                const confirmResponse = await fetch(`/app/api/booking/${currentBookingId}/payment/stripe/confirm/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: `payment_intent_id=${result.paymentIntent.id}`
                });

                const confirmData = await confirmResponse.json();

                if (confirmData.success) {
                    alert('Payment successful! Your booking has been updated.');
                    window.location.reload();
                } else {
                    throw new Error(confirmData.message || 'Payment confirmation failed');
                }

            } catch (error) {
                console.error('Stripe payment error:', error);
                document.getElementById('stripe-booking-errors').textContent = error.message;
                document.getElementById('stripe-booking-errors').style.display = 'block';

                // Re-enable button
                btn.disabled = false;
                btnText.textContent = originalText;
            }
        };
    }
}

/**
 * Get CSRF token from cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Open the review modal with service information
 * @param {number} serviceId - ID of the service to review
 * @param {string} serviceName - Name of the service
 * @param {string} churchName - Name of the church
 * @param {number} bookingId - ID of the booking
 */
function openReviewModal(serviceId, serviceName, churchName, bookingId) {
    currentServiceId = serviceId;
    
    const modalServiceName = document.getElementById('modal-service-name');
    const modalChurchName = document.getElementById('modal-church-name');
    const modal = document.getElementById('reviewModal');
    
    if (modalServiceName) modalServiceName.textContent = serviceName;
    if (modalChurchName) modalChurchName.textContent = 'at ' + churchName;

    if (modal) modal.style.setProperty('display', 'flex', 'important');

    // Reset form
    const reviewForm = document.getElementById('reviewForm');
    const modalRating = document.getElementById('modal-rating');
    if (reviewForm) reviewForm.reset();
    if (modalRating) modalRating.value = '';

    // Reset stars
    const stars = document.querySelectorAll('.star-rating-modal .star');
    stars.forEach(star => star.classList.remove('filled'));
}

/**
 * Close the review modal and reset state
 */
function closeReviewModal() {
    document.getElementById('reviewModal').style.display = 'none';
    currentServiceId = null;
}

/**
 * Initialize modal event listeners and star rating functionality
 */
function initializeReviewModal() {
    const modal = document.getElementById('reviewModal');
    const stars = document.querySelectorAll('.star-rating-modal .star');
    const reviewForm = document.getElementById('reviewForm');

    // Check if modal exists before adding event listeners
    if (!modal) {
        console.warn('Review modal not found in DOM');
        return;
    }

    // Close modal when clicking outside
    modal.addEventListener('click', function (e) {
        if (e.target === this) {
            closeReviewModal();
        }
    });

    // Star rating click handlers
    stars.forEach((star, index) => {
        star.addEventListener('click', function () {
            const rating = index + 1;
            document.getElementById('modal-rating').value = rating;

            // Update visual stars
            updateStarDisplay(rating);
        });

        star.addEventListener('mouseenter', function () {
            const rating = index + 1;
            updateStarPreview(rating);
        });
    });

    // Reset star display on mouse leave
    const starRatingModal = document.querySelector('.star-rating-modal');
    if (starRatingModal) {
        starRatingModal.addEventListener('mouseleave', function () {
            const currentRating = parseInt(document.getElementById('modal-rating').value) || 0;
            updateStarDisplay(currentRating);
        });
    }

    // Form submission handler
    if (reviewForm) {
        reviewForm.addEventListener('submit', handleReviewSubmission);
    }
}

/**
 * Update star display based on rating
 * @param {number} rating - Rating value (1-5)
 */
function updateStarDisplay(rating) {
    const stars = document.querySelectorAll('.star-rating-modal .star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('filled');
            star.style.color = '#fbbf24';
        } else {
            star.classList.remove('filled');
            star.style.color = '#d1d5db';
        }
    });
}

/**
 * Update star preview on hover
 * @param {number} rating - Rating value (1-5)
 */
function updateStarPreview(rating) {
    const stars = document.querySelectorAll('.star-rating-modal .star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.style.color = '#fbbf24';
        } else {
            star.style.color = '#d1d5db';
        }
    });
}

/**
 * Validate review form data
 * @param {string} rating - Rating value
 * @param {string} title - Review title
 * @param {string} comment - Review comment
 * @returns {Object} Validation result with isValid flag and message
 */
function validateReviewForm(rating, title, comment) {
    if (!rating || rating < 1 || rating > 5) {
        return {
            isValid: false,
            message: 'Please provide a rating between 1 and 5 stars.'
        };
    }

    if (!title || title.length < 5) {
        return {
            isValid: false,
            message: 'Please provide a review title with at least 5 characters.'
        };
    }

    if (!comment || comment.length < 10) {
        return {
            isValid: false,
            message: 'Please provide a review comment with at least 10 characters.'
        };
    }

    return { isValid: true };
}

/**
 * Handle review form submission
 * @param {Event} e - Form submission event
 */
function handleReviewSubmission(e) {
    e.preventDefault();

    if (!currentServiceId) {
        alert('Error: No service selected');
        return;
    }

    // Get form data
    const rating = document.getElementById('modal-rating').value;
    const title = document.getElementById('modal-title').value.trim();
    const comment = document.getElementById('modal-comment').value.trim();

    // Validate form data
    const validation = validateReviewForm(rating, title, comment);
    if (!validation.isValid) {
        alert(validation.message);
        return;
    }

    const formData = new FormData(e.target);
    const submitButton = e.target.querySelector('button[type="submit"]');

    // Update button state
    submitButton.disabled = true;
    submitButton.textContent = 'Submitting...';

    // Submit review
    submitReview(formData, submitButton);
}

/**
 * Submit review to server
 * @param {FormData} formData - Form data to submit
 * @param {HTMLElement} submitButton - Submit button element
 */
function submitReview(formData, submitButton) {
    // Debug form data
    console.log('Form data being sent:');
    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }

    // Construct review URL using Django template variable
    const reviewUrl = window.djangoUrls.createReviewUrl.replace('0', currentServiceId);
    console.log('Submitting to URL:', reviewUrl);

    fetch(reviewUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
        .then(response => {
            console.log('Response status:', response.status);

            if (!response.ok) {
                return response.text().then(text => {
                    console.error('Server response:', text);
                    throw new Error(`HTTP ${response.status}: ${text}`);
                });
            }

            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            if (data.success) {
                alert('Thank you for your review!');
                closeReviewModal();
                // Refresh the page to show updated button state
                location.reload();
            } else {
                alert('Error submitting review: ' + (data.message || 'Please try again'));
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            alert('Error submitting review: ' + error.message);
        })
        .finally(() => {
            // Re-enable submit button
            submitButton.disabled = false;
            submitButton.textContent = 'Submit Review';
        });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    initializeReviewModal();
    initializeAppointmentSummaryModal();
});

/**
 * Initialize appointment summary modal event listeners
 */
function initializeAppointmentSummaryModal() {
    const modal = document.getElementById('appointmentSummaryModal');

    // Ensure modal exists and is hidden on page load
    if (modal) {
        modal.style.display = 'none';

        // Close modal when clicking outside
        modal.addEventListener('click', function (e) {
            if (e.target === this) {
                closeAppointmentSummary();
            }
        });
    } else {
        console.warn('Appointment summary modal not found in DOM');
    }
}

/**
 * Open cancel booking confirmation modal from summary
 */
function confirmCancelBookingFromSummary() {
    const code = document.getElementById('summary-code').textContent;
    const serviceName = document.getElementById('summary-service').textContent;

    // Close summary modal first
    closeAppointmentSummary();

    // Open cancel confirmation modal
    confirmCancelBooking(currentBookingId, code, serviceName);
}

/**
 * Open cancel booking confirmation modal
 */
function confirmCancelBooking(bookingId, code, serviceName) {
    cancelBookingId = bookingId;
    document.getElementById('cancel-booking-code').textContent = code;
    document.getElementById('cancel-booking-service').textContent = serviceName;
    document.getElementById('cancelBookingModal').style.display = 'flex';

    // Re-initialize Feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

/**
 * Close cancel booking modal
 */
function closeCancelModal() {
    document.getElementById('cancelBookingModal').style.display = 'none';
    cancelBookingId = null;
}

/**
 * Cancel the booking
 */
function cancelBooking() {
    if (!cancelBookingId) return;

    const btn = document.getElementById('confirm-cancel-btn');
    btn.disabled = true;
    btn.textContent = 'Cancelling...';

    fetch(`/app/cancel-booking/${cancelBookingId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || 'Failed to cancel booking');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Hide the cancel button immediately in the summary modal (if still open later)
                const summaryCancelBtn = document.getElementById('cancel-booking-btn');
                if (summaryCancelBtn) summaryCancelBtn.style.setProperty('display', 'none', 'important');

                closeCancelModal();
                // Show success message
                alert('Booking cancelled successfully!');
                // Reload page to update the list
                window.location.reload();
            } else {
                alert(data.message || 'Failed to cancel booking. Please try again.');
                btn.disabled = false;
                btn.textContent = 'Yes, Cancel Booking';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message || 'An error occurred. Please try again.');
            btn.disabled = false;
            btn.textContent = 'Yes, Cancel Booking';
        });
}

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Switch between payment method tabs (PayPal/Stripe)
 */
function switchPaymentTab(method) {
    document.querySelectorAll('.payment-tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-method') === method) {
            btn.classList.add('active');
        }
    });

    if (method === 'paypal') {
        document.getElementById('paypal-booking-section').style.display = 'block';
        document.getElementById('stripe-booking-section').style.display = 'none';
    } else {
        document.getElementById('paypal-booking-section').style.display = 'none';
        document.getElementById('stripe-booking-section').style.display = 'block';
        if (!stripeCardElement) {
            initializeStripe();
        }
    }
}

/**
 * Print the appointment summary
 */
function printAppointmentSummary() {
    window.print();
}

// Expose functions globally for inline event handlers
window.openReviewModal = openReviewModal;
window.closeReviewModal = closeReviewModal;
window.openAppointmentSummary = openAppointmentSummary;
window.closeAppointmentSummary = closeAppointmentSummary;
window.confirmCancelBooking = confirmCancelBooking;
window.confirmCancelBookingFromSummary = confirmCancelBookingFromSummary;
window.closeCancelModal = closeCancelModal;
window.cancelBooking = cancelBooking;
window.switchPaymentTab = switchPaymentTab;
window.printAppointmentSummary = printAppointmentSummary;
