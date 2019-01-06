from django.test import TestCase, Client

# Create your tests here.

class TestRegister(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register(self):
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
