from car_aquisition_roi import app

@property
def server():
  return app

if __name__ == '__main__':
  server().run_server(debug=False)
