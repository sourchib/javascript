from flask import Flask, request, jsonify, make_response
import pymysql

# Membuat server flask
app = Flask(__name__)

mydb = pymysql.connect(
	host="localhost",
	user="root",
	passwd="",
	database="sekolah"
)

@app.route('/')
@app.route('/index')
def index():
	return "<h1>Belajar Python Flask</h1>"

@app.route('/get_data_siswa', methods=['GET'])
def get_data_siswa():
	query = "SELECT * FROM siswa WHERE 1=1"
	values = ()

	nis = request.args.get("nis")
	nama = request.args.get("nama")
	umur = request.args.get("umur")

	if nis:
		query += " AND nis=%s "
		values += (nis,)

	if nama:
		query += " AND nama LIKE %s "
		values += ("%"+nama+"%", )
	if umur:
		query += " AND umur=%s "
		values += (umur,)

	mycursor = mydb.cursor()
	mycursor.execute(query, values)
	data = mycursor.fetchall()

	row_headers = [x[0] for x in mycursor.description]
	json_data = []
	for result in data:
		json_data.append(dict(zip(row_headers, result)))

	return make_response(jsonify(json_data),200)

@app.route('/insert_data_siswa', methods=['POST'])
def insert_data_siswa():
	hasil = {"status": "gagal insert data siswa"}

	try:
		data = request.json

		nis = data["nis"]
		nama = data["nama"]
		umur = data["umur"]
		alamat = data["alamat"]

		query = "INSERT INTO siswa(nis, nama, umur, alamat) VALUES(%s,%s,%s,%s)"
		values = (nis, nama, umur, alamat, )

		mycursor = mydb.cursor()
		mycursor.execute(query, values)
		mydb.commit()
		hasil = {"status": "berhasil insert data siswa"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@app.route('/update_data_siswa', methods=['PUT'])
def update_data_siswa():
	hasil = {"status": "gagal update data siswa"}

	try:
		data = request.json
		nis_awal = data["nis_awal"]

		query = "UPDATE siswa SET nis = %s "
		values = (nis_awal, )

		if "nis_ubah" in data:
			query += ", nis = %s"
			values += (data["nis_ubah"], )
		if "nama" in data:
			query += ", nama = %s"
			values += (data["nama"], )
		if "umur" in data:
			query += ", umur = %s"
			values += (data["umur"], )
		if "alamat" in data:
			query += ", alamat = %s"
			values += (data["alamat"], )

		query += " WHERE nis = %s"
		values += (nis_awal, )

		mycursor = mydb.cursor()
		mycursor.execute(query, values)
		mydb.commit()
		hasil = {"status": "berhasil update data siswa"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@app.route('/delete_data_siswa/<nis>', methods=['DELETE'])
def delete_data_siswa(nis):
	hasil = {"status": "gagal hapus data siswa"}

	try:

		query = "DELETE FROM siswa WHERE nis=%s"
		values = (nis,)
		mycursor = mydb.cursor()
		mycursor.execute(query, values)
		mydb.commit()
		hasil = {"status": "berhasil hapus data siswa"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5010, debug=True)
