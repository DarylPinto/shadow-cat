import requests
import time

endpoints = {
	"auth": "https://api.gfycat.com/v1/oauth/token",
	"upload": "https://api.gfycat.com/v1/gfycats",
	"file_drop": "https://filedrop.gfycat.com",
	"status": "https://api.gfycat.com/v1/gfycats/fetch/status"
}

class Client:

	def __init__(self, client_id=None, client_secret=None, username=None, password=None):
		self.client_id = client_id
		self.client_secret = client_secret
		self.username = username
		self.password = password
		self.access_token = None

		if client_id and client_secret and username and password:
			auth = {
				"grant_type": "password",
				"client_id": self.client_id,
				"client_secret": self.client_secret,
				"username": self.username,
				"password": self.password
			}
			r = requests.post(endpoints['auth'], json=auth)
			self.access_token = r.json()['access_token']

	def upload(self, file_path, anonymous=True):

		header = {'Content-Type': 'application/json'}

		if(not anonymous):
			header.update({'Authorization': self.access_token})

		r = requests.post(endpoints['upload'], headers=header, json={})
		key = r.json()['gfyname']

		r = requests.post(endpoints['file_drop'], files={'file': open(file_path,'rb')}, data={'key':key})

		time.sleep(5)
		
		status = self.check_status(key)
		while status["task"].lower() == "encoding":
			time.sleep(2)
			status = self.check_status(key)

		if status["task"] == "complete":
			return "https://gfycat.com/" + key
		else:
			return "An error occurred while uploading."


	def check_status(self, gfyname):
		status_url = endpoints['status'] + "/" + gfyname
		r = requests.get(status_url)
		return r.json()
