from datetime import datetime

from flask import session
from flask_login import login_user, current_user

from app.models import User, Course, Register
from app import app, db
from app.templates import cypher


# def load_categories():
#     return Category.query.all()
#     # return [{
#     #     'id': 1,
#     #     'name': 'Canon'
#     # }, {
#     #     'id': 2,
#     #     'name': 'Nikon'
#     # }, {
#     #     'id': 3,
#     #     'name': 'Sony'
#     # }]
#
#
# def load_products(kw=None, cate_id=None, page=None):
#     pros = Product.query
#
#     if kw:
#         pros = pros.filter(Product.name.contains(kw))
#
#     if cate_id:
#         pros = pros.filter(Product.category_id.__eq__(cate_id))
#
#     if page:
#         page = int(page)
#         page_size = app.config['PAGE_SIZE']
#         start = (page - 1)*page_size
#
#         return pros.slice(start, start + page_size)
#
#     return pros.all()
#     # pros = [{
#     #     'id': 1,
#     #     'name': 'Canon 750D',
#     #     'price': 7500000,
#     #     'image': 'https://product.hstatic.net/200000354621/product/may-anh-dslr-canon-eos-750d-ef-s18-55-is-stm_40450531012c4f6f89c50efc4fb684de_grande.jpg'
#     # }, {
#     #     'id': 2,
#     #     'name': 'Canon 750D',
#     #     'price': 7500000,
#     #     'image': 'https://product.hstatic.net/200000354621/product/may-anh-dslr-canon-eos-750d-ef-s18-55-is-stm_40450531012c4f6f89c50efc4fb684de_grande.jpg'
#     # }, {
#     #     'id': 3,
#     #     'name': 'Canon 750D',
#     #     'price': 7500000,
#     #     'image': 'https://product.hstatic.net/200000354621/product/may-anh-dslr-canon-eos-750d-ef-s18-55-is-stm_40450531012c4f6f89c50efc4fb684de_grande.jpg'
#     # }, {
#     #     'id': 4,
#     #     'name': 'Sony A6000',
#     #     'price': 10000000,
#     #     'image': 'https://binhminhdigital.com/storedata/images/product/sony-a6000-kit-1650-xam.jpg'
#     # }, {
#     #     'id': 5,
#     #     'name': 'Sony A6000',
#     #     'price': 10000000,
#     #     'image': 'https://binhminhdigital.com/storedata/images/product/sony-a6000-kit-1650-xam.jpg'
#     # }, {
#     #     'id': 6,
#     #     'name': 'Sony A6000',
#     #     'price': 10000000,
#     #     'image': 'https://binhminhdigital.com/storedata/images/product/sony-a6000-kit-1650-xam.jpg'
#     # }]
#     #
#     # if kw:
#     #     pros = [p for p in pros if p['name'].find(kw) >= 0]
#     #
#     # return pros
#
#
# def count_product():
#     return Product.query.count()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def authenticated_user(username, password):
    password = cypher.affine_encrypt(password, 22, 11)
    return User.query.filter(User.username.__eq__(username.strip()), User.password.__eq__(password.strip())).first()


def loadCourse():
    return Course.query.all()


def register_course():
    if 'course' in session:
        for c in session['course'].values():
            # Assuming c['id'] is the course ID
            course_id = c['id']

            # Create a Register instance for each course and user
            register_course = Register(
                user_id=current_user.id,
                course_id=course_id,
                registertime=datetime.now(),
                quantity=c['quantity']
            )
        db.session.add(register_course)
        db.session.commit()
        session.pop('course')

def clean_course(course_id):
    # Check if the 'course' key exists in the session
    if 'course' in session:
        course = session.get('course', {})
        # Check if the specified course ID exists in the session
        if course_id in course:
            # Remove the specified course ID from the session
            removed_course = course.pop(course_id)
            session['course'] = course
            return f'Course with ID {course_id} cleaned from session.'
        else:
            return f'Course with ID {course_id} not found in session.'
    else:
        return 'No course data in session.'
