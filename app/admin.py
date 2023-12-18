from flask import redirect
from flask_admin import BaseView, expose, Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from app import db, app
from app.models import UserRoleEnum, Course, User

admin = Admin(app=app, name='QUẢN LÝ WEBSITE TIN HỌC', template_mode='bootstrap4')


class AuthenticatedAdminMV(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class AuthenticatedAdminBV(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN


class StatsView(AuthenticatedAdminBV):
    @expose("/")
    def index(self):
        return self.render('admin/stats.html')


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class CalendarCourseView(AuthenticatedAdminMV):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ('id', 'classname', 'starttime', 'endtime', 'startdate', 'address', 'type', 'price')

    column_filters = ['classname', 'type', 'price']
    column_searchable_list = ['classname', 'type', 'price']

    column_labels = {
        'id': "Mã Khóa Học",
        'classname': "Tên Lớp Học",
        'starttime': "Giờ Học Bắt Đầu",
        'endtime': "Giờ Học Kết Thúc",
        'startdate': "Ngày Khai Giảng",
        'address': "Địa Chỉ",
        'type': "Tên Khóa Học",
        'price': "Giá",

    }


class UserView(AuthenticatedAdminMV):
    column_display_pk = True
    can_view_details = True
    can_export = True
    edit_modal = True
    details_modal = True
    create_modal = True
    column_list = ('id', 'username', 'password', 'user_role', 'role', 'ho_ten', 'ngay_sinh', 'dia_chi','email')

    column_filters = ['username', 'user_role', 'role', 'ho_ten']
    column_searchable_list =  ['username', 'user_role', 'role', 'ho_ten']

    column_labels = {
        'id': "STT",
        'username': "Tên Tài Khoản",
        'password': "Mật Khẩu",
        'user_role': "Vai Trò",
        'role': "Chức Vụ",
        'ho_ten': "Họ Và Tên",
        'ngay_sinh': "Ngày Sinh",
        'dia_chi': "Địa Chỉ",
        'email': "Email"
    }


admin.add_view(StatsView(name='Thống kê báo cáo'))
admin.add_view(LogoutView(name="Đăng xuất"))
admin.add_view(CalendarCourseView(Course, db.session, name="Quản Lý Lịch Học"))
admin.add_view(UserView(User, db.session, name="Quản Lý Người Dùng"))
