from . import admin
from .forms import DepartmentForm, RoleForm
from app import db
from ..models import Department,Role,Employee
from flask_login import current_user, login_required
from flask import abort, render_template, flash, url_for,redirect
from .forms import DepartmentForm, EmployeeAssignForm, RoleForm



def check_admin():
    if not current_user.is_admin:
        abort(403, description="You are not authorize to access this page.")


@admin.route('/departments', methods=['POST','GET'])
@login_required
def list_departments():
    check_admin()
    departments = Department.query.all()
    return render_template('admin/departments/departments.html',\
                           departments=departments, title='Departments')


@admin.route('/department/add', methods=['POST', 'GET'])
@login_required
def add_department():
    check_admin()
    add_department = True
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data, description=form.description.data)
        try:
            db.session.add(department)
            db.session.commit()
            flash('You have successfully added a new department', 'success')
            return redirect(url_for(''))
        except:
            flash('Department name already exists', 'info')
        return redirect(url_for('admin.list_departments'))
    return render_template('admin/departments/department.html',action='Add',\
                           add_department=add_department, form=form, title='Add Department')


@login_required
@admin.route('/departments/edit/<int:id>', methods=['POST', 'GET'])
def edit_department(id):
    check_admin()
    add_department = True
    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('You have successfully edited the department.', 'success')
        return redirect(url_for('admin.list_departments'))
    form.description.data = department.description
    form.name.data = department.name
    return render_template('admin/departments/department.html', action='Edit',\
                           add_department=add_department, department=department, title='Edit Department', form=form)


@admin.route('/departments/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_department(id):
    check_admin()
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    flash('You have successfully deleted the department.', 'info')
    return redirect(url_for('admin.list_departments'))
    return render_template(title="Delete Department")


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    roles = Role.query.all()
    return render_template('admin/roles/roles.html', roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET','POST'])
@login_required
def add_role():
    check_admin()
    add_role = True
    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,description=form.description.data)
        try:
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            flash('Role name already exists.', 'info')
        return redirect(url_for('admin.list_roles'))
    return render_template('admin/roles/role.html', add_role=add_role, form=form, title='Add role')



@admin.route('/roles/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_role(id):
    check_admin()
    add_role = False
    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role', 'success')
        return redirect(url_for('admin.list_roles'))
    form.name.data = role.name
    form.description.data = role.description
    return render_template('admin/roles/role.html', add_role=add_role,\
                           form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):

    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.', 'success')

    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")

@admin.route('/employees')
@login_required
def list_employees():
    check_admin()
    employees = Employee.query.all()
    return render_template('admin/employees/employees.html',
                           employees=employees, title='Employees')

@admin.route('/employees/assign/<int:id>', methods=['POST', 'GET'])
@login_required
def assign_employee(id):
    check_admin()
    employee = Employee.query.get_or_404(id)
    if employee.is_admin:
        abort(403,description='admin is not assign able for role and departments')
    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department = form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash('You have successfully assigned a department and role.', 'success')
        return redirect(url_for('admin.list_employees'))

    return render_template('admin/employees/employee.html',
                           employee=employee, form=form,
                           title='Assign Employee')


@admin.route('/500')
def error():
    return abort(500)
