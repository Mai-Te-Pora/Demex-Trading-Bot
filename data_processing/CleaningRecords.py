def cleaning_orderbooks(books):
    #Turn all prices and quantity into floats for calculation
    for i in range(len(books)):
        if books[i]['price']:
            books[i]['price'] = float(books[i]['price'])
        if books[i]['quantity']:
            books[i]['quantity'] = float(books[i]['quantity'])
        if books[i]['type'] == "delete":
            s = books[i]['side']
            p = books[i]['price']
            del i

    #Side, price and quantity holding variables for deletion
    s = ''
    p = 0
    q = 0
    q = 0
    new_record = []
    #Document as much provided information (side and price) prior to deletion from list
    #Monitor for "id" or some other way to accurately delete existing order
    for i,e in enumerate(list(books)):
        if e['type'] == "delete":
            s = e['side']
            p = e['price']
            del books[books.index(e)]
            new_record = books
            for d, k in enumerate(list(new_record)):
                if  k['type'] == 'new':
                    if k['side'] == s:
                        if k['price'] == p:
                            del new_record[new_record.index(k)]
                            books = new_record
        elif e['type'] == "update":
            s = e['side']
            p = e['price']
            q = e['quantity']
            del books[books.index(e)]
            new_record = books
            for d, k in enumerate(list(new_record)):
                if  k['type'] == 'new':
                    if k['side'] == s:
                        if k['price'] == p:
                            k['quantity'] = k['quantity'] + float(q)
                            books = new_record
        print(books)
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
