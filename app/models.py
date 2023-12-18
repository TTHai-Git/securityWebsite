from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Date, DateTime, Time

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Date, DateTime

from sqlalchemy.orm import relationship
from app import db, app
from flask_login import UserMixin
import enum
from app.templates import cypher


class UserRoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2

class ClassNameEnum(enum.Enum):
    KTVTKW = "Kỹ thuật viên thiết kế Website",
    TKW = "Thiết kế Website",
    TKGDW = "Thiết kế giao diện Website",
    AMD = "App Mobile Design",
    CVTKDHVW = "Chuyên viên thiết kế đồ họa & Website",
    LTA = "Lập trình Android",
    LTI = "Lập trình IOS",
    RN = "React Native",
    UDCNTTCB = "Ứng dụng CNTT cơ bản",
    UDCNTTNC = " Ứng dụng CNTT nâng cao",
    LTNCC = 'Luyện thi nhận chứng chỉ'
    MOS_W = " MOS WORD",
    MOS_E = "MOS EXCEL",
    MOS_P = "MOS POWERPOINT",
    NMQTMVANM = "Nhập môn quản trị mạng và An ninh mạng",
    QTHTM = 'Quản trị hệ thống mạng',
    ANM = "An ninh mạng",


class CourseType(enum.Enum):
    WebDesign = "Thiết kế web",
    MobileDevelopment = "Lập trình di động",
    OfficeAutomation = 'Tin học văn phòng',
    MOSOfficeAutomation = 'Tin học văn phòng (MOS)',
    ComputerNetworking = 'Mạng máy tính'


class RoleEnum(enum.Enum):
    Teacher = "teacher",
    Student = "student",
    Staff = "staff",


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(255), default='https://genshin-guide.com/wp-content/uploads/yae-miko.png')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    role = Column(Enum(RoleEnum), nullable=False)
    ho_ten = Column(String(50), nullable=False)
    ngay_sinh = Column(Date, nullable=False, default=datetime.now())
    dia_chi = Column(String(100))
    email = Column(String(100), unique=True)
    phone = Column(String(10))

    def __str__(self):
        return self.ho_ten


class Course(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    classname = Column(Enum(ClassNameEnum), nullable=False)
    starttime = Column(Time, nullable=False)
    endtime = Column(Time, nullable=False)
    startdate = Column(Date, nullable=False)
    address = Column(String(100), nullable=False)
    type = Column(Enum(CourseType), nullable=False)
    price = Column(Float, nullable=False)


class Register(db.Model):
    __tablename__ = 'register'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    course_id = Column(Integer, ForeignKey(Course.id))
    registertime = Column(DateTime, nullable=False, default=datetime.now())
    quantity = Column(Integer, nullable=False)


if __name__ == '__main__':
    with app.app_context():
        #Xóa các bảng đã tạo
        db.drop_all()

        # Tạo các bảng mới
        db.create_all()

        # Tạo User
        u1 = User(name='Admin', username='admin', ho_ten='Text', ngay_sinh=datetime.now(), phone='1234567890',
                 password=cypher.affine_encrypt('123456', 22, 11),
                 user_role=UserRoleEnum.ADMIN, role=RoleEnum.Staff)
        u2 = User(name='User1', username='user1', ho_ten='Text', ngay_sinh=datetime.now(), phone='0123456789',
                  password=cypher.affine_encrypt('abcdef', 22, 11),
                  user_role=UserRoleEnum.USER, role=RoleEnum.Staff)
        db.session.add_all([u1, u2])

        # #Tạo Học viên
        # hv1 = HocVien(ho_ten='Nguyen Van A', ngay_sinh='2003-12-1', dia_chi='Duong X, tinh X', email='nva@gmail.com')
        # hv2 = HocVien(ho_ten='Nguyen Van B', ngay_sinh='2002-11-20', dia_chi='Duong A, tinh A', email='nvb@gmail.com')
        # hv3 = HocVien(ho_ten='Nguyen Van C', ngay_sinh='2000-1-1', dia_chi='Duong B, tinh B', email='nvc@gmail.com')
        # hv4 = HocVien(ho_ten='Nguyen Van D', ngay_sinh='2005-5-5', dia_chi='Duong C, tinh c', email='nvd@gmail.com')
        # hv5 = HocVien(ho_ten='Nguyen Van E', ngay_sinh='2001-2-28', dia_chi='Duong D, tinh D', email='nve@gmail.com')
        # db.session.add_all([hv1, hv2, hv3, hv4, hv5])
        #
        # #Tạo Khóa học
        # kh1 = KhoaHoc(ten_khoa_hoc='Lap trinh Android')
        # kh2 = KhoaHoc(ten_khoa_hoc='Lap trinh iOS')
        # kh3 = KhoaHoc(ten_khoa_hoc='Quan tri ha tang mang')
        # kh4 = KhoaHoc(ten_khoa_hoc='Quan tri he thong mang')
        # db.session.add_all([kh1, kh2, kh3, kh4])
        #
        # #Tạo Đăng ký khóa học
        # dk1 = DangKy(hoc_vien_id=1, khoa_hoc_id=2)
        # dk2 = DangKy(hoc_vien_id=2, khoa_hoc_id=2)
        # dk3 = DangKy(hoc_vien_id=3, khoa_hoc_id=2)
        # dk4 = DangKy(hoc_vien_id=4, khoa_hoc_id=4)
        # dk5 = DangKy(hoc_vien_id=5, khoa_hoc_id=3)
        # db.session.add_all([dk1, dk2, dk3, dk4, dk5])
        #
        # #Tạo Giáo viên
        # gv1 = GiaoVien(ten_giao_vien='Trinh Thanh Hai')
        # gv2 = GiaoVien(ten_giao_vien='Tran Minh Bao Long')
        # gv3 = GiaoVien(ten_giao_vien='Phan Hoang Trieu')
        # gv4 = GiaoVien(ten_giao_vien='Nguyen Minh Sang')
        # gv5 = GiaoVien(ten_giao_vien='Ho Phan Tan Khoa')
        # db.session.add_all([gv1, gv2, gv3, gv4, gv5])
        #
        # #Tạo Lớp học
        # lh1 = LopHoc(giao_vien_id=5, thoi_gian='2023-12-20 07:00:00', phong_hoc='A.XXX', khoa_hoc_id=1)
        # lh2 = LopHoc(giao_vien_id=4, thoi_gian='2023-12-21 07:00:00', phong_hoc='A.XXX', khoa_hoc_id=1)
        # lh3 = LopHoc(giao_vien_id=1, thoi_gian='2023-12-20 13:00:00', phong_hoc='A.XXX', khoa_hoc_id=2)
        # lh4 = LopHoc(giao_vien_id=3, thoi_gian='2023-12-30 18:00:00', phong_hoc='A.XXX', khoa_hoc_id=3)
        # db.session.add_all([lh1, lh2, lh3, lh4])
        #
        # #Tạo Quản lý học phí
        # hp1 = QuanLyHocPhi(hoc_vien_id=1, khoa_hoc_id=2, hoc_phi=5000000)
        # hp2 = QuanLyHocPhi(hoc_vien_id=2, khoa_hoc_id=2, hoc_phi=5000000)
        # hp3 = QuanLyHocPhi(hoc_vien_id=3, khoa_hoc_id=2, hoc_phi=5000000)
        # db.session.add_all([hp1, hp2, hp3])

        # # Tạo Điểm
        # diem1 = Diem(hoc_vien_id=1, lop_hoc_id=3, diems=10)
        # diem2 = Diem(hoc_vien_id=2, lop_hoc_id=3, diems=8)
        # diem3 = Diem(hoc_vien_id=3, lop_hoc_id=3, diems=5)
        # diem4 = Diem(hoc_vien_id=5, lop_hoc_id=4, diems=9)
        # db.session.add_all([diem1, diem2, diem3, diem4])

        # Đẩy dữ liệu lên mysql
        db.session.commit()
