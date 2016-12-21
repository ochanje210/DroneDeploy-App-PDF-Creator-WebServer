import os
import base64
import requests
import tornado.ioloop
import tornado.web

class getEncodedUrlHandler(tornado.web.RequestHandler):

	def set_default_headers(self):
		# allow cross-origin requests from the pdf creating app on DroneDeploy to the heroku server
		self.set_header("Access-Control-Allow-Origin", "https://www.dronedeploy.com")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		# allow POST method
		self.set_header("Access-Control-Allow-Methods", "POST, OPTIONS")

	def post(self):
		# decode the request body to JSON
		data = tornado.escape.json_decode(self.request.body)

		# list of tile image URLs will be pushed into the following list and sent to client
		encoded_tiles = []

		for tile in data['tile']:
			# get results from the given URL including tile image
			res = requests.get(tile)
			# encode the tile png into base64
			encoded = base64.b64encode(res.content)
			encoded_tiles.append(encoded)

		# send the results as JSON format back to the client
		self.write({'msg': encoded_tiles})

	def options(self):
		# no body
		self.set_status(204)
		self.finish()

def main():
    application = tornado.web.Application([
        (r"/getEncodedUrl/", getEncodedUrlHandler)
    ])
    port = int(os.environ.get("PORT", 5000))
    application.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()