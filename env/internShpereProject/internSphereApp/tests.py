from django.test import TestCase
from .models import CustomUser

class CustomUserTestCase(TestCase):
    def test_create_custom_user(self):
        user = CustomUser.objects.create(username="testuser", user_type="Student")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.user_type, "Student")
from django.test import TestCase
from .models import CustomUser, stud_profile

class StudentProfileTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="student1", user_type="Student")

    def test_create_student_profile(self):
        profile = stud_profile.objects.create(
            user=self.user,
            batch="2023",
            section="A",
            email="student1@example.com",
            phone_number="1234567890",
            department="Computer Science"
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.batch, "2023")
        self.assertEqual(profile.department, "Computer Science")







                           # INTEGRATION TESTS

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import CustomUser, stud_profile, Company, Internship, Application, BiWeeklyReport

class IntegrationTestCase(TestCase):

    def setUp(self):
        # Create users
        self.admin_user = CustomUser.objects.create_user(username='adminuser', password='password123', user_type='Admin')
        self.student_user = CustomUser.objects.create_user(username='studentuser', password='password123', user_type='Student')
        self.company_user = CustomUser.objects.create_user(username='companyuser', password='password123', user_type='Company')

        # Create company
        self.company = Company.objects.create(
            user=self.company_user,
            company_name="Tech Corp",
            company_address="123 Tech Street",
            company_phone="1234567890",
            company_description="A technology company",
            approved=True
        )

        # Create student profile
        self.student_profile = stud_profile.objects.create(
            user=self.student_user,
            batch='2025',
            section='A',
            temporary_password='temp1234',
            profile_completed=True,
            email='student@example.com',
            phone_number='9876543210',
            gender='M',
            year_of_study='3',
            skills='Python, Django, React',
            department='Computer Science',
            resume=None,
            linkedin_profile=None,
            list_of_students=None
        )

        # Create internship
        self.internship = Internship.objects.create(
            company=self.company,
            title="Software Engineering Internship",
            description="A 3-month internship for software development",
            requirement="Basic knowledge of Python and Django",
            location="Remote",
            sector="Computer Science",
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=90),
            deadline=timezone.now().date() + timedelta(days=30),
            posted_on=timezone.now(),
            status='Open'
        )

    def test_student_application_and_biweekly_report(self):
        # Student applies for the internship
        application = Application.objects.create(
            student=self.student_profile,
            internship=self.internship,
            company=self.company,
            status='Pending',
            is_active=True
        )

        # Check application status
        self.assertEqual(application.status, 'Pending')
        self.assertTrue(application.is_active)

        # Create bi-weekly report for the student
        biweekly_report = BiWeeklyReport.objects.create(
            student=self.student_profile,
            company=self.company,
            application_status=application,
            report_number=1,
            week_start=timezone.now().date(),
            week_end=timezone.now().date() + timedelta(weeks=2),
            total_hours_completed=80,
            assignment_responsibilities="Developed features for the company website.",
            critical_analysis="Learned new web development skills.",
            observing_hours=20,
            administrative_hours=10,
            researching_hours=10,
            assisting_hours=20,
            misc_hours=20,
            meetings_discussions="Met with the team to discuss project progress.",
            course_relevance_suggestions="The internship is very relevant to my course.",
            company_approval_status='Pending',
            internship_office_approval_status='Pending',
            department_approval_status='Pending',
            supervisor_approval_status='Pending'
        )

        # Check bi-weekly report creation
        self.assertEqual(biweekly_report.report_number, 1)
        self.assertEqual(biweekly_report.company_approval_status, 'Pending')

    def test_internship_status_expiry(self):
        # Check if the internship status changes when the deadline is passed
        expired_internship = Internship.objects.create(
            company=self.company,
            title="Expired Internship",
            description="This internship has expired.",
            requirement="None",
            location="Remote",
            sector="Computer Science",
            start_date=timezone.now().date() - timedelta(days=60),
            end_date=timezone.now().date() - timedelta(days=30),
            deadline=timezone.now().date() - timedelta(days=1),
            posted_on=timezone.now() - timedelta(days=60),
            status='Open'
        )

        # Simulate the passing of time
        expired_internship.close_if_expired()

        # Check if the status is 'Closed'
        expired_internship.refresh_from_db()
        self.assertEqual(expired_internship.status, 'Closed')

    def test_integration_flow(self):
        # Test the whole flow from application to bi-weekly report
        application = Application.objects.create(
            student=self.student_profile,
            internship=self.internship,
            company=self.company,
            status='Pending',
            is_active=True
        )

        biweekly_report = BiWeeklyReport.objects.create(
            student=self.student_profile,
            company=self.company,
            application_status=application,
            report_number=1,
            week_start=timezone.now().date(),
            week_end=timezone.now().date() + timedelta(weeks=2),
            total_hours_completed=80,
            assignment_responsibilities="Worked on Django project.",
            critical_analysis="Improved my Django skills.",
            observing_hours=10,
            administrative_hours=10,
            researching_hours=20,
            assisting_hours=30,
            misc_hours=10,
            meetings_discussions="Attended team meetings.",
            course_relevance_suggestions="This internship complements my studies well.",
            company_approval_status='Pending',
            internship_office_approval_status='Pending',
            department_approval_status='Pending',
            supervisor_approval_status='Pending'
        )

        # Check bi-weekly report creation and application status
        self.assertEqual(biweekly_report.report_number, 1)
        self.assertEqual(application.status, 'Pending')





from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

class UserRegistrationSystemTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path="C:/WebDrivers/chromedriver.exe")

    def tearDown(self):
        self.driver.quit()

    def test_user_registration(self):
        """Test user registration through the web interface."""
        self.driver.get(self.live_server_url + "/register/")
        
        # Fill in the registration form
        self.driver.find_element(By.NAME, "username").send_keys("student1")
        self.driver.find_element(By.NAME, "password1").send_keys("password")
        self.driver.find_element(By.NAME, "password2").send_keys("password")
        self.driver.find_element(By.NAME, "user_type").send_keys("Student")
        self.driver.find_element(By.NAME, "submit").click()
        
        # Verify registration
        self.assertEqual(self.driver.current_url, self.live_server_url + "/dashboard/")
