from data import db_session
from data.applications import Applications
from data.rooms import Rooms
from data.statuses import Statuses
from data.floors import Floors

db_session.global_init('db/applications.db')
session = db_session.create_session()

s1 = Statuses(status='Новый запрос')
session.add(s1)
s2 = Statuses(status='В обработке')
session.add(s2)
s3 = Statuses(status='Завершено')
session.add(s3)

floor1 = Floors(floor='-1')
session.add(floor1)
floor2 = Floors(floor='1')
session.add(floor2)
floor3 = Floors(floor='2')
session.add(floor3)
floor4 = Floors(floor='3')
session.add(floor4)

r1 = Rooms(room='100', floor_id=1)
r2 = Rooms(room='101', floor_id=1)
r3 = Rooms(room='112', floor_id=1)
r4 = Rooms(room='123', floor_id=1)
r5 = Rooms(room='134', floor_id=1)
r6 = Rooms(room='145', floor_id=1)
r6 = Rooms(room='156', floor_id=1)
r7 = Rooms(room='167', floor_id=1)
r8 = Rooms(room='178', floor_id=1)
r9 = Rooms(room='190', floor_id=1)

r10 = Rooms(room='195', floor_id=1)
r11 = Rooms(room='202', floor_id=2)
r12 = Rooms(room='212', floor_id=2)
r13 = Rooms(room='232', floor_id=2)
r14 = Rooms(room='243', floor_id=2)
r15 = Rooms(room='254', floor_id=2)
r16 = Rooms(room='276', floor_id=2)
r17 = Rooms(room='287', floor_id=2)
r18 = Rooms(room='298', floor_id=2)
r19 = Rooms(room='231', floor_id=2)
r20 = Rooms(room='275', floor_id=2)

r21 = Rooms(room='300', floor_id=3)
r22 = Rooms(room='391', floor_id=3)
r23 = Rooms(room='382', floor_id=3)
r24 = Rooms(room='373', floor_id=3)
r25 = Rooms(room='364', floor_id=3)
r26 = Rooms(room='351', floor_id=3)
r27 = Rooms(room='398', floor_id=3)
r28 = Rooms(room='352', floor_id=3)
r29 = Rooms(room='371', floor_id=3)
r30 = Rooms(room='390', floor_id=3)

r31 = Rooms(room='442', floor_id=4)
r32 = Rooms(room='496', floor_id=4)
r33 = Rooms(room='417', floor_id=4)
r34 = Rooms(room='482', floor_id=4)
r35 = Rooms(room='465', floor_id=4)
r36 = Rooms(room='425', floor_id=4)
r37 = Rooms(room='409', floor_id=4)
r38 = Rooms(room='492', floor_id=4)
r39 = Rooms(room='431', floor_id=4)
r40 = Rooms(room='401', floor_id=4)

for i in range(1, 41):
    session.add(eval(f'r{i}'))


session.commit()