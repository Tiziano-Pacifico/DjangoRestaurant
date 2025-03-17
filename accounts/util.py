def detectUser(user):
    if user.role == 1:
        redicrectUrl = 'vendorDashboard'
        return redicrectUrl
    elif user.role == 2:
        redicrectUrl = 'custDashboard'
        return redicrectUrl
    elif user.role == None:
        redicrectUrl = '/admin'
        return redicrectUrl
    