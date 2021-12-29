from flask import make_response, abort, request, jsonify
from db_connect import db_connect

conn = db_connect()

cursor = conn.cursor()


cursor.execute('CREATE TABLE IF NOT EXISTS user (id INT PRIMARY KEY AUTO_INCREMENT, username VARCHAR(50), password VARCHAR(20), email VARCHAR(50), phone VARCHAR(20), country VARCHAR(30), city VARCHAR(30), postcode VARCHAR(10), name VARCHAR(50), address VARCHAR(100), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)')

def post(user):
    body = user.get

    username = body('username')
    password = body('password')
    email = body('email')
    phone = body('phone')
    country = body('country')
    city = body('city')
    postcode = body('postcode')
    name = body('name')
    address = body('address')

    query_check = 'SELECT * FROM user where email = %s'
    cursor.execute(query_check, (email,))
    result = cursor.fetchone()

    if result is None:
        sql = 'INSERT INTO user(username, password, email, phone, country, city, postcode, name, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        val = (username,password,email,phone,country,city,postcode,name,address)
        cursor.execute(sql, val)
        
        conn.commit()

        data = {
            'username' : username,
            'email' : email,
            'phone' : phone,
            'country' : country,
            'city' : city,
            'postcode' : postcode,
            'name' : name,
            'address' : address
        }

        response = make_response(jsonify({
            'message' : 'Register Success',
            'data' : data
        }), 201)

        return response
    else:
        abort(409, f'User with email {email} already exists, please use another email')

def get_one(id):
    sql = 'SELECT * FROM user WHERE id = %s'
    cursor.execute(sql, (id,))
    myresult = cursor.fetchall()

    content = {}
    if len(myresult) != 0:
        for result in myresult:
            content = {
                'id' : result[0],
                'username' : result[1],
                'email' : result[3],
                'phone' : result[4],
                'country' : result[5],
                'city' : result[6],
                'postcode' : result[7],
                'name' : result[8],
                'address' : result[9]
            }
        response = make_response(jsonify({
            'message' : 'Retrieved data Success',
            'data' : content
        }))

        return response
    else:
        abort(404, f'Data with id {id} not found')

def get_all():
    sql = 'SELECT * FROM user'
    cursor.execute(sql)
    myresult = cursor.fetchall()

    payload = []
    content = {}
    
    if len(myresult) != 0:
        for result in myresult:
            content = {
                'id' : result[0],
                'username' : result[1],
                'email' : result[3],
                'phone' : result[4],
                'country' : result[5],
                'city' : result[6],
                'postcode' : result[7],
                'name' : result[8],
                'address' : result[9]
            }
            payload.append(content)
            content = {}
        response = make_response(jsonify({
            'message' : 'Retrieved all data Success',
            'data' : payload
        }))

        return response
    else:
        abort(404, f'Data not found')

def delete(id):
    sql = 'SELECT * FROM user WHERE id = %s'
    cursor.execute(sql, (id,))
    myresult = cursor.fetchall()

    if len(myresult) == 0:
        abort(404, f'Data with id {id} not found')
    
    query_delete = 'DELETE FROM user WHERE id = %s'
    cursor.execute(query_delete, (id,))

    conn.commit()
    
    response = make_response(jsonify({'message' : f'Data with id {id} successfully deleted'}), 201)
    
    return response

def update(id, user):
    sql = 'SELECT * FROM user WHERE id = %s'
    cursor.execute(sql, (id,))
    myresult = cursor.fetchall()
    if len(myresult) != 0:
        body = user.get
        for result in myresult:
            username = body('username', result[1])
            password = body('password', result[2])
            email = body('email', result[3])
            phone = body('phone', result[4])
            country = body('country', result[5])
            city = body('city', result[6])
            postcode = body('postcode', result[7])
            name = body('name', result[8])
            address = body('address', result[9])

        query_update = 'UPDATE user SET username= %s, password= %s, email= %s, phone= %s, country= %s, city= %s, postcode= %s, name= %s, address= %s WHERE id= %s'
        val = (username,password,email,phone,country,city,postcode,name,address,id,)
        cursor.execute(query_update, val)

        conn.commit()

        response = make_response(jsonify({'message' : f"Successfully modified data with id {id}"}), 201) 

        return response
    else:
        abort(404, f'Data with id {id} not found')