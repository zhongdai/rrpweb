from rrp import db, User, Request, Rule, Field


def main():
    # Create the first user
    u = User(salary_number='M043944',
             name='Zhong',
             email='zhong@abc.com',
             enabled_flag=1,
             role='Admin')

    u.password = '123456'
            
    try:
        db.session.delete(u)
    except:
        pass

    db.session.add(u)
    db.session.commit()
    print('Added User {}'.format(u.id))
    

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



