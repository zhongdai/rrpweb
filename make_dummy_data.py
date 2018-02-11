from rrp import db, User, Request, Rule, Field


def main():
    # Create the first user
    u = User(salary_number='M043944',
             name='Zhong',
             password='123',
             email='zhong@abc.com',
             enabled_flag=1)

    try:
        db.session.delete(u)
    except:
        pass

    db.session.add(u)
    db.session.commit()
    print('Added User {}'.format(u.id))
    

    for i in range(20):
        req = Request(user_id=u.id, 
                     data_file_full_loc='Dummy full path for file {}'.format(str(i)),
                     comments = 'Dummy comments'
                     )
        try:
            db.session.delete(req)
        except:
            pass
        db.session.add(req)
        print('Added Request {}'.format(req.id))

    db.session.commit()
    print('Adding requests')


    for i in range(10):
        f = Field(field_name='Dummy Field #{}'.format(i))
        try:
            db.session.delete(f)
        except:
            pass
        db.session.add(f)
    db.session.commit()
    print('Adding fields')

    for i in range(10):
        r = Rule(name='Dummy Rule #{}'.format(i))
        try:
            db.session.delete(r)
        except:
            pass
        db.session.add(r)
    db.session.commit()
    print('Adding rules')

if __name__ == '__main__':
    main()


