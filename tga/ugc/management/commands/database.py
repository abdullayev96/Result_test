import sqlite3
from datetime import datetime


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_user(self, chat_id):
        self.cur.execute("""insert into user(chat_id) values (?)""", (chat_id,))
        self.conn.commit()

    def update_user_data(self, chat_id, key, value):
        self.cur.execute(f"""update user set {key} = ? where chat_id = ?""", (value, chat_id))
        self.conn.commit()

    def create_comment(self,user_id,username,comment):
        self.cur.execute("""insert into comment(user_id, comment_text, username) values (?, ?, ?)""",
                         (user_id,comment,username))
        self.conn.commit()

############################# test id_number

    # def create_test(self, user_id, username, id_number):
    #     self.cur.execute("""insert into ugc_user_test(user_id, id_number, username) values (?, ?, ?)""",
    #                      (user_id, id_number, username))
    #     self.conn.commit()

################   test id_number

    def get_user_by_chat_id(self, chat_id):
        self.cur.execute("""select * from user where chat_id = ?""", (chat_id, ))
        user = dict_fetchone(self.cur)
        return user

################
    # def get_user_by_id_number(self, id_number):
    #
    #
    #     try:
    #         self.cur.execute("""select * from ugc_test_result where id_number = ?""", (id_number,))
    #
    #     except Exception as e:
    #         print("E: ", e)
    #     user = dict_fetchone(self.cur)
    #
    #     return user
    def get_user_by_id_number(self, id_number=None):

        try:
            self.cur.execute("""select * from ugc_test_result where id_number = ?""", (id_number, ))
        except:
            self.cur.execute("""select * from ugc_test_result where id_number is NULL""")

        user = dict_fetchone(self.cur)
        return user




#################

###########GET ALL USERS#########
    def get_all_users(self):
        self.cur.execute("""select * from user""")
        user = dict_fetchall(self.cur)
        return user


############################# id_number
    def get_all_number(self):
        self.cur.execute("""select * from ugc_test_result""")
        user = dict_fetchall(self.cur)
        return user

#################


    def get_categories_by_parent(self, parent_id=None):
        if parent_id:
            self.cur.execute("""select * from category where parent_id = ?""", (parent_id, ))
        else:
            self.cur.execute("""select * from category where parent_id is NULL""")

        categories = dict_fetchall(self.cur)
        return categories

    def get_category_parent(self, category_id):
        self.cur.execute("""select parent_id from category where id = ?""", (category_id, ))
        category = dict_fetchone(self.cur)
        return category

    def get_products_by_category(self, category_id):
        self.cur.execute("""select * from product where category_id = ?""", (category_id, ))
        products = dict_fetchall(self.cur)
        return products

    def get_product_by_id(self, product_id):
        self.cur.execute("""select * from product where id = ?""", (product_id, ))
        product = dict_fetchone(self.cur)
        return product

    def get_about_us(self):
        self.cur.execute("""select * from about_us""")
        about_us = dict_fetchall(self.cur)
        return about_us

    def get_product_for_cart(self, product_id):
        self.cur.execute(
            """select product.*, category.name_uz as cat_name_uz, category.name_ru as cat_name_ru, category.name_en as cat_name_en 
            from product inner join category on product.category_id = category.id where product.id = ?""",
            (product_id, )
        )
        product = dict_fetchone(self.cur)
        return product

    def create_order(self, user_id, products, payment_type, location):
        self.cur.execute(
            """insert into "order"(user_id, status, payment_type, longitude, latitude, created_at) values (?, ?, ?, ?, ?, ?)""",
            (user_id, 1, payment_type, location.longitude, location.latitude, datetime.now())
        )
        self.conn.commit()
        self.cur.execute(
            """select max(id) as last_order from "order" where user_id = ?""", (user_id, )
        )
        last_order = dict_fetchone(self.cur)['last_order']
        for key, val in products.items():
            self.cur.execute(
                """insert into "order_product"(product_id, order_id, amount, created_at) values (?, ?, ?, ?)""",
                (int(key), last_order,  int(val), datetime.now())
            )
        self.conn.commit()

    def get_user_orders(self, user_id):
        self.cur.execute(
            """select * from "order" where user_id = ? and status = 1""", (user_id, )
        )
        orders = dict_fetchall(self.cur)
        return orders

    def get_order_products(self, order_id):
        self.cur.execute(
            """select order_product.*, product.name_uz as product_name_uz, product.name_ru as product_name_ru,product.name_en as product_name_en, 
            product.price as product_price from order_product inner join product on order_product.product_id = product.id
            where order_id = ?""", (order_id, ))
        products = dict_fetchall(self.cur)
        return products

    def get_news(self):
        self.cur.execute(
            """select * from 'ugc_new'"""
        )
        news=dict_fetchall(self.cur)
        return news


    ###################### test resultes #####################

    def get_test_result(self):
        self.cur.execute(
            """select * from 'ugc_test_result'"""
        )
        test=dict_fetchall(self.cur)
        return test



################################   end code #####################3

def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
