from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Church, BookableService, Booking
from django.utils import timezone
import datetime

User = get_user_model()

class BookingFlowTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@church.com',
            password='testpass123',
            first_name='Admin',
            last_name='One'
        )
        
        self.church = Church.objects.create(
            name='Test Church',
            slug='test-church',
            owner=self.admin_user
        )
        
        self.service = BookableService.objects.create(
            name='Test Service',
            church=self.church,
            duration=60,
            price=100.00
        )
        
    def test_booking_request_flow(self):
        """Test the full booking flow: Request -> Approve -> Verify -> Schedule"""
        
        # 1. User submits request (no date/time)
        self.client.login(username='testuser', password='testpass123')
        url = reverse('core:submit_booking_request', kwargs={'service_id': self.service.id})
        response = self.client.post(url, {
            'notes': 'I want to book this service.'
        })
        # Should redirect to appointments page
        self.assertEqual(response.status_code, 302)
        
        # Verify booking created with correct status
        booking = Booking.objects.first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.service, self.service)
        self.assertEqual(booking.status, Booking.STATUS_REQUESTED)
        self.assertIsNone(booking.date)
        
        # 2. Admin approves request and asks for requirements
        self.client.logout()
        self.client.login(username='adminuser', password='testpass123')
        
        url = reverse('core:admin_approve_request_requirements', kwargs={'booking_id': booking.id})
        response = self.client.post(url, {'notes': 'Please bring your birth certificate.'})
        
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data['success'])
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.STATUS_PENDING_REQUIREMENTS)
        self.assertEqual(booking.form_approval_notes, 'Please bring your birth certificate.')
        
        # 3. Admin verifies requirements (simulating user submitted them offline or via other means)
        url = reverse('core:admin_verify_requirements', kwargs={'booking_id': booking.id})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.STATUS_READY_TO_SCHEDULE)
        
        # 4. User schedules the date
        self.client.logout()
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('core:schedule_booking_date', kwargs={'booking_id': booking.id})
        tomorrow = timezone.now().date() + datetime.timedelta(days=1)
        response = self.client.post(url, {
            'date': tomorrow,
            'start_time': '10:00'
        })
        
        self.assertEqual(response.status_code, 302) # Redirects to appointments
        
        booking.refresh_from_db()
        self.assertEqual(booking.status, Booking.STATUS_SCHEDULED)
        self.assertEqual(booking.date, tomorrow)
        self.assertEqual(booking.start_time.strftime('%H:%M'), '10:00')
