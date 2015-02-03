__author__ = 'yestin'

import datetime

import hashlib

class Tag():
    table="tag"

    @classmethod
    def all(cls, db):
        return db.query("SELECT distinct tag_name FROM {0}".format(cls.table))

    @classmethod
    def count(cls, db):
        return db.query("SELECT count(distinct tag_name) FROM {0}".format(cls.table))

    @classmethod
    def get_post_tag(cls, db, post_id):
        return db.query("SELECT tag_name from {0} WHERE post_id = %s".format(cls.table), int(post_id))

    @classmethod
    def _update_post_tags(cls, db, post_id , post_tags):
        cls.delete_post_tags(db, post_id)
        cls.add_post_tags(db, post_id, post_tags)

    @classmethod
    def update_post_tags(cls, db, post_id , post_tags):
        db._db.autocommit(False)
        cls._update_post_tags(db,post_id,post_tags)
        db._db.commit()
        db._db.autocommit(True)

    @classmethod
    def delete_post_tags(cls, db, post_id):
        db.execute("DELETE from {0} WHERE post_id = %s ".format(cls.table), int(post_id))

    @classmethod
    def add_post_tags(cls, db, post_id , post_tags):
        seq = []
        for tag in post_tags:
            seq.append([post_id,tag])
        db.insertmany("INSERT INTO {0} (post_id, tag_name) VALUES (%s , %s)".format(cls.table), seq)

class Category():
    table="category"

    @classmethod
    def all(cls, db):
        return db.query("SELECT distinct category_name FROM {0}".format(cls.table))

    @classmethod
    def count(cls, db):
        return db.query("SELECT count(distinct category_name) FROM {0}".format(cls.table))

    @classmethod
    def get_post_category(cls, db, post_id):
        return db.query("SELECT category_name from {0} WHERE post_id = %s".format(cls.table), int(post_id))

    @classmethod
    def _update_post_categories(cls, db, post_id , post_categories):
        cls.delete_post_categories(db, post_id)
        cls.add_post_categories(db, post_id, post_categories)

    @classmethod
    def update_post_categories(cls, db, post_id , post_categories):
        db._db.autocommit(False)
        cls._update_post_categories(db, post_id, post_categories)
        db._db.commit()
        db._db.autocommit(True)

    @classmethod
    def delete_post_categories(cls, db, post_id):
        db.execute("DELETE from {0} WHERE post_id = %s ".format(cls.table), int(post_id))

    @classmethod
    def add_post_categories(cls, db, post_id , post_categories):
        seq = []
        for tag in post_categories:
            seq.append([post_id,tag])
        db.insertmany("INSERT INTO {0} (post_id, category_name) VALUES (%s , %s)".format(cls.table), seq)


class Post():

    table = "post"

    @classmethod
    def all(cls,db):
        return db.query("SELECT * FROM {0}".format(cls.table))

    @classmethod
    def get(cls, db, id):
        return db.get("SELECT * FROM {0} WHERE id = %s limit 1".format(cls.table), id)

    @classmethod
    def update(cls, db, id, title,  markdown, html,  categories, tags):
        db._db.autocommit(False)
        now = datetime.datetime.now()
        now_str =  now.strftime('%Y-%m-%d %H:%M:%S')
        db.update("UPDATE {0} set title = %s , markdown = %s, html = %s , edit_time = %s where id=%s"
                  .format(cls.table), title, markdown, html, now_str, id)
        Tag._update_post_tags(db, id, tags)
        Category._update_post_categories(db, id, categories)
        db._db.commit()
        db._db.autocommit(True)

    @classmethod
    def add(cls, db , title, markdown , html, categories, tags):
        db._db.autocommit(False)
        now = datetime.datetime.now()
        now_str =  now.strftime('%Y-%m-%d %H:%M:%S')
        post_id = db.insert("INSERT INTO {0} (title, markdown, html, add_time, edit_time) VALUES (%s,%s,%s,%s,%s)"
                  .format(cls.table), title, markdown, html, now_str, now_str)
        Tag.add_post_tags(db, post_id, tags)
        Category.add_post_categories(db, post_id, categories)
        db._db.commit()
        db._db.autocommit(True)

    @classmethod
    def delete(cls, db, id):
        db._db.autocommit(False)
        Tag.delete_post_tags(db,id)
        Category.delete_post_categories(db, id)
        db.execute("DELETE from {0} WHERE id = %s ".format(cls.table), int(id))
        db._db.commit()
        db._db.autocommit(True)

class User():
    table = "user"

    @classmethod
    def add(cls, db, name, pwd):
        db.insert("INSERT into {0} (name, password) VALUES (%s, %s)".format(cls.table)
                  , name, hashlib.md5(pwd).hexdigest())

    @classmethod
    def delete(cls, db, name):
        db.execute("DELETE FROM {0} where name = %s".format(cls.table), name)

    @classmethod
    def change_password(cls, db, name, pwd):
        db.execute("UPDATE {0} set password = %s where name = %s".format(cls.table),
                   hashlib.md5(pwd).hexdigest(), name)

    @classmethod
    def get(cls, db, name):
        return db.get("SELECT * from {0} where name = %s "
               .format(cls.table), name)

    @classmethod
    def get(cls, db, name, pwd):
        return db.get("SELECT * from {0} where name = %s and password = %s"
               .format(cls.table), name, hashlib.md5(pwd).hexdigest())

    @classmethod
    def check_password(cls, db, name, pwd):
        return not db.get("SELECT * from {0} where name = %s and password = %s"
               .format(cls.table), name, hashlib.md5(pwd).hexdigest()) is None


if __name__ == "__main__":
    import torndb
    from config import config

    db = torndb.Connection(
                host=config['db_host'], database=config['db_database'],
                user=config['db_user'], password=config['db_pass'], max_idle_time=config['db_idle_time'])

    #Post.add(db, "test","test","test")
    post = Post.all(db)
    for item in post:
        print item.title

    #Tag.add_post_tags(db, '1', ['t1','t2'])
    #Tag.update_post_tags(db, '1', ['t3','t2'])

    #Post.delete(db, 1)
    #User.delete(db, 'test')
    #User.add(db, 'test','test')
    #print User.check_password(db, 'test', 'test')
    #print User.check_password(db, 'test', 'tes2')


