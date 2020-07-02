class KWH_MySQL(object):
    def __init__(self):
        True

    def SELECT(self, sql):
        import MySQLdb
        from MySQLdb import Error

        try:
            db = MySQLdb.connect('localhost', 'pi', '', 'kwh')
            cursor = db.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()

        except MySQLdb.Error as error:
            return [1, error]

        cursor.close()
        db.close()

        return result

    def INSERT(self, sql):
        import MySQLdb
        from MySQLdb import Error

        try:
            db = MySQLdb.connect('localhost', 'pi', '', 'kwh')
            cursor = db.cursor()
            result = cursor.execute(sql)
            db.commit()
            cursor.close()
            db.close()

        except MySQLdb.Error as error:
            db.rollback()
            cursor.close()
            db.close()
            return [1, error]

        return [0]
