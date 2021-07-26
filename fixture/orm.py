
from pony.orm import *
from _datetime import datetime
from model.group import Group
from model.contact import Contact
from pymysql.converters import decoders

class ORMFixture:

    db = Database() # объект, на основании которого строится привязка (в виде наборов классов)

    class ORMGroup(db.Entity): # привязываем этот класс к БД ч/з db.Entity, т.е этот класс опис разл объекты, кот будут сохр в эту БД
        _table_ = 'group_list'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')



    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        name = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        deprecated = Optional(datetime, column='deprecated')


    # выше -структура таблиц
    # ниже - привязка к БД

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password)#, conv=decoders)  # это несмотря на то, что установлен pymysql
        self.db.generate_mapping()   # начинается сопоставление св-в описанных выше классов с таблицами и полями этих таблиц
        sql_debug(True)  # выводит реальный запрос на языке SQL который генерирует Pony ORM



## ниже - ф-ии, кот получают списки объектов

    def convert_groups_to_model(self, groups):
        def convert(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))



    def convert_contacts_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), name=contact.name, lastname=contact.lastname)

        return list(map(convert, contacts))




    @db_session   # для групп
    def get_group_list(self):
        return self.convert_groups_to_model(select (g for g in ORMFixture.ORMGroup))


    @db_session  # для групп
    def get_contact_list(self):
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))




















