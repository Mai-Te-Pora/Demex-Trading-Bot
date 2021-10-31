def cleaning_orderbooks(books):
    #Side, price and quantity holding variables for updating
    s = ''
    p = 0
    q = 0
    q = 0
    ls = []

    #Adjust quantities on update message
    for i, d in enumerate(books):
        if d['type'] == 'update':
            s = d['side']
            p = d['price']
            ls = books
            for y, z in enumerate(ls):
                if z['type'] == 'new':
                    if z['side'] == s:
                        if z['price'] == p:
                            z['quantity'] = float(z['quantity']) + float(q)
                            books = ls
                            
    #Register new messages with same price as delete message
    for i, d in enumerate(books):
        if d['type'] == 'delete':
            s = d['side']
            p = d['price']
            ls = books
            for y, z in enumerate(ls):
                if z['type'] == 'new':
                    if z['side'] == s:
                        if z['price'] == p:
                            z['type'] = 'delete'
                            books = ls

    books = list(filter(lambda i: i['type'] != 'delete', books))
    
    return books

def cleaning_orders(books):
    #Order Status = Pending, Cancelled
    #Turn all prices and quantity into floats for calculation
    for i in range(len(books)):
        if books[i]['quantity']:
            books[i]['quantity'] = float(books[i]['quantity'])
        if books[i]['available']:
            books[i]['available'] = float(books[i]['available'])
        if books[i]['filled']:
            books[i]['filled'] = float(books[i]['filled'])

    #Pending quantities showing after iteration...closing any negative quantity open orders for consistent book
    for i in range(len(books)):
        if books[i]['quantity'] < 0:
            del books[i]

    order_id = []
    #Document as order_id prior to deletion from list
    for i in range(len(books)):
        if books[i]['order_status'] == 'cancelled':
            order_id.append(books[i]['order_id'])
            #Delete cancelled orders
            del books[i]

    #Locate any active arders in the list with the same order_id and delete them
    for i in range(len(books)):
        try:
            if books[i]['order_status'] == 'pending':
                for num in order_id:
                    print("Number: " + num)
                    if books[i]['order_id'] == num:
                        del books[i]
        except:
            pass

    #Locate any active arders in the list with the same order_id and delete them
    for i in range(len(books)):
        try:
            if books[i]['order_status'] == 'new':
                for num in order_id:
                    print("Number: " + num)
                    if books[i]['order_id'] == num:
                        del books[i]
        except:
            pass

    #Locate any active arders in the list with the same order_id and delete them
    for i in range(len(books)):
        try:
            if books[i]['order_status'] == 'open':
                for num in order_id:
                    print("Number: " + num)
                    if books[i]['order_id'] == num:
                        del books[i]
        except:
            pass


    #Tracking/addressing filled orders
    order_id = []
    successful_orders = []
    #Document as order_id prior to deletion from list
    for i in range(len(books)):
        if books[i]['order_status'] == 'filled':
            order_id.append(books[i]['order_id'])
            successful_orders.append(books[i])
            #Delete filed orders from active orders
            del books[i]

    #Locate any active arders in the list with the same order_id and delete them
    for i in range(len(books)):
        if books[i]['order_status'] == 'pending':
            for num in order_id:
                if books[i]['order_id'] == num:
                    del books[i]

    #Note...successful_orders possesses successful orders list of dicts
    #Need to pass to another function for analytics
    return books
