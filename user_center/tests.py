from django.test import TestCase, Client
from register.views import hash_code
from django.contrib.auth.models import User
from login.models import UserLogin
from register.models import OrganizerInfo, JudgeInfo

# Create your tests here.

class TestUsercenter_Competitor(TestCase):
    def setUp(self):
        self.client = Client()
        post_data = {}
        post_data['username'] = 'robot'
        post_data['password1'] = 'robotpwd'
        post_data['password2'] = 'robotpwd'
        post_data['email'] = 'robot@robot.com'
        post_data['type'] = 'competitor'
        post_data['captcha_0'] = 'dummy-value'
        post_data['captcha_1'] = 'PASSED'
        response = self.client.post('/register/', data=post_data)
        self.assertEqual(response.context['msg'], '注册成功！')

        post_data['password'] = 'robotpwd'
        response = self.client.post('/login/', data=post_data)
        self.assertNotEqual(response.context['competitionlist'], None)

    def test_myinfo_get(self):
        response = self.client.get('/usercenter/myinfo/')
        self.assertEqual(response.context['username'], 'robot')

    def test_myinfo_post(self):
        post_data = {}
        post_data['Username'] = 'robot'
        post_data['Email'] = 'robot_new@robot.com'
        post_data['Studentnumber'] = '123456'
        post_data['School'] = 'robot_school_new'
        post_data['Grade'] = 'robot_grade_new'
        response = self.client.post('/usercenter/myinfo/', data=post_data)
        self.assertEqual(response.context['email'], 'robot_new@robot.com')

    def test_myconpetition_get(self):
        response = self.client.get('/usercenter/mycompetition/')
        self.assertNotEqual(response.context['competitionlist'], None)

    def test_myteam_get(self):
        response = self.client.get('/usercenter/myteam/')
        self.assertNotEqual(response.context['teamlist'], None)

class TestUsercenter_SuperAdmin(TestCase):
    def setUp(self):
        self.client = Client()
        name = 'robot'
        pwd1 = 'robot'
        user_type = 'superadmin'
        pwd = hash_code(pwd1)
        User.objects.create_user(username=name, password=pwd)
        UserLogin.objects.create(username=name, password=pwd, type=user_type)

        post_data = {}
        post_data['username'] = 'robot'
        post_data['password'] = 'robot'
        post_data['captcha_0'] = 'dummy-value'
        post_data['captcha_1'] = 'PASSED'
        response = self.client.post('/login/', data=post_data)
        self.assertNotEqual(response.context['competitionlist'], None)

    def test_adminlist(self):
        response = self.client.get('/usercenter/superadmin/adminlist')
        self.assertNotEqual(response.context['adminlist'], None)

    def test_addadmin(self):
        post_data = {}
        post_data['adminname'] = 'robotadmin1'
        post_data['adminpwd'] = 'robotadmin1'
        self.client.post('/usercenter/superadmin/adminlist/add', post_data)
        result = UserLogin.objects.get(username='robotadmin1')
        self.assertEqual(result.username, 'robotadmin1')

    def test_deleteadmin(self):
        post_data = {}
        post_data['adminname'] = 'robotadmin1'
        post_data['adminpwd'] = 'robotadmin1'
        self.client.post('/usercenter/superadmin/adminlist/add', post_data)
        result = UserLogin.objects.get(username='robotadmin1')
        self.assertEqual(result.username, 'robotadmin1')

        self.client.post('/usercenter/superadmin/adminlist/delete', post_data)

class TestUsercenter_Admin(TestCase):
    def setUp(self):
        self.client = Client()
        adminname = 'robot'
        password = 'robot'
        pwd = hash_code(password)
        User.objects.create_user(username=adminname, password=pwd)
        UserLogin.objects.create(username=adminname, password=pwd, type='admin')

        post_data = {}
        post_data['username'] = 'robot'
        post_data['password'] = 'robot'
        post_data['captcha_0'] = 'dummy-value'
        post_data['captcha_1'] = 'PASSED'
        response = self.client.post('/login/', data=post_data)
        self.assertNotEqual(response.context['competitionlist'], None)

        name = 'robot_org'
        pwd1 = 'robot'
        pwd = hash_code(pwd1)
        email = 'robot_org@robot.com'
        User.objects.create_user(username=name, password=pwd)
        user_login = UserLogin.objects.create(username=name, password=pwd, type='organizer')
        OrganizerInfo.objects.create(userlogin=user_login, email=email, name=name)

    def test_admin_auth_list(self):
        response = self.client.get('/usercenter/admin/authlist/')
        self.assertNotEqual(response.context['authorganizerlist'], None)

    def test_admin_auth_pass(self):
        post_data = {}
        post_data['checked'] = 'robot_org'
        self.client.post('/usercenter/admin/authlist/pass', post_data)
        auth_organizer = OrganizerInfo.objects.get(name='robot_org')
        self.assertEqual(auth_organizer.authenticationstatus, 1)

    def test_admin_auth_deny(self):
        post_data = {}
        post_data['checked'] = 'robot_org'
        self.client.post('/usercenter/admin/authlist/deny', post_data)
        auth_organizer = OrganizerInfo.objects.get(name='robot_org')
        self.assertEqual(auth_organizer.authenticationstatus, 3)

class TestUsercenter_Organizer(TestCase):
    def setUp(self):
        self.client = Client()
        name = 'robot_org'
        pwd1 = 'robot'
        pwd = hash_code(pwd1)
        email = 'robot_org@robot.com'
        User.objects.create_user(username=name, password=pwd)
        user_login = UserLogin.objects.create(username=name, password=pwd, type='organizer')
        OrganizerInfo.objects.create(userlogin=user_login, email=email, name=name)

        post_data = {}
        post_data['username'] = 'robot_org'
        post_data['password'] = 'robot'
        post_data['captcha_0'] = 'dummy-value'
        post_data['captcha_1'] = 'PASSED'
        response = self.client.post('/login/', data=post_data)
        self.assertNotEqual(response.context['competitionlist'], None)

    def test_organizer_judgelist(self):
        response = self.client.get('/usercenter/judgelist/')
        self.assertNotEqual(response.context['judgelist'], None)

    def test_organizer_judgelist_add(self):
        post_data = {}
        post_data['name'] = 'robotjudge1'
        post_data['pwd'] = 'robotjudge1'
        self.client.post('/usercenter/judgelist/add/', post_data)
        user = UserLogin.objects.get(username='robotjudge1')
        result = JudgeInfo.objects.get(userlogin=user)
        self.assertEqual(result.userlogin.username, 'robotjudge1')

    def test_organizer_judgelist_delete(self):
        post_data = {}
        post_data['name'] = 'robotjudge1'
        post_data['pwd'] = 'robotjudge1'
        self.client.post('/usercenter/judgelist/add/', post_data)
        user = UserLogin.objects.get(username='robotjudge1')
        result = JudgeInfo.objects.get(userlogin=user)
        self.assertEqual(result.userlogin.username, 'robotjudge1')

        post_data = {}
        post_data['name'] = 'robotjudge1'
        self.client.post('/usercenter/judgelist/delete/', post_data)
        user = UserLogin.objects.filter(username='robotjudge1')
        self.assertNotEqual(user, None)