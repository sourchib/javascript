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

@app.route('/get_data_mahasiswa', methods=['GET'])
def get_data_mahasiswa():
	query = "SELECT * FROM mahasiswa WHERE 1=1"
	values = ()

	nis = request.args.get("nim")
	nama = request.args.get("nama")
	umur = request.args.get("umur")

	if nis:
		query += " AND nim=%s "
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

@app.route('/insert_data_mahasiswa', methods=['POST'])
def insert_data_mahasiswa():
	hasil = {"status": "gagal insert data mahasiswa"}

	try:
		data = request.json

		nis = data["nis"]
		nama = data["nama"]
		umur = data["umur"]
		alamat = data["alamat"]

		query = "INSERT INTO mahasiswa(nis, nama, umur, alamat) VALUES(%s,%s,%s,%s)"
		values = (nis, nama, umur, alamat, )

		mycursor = mydb.cursor()
		mycursor.execute(query, values)
		mydb.commit()
		hasil = {"status": "berhasil insert data mahasiswa"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@app.route('/update_data_mahasiswa', methods=['PUT'])
def update_data_mahasiswa():
	hasil = {"status": "gagal update data mahasiswa"}

	try:
		data = request.json
		nis_awal = data["nis_awal"]

		query = "UPDATE mahasiswa SET nis = %s "
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
		hasil = {"status": "berhasil update data mahasiswa"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

@app.route('/delete_data_mahasiswa/<nis>', methods=['DELETE'])
def delete_data_mahasiswa(nis):
	hasil = {"status": "gagal hapus data mahasiswa"}

	try:

		query = "DELETE FROM mahasiswa WHERE nis=%s"
		values = (nis,)
		mycursor = mydb.cursor()
		mycursor.execute(query, values)
		mydb.commit()
		hasil = {"status": "berhasil hapus data mahasiswa"}

	except Exception as e:
		print("Error: " + str(e))

	return jsonify(hasil)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5011, debug=True)
