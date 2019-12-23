from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL
app = Flask(__name__)
#MySQL Connection
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''
mysql = MySQL(app)
# settings
app.secret_key = 'mysecretkey'
#Le pasamos un nombre para crear una url
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html',contacts=data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s,%s,%s)',(fullname,phone, email))
        mysql.connection.commit()
        flash('Contact Added Succesfully')
        return redirect(url_for('index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id, ))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s 
            WHERE id = %s
        """, (fullname,email,phone,id))
        print(fullname,phone,email)
        mysql.connection.commit()
        flash('Contact Updated Successfully')
        return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('index'))

@app.route('/search',methods=['POST'])
def search_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM contacts WHERE fullname LIKE '%{0}%'".format(fullname))
        data = cur.fetchall()
        print(data)
        return render_template("index.html",contacts=data)


if __name__ == '__main__':
    app.run(debug=True)
