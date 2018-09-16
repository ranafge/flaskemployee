import unittest
from flask_testing import TestCase
from flask import render_template, redirect, url_for, abort
from app import create_app, db
from app.models import Employee, Department, Role

class TestBase(TestCase):
    def create_app(self):
        config_name='testing'
        app = create_app(config_name)
        app.config.update(
             SQLALCHEMY_DATABASE_URI='mysql://dt_admin:dt2016@localhost/dreamteam_test'
        )
        return app

    def setUp(self):
        db.create_all()
        admin = Employee(username="admin", password="admin2016", is_admin=True)
        employee =  Employee(username="test_user", password="test2016")
        db.session.add(admin)
        db.session.add(employee)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestModels(TestCase):
    def test_employee_model(self):
        self.assertEqual(Employee.query.count(),6)
    def test_department_model(self):
        department = Department(name='IT',description='The IT Department')
        db.session.add(department)
        db.session.commit()
        self.assertEqual(Department.query.count(),1)
    def test_role_model(self):
        role = Role(name='CEO', description='Run the whole company.')
        db.session.add(role)
        db.session.commit()
        self.assertEqual(Role.query.count(),1)

class Testviews(TestBase):
    def test_homepage_view(self):
        response = self.client.get(url_for('home.homepage'))
        self.assertEqual(response.status_code, 200)
    def test_login_view(self):
        response = self.client.get(url_for('auth.login'))
        self.assertEqual(response.status_code, 200)
    def test_logout_view(self):
        target_url = url_for('auth.logout')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response, redirect_url)
    def test_dashboard_view(self):
        target_url = url_for('home.dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_admin_dashboard_view(self):
        target_url = url_for('home.admin_dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_departments_view(self):
        target_url = url_for('admin.list_departments')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_roles_view(self):
        target_url = url_for('admin.list_roles')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_employees_view(self):
        target_url = url_for('admin.list_employees')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

class TestErrorPages(TestBase):
    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client.get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client.get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)


if __name__=="__main__":
    unittest.main()
