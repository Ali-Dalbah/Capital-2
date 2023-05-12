from bot import run
import server
from threading import Thread
if __name__ == '__main__':
  server_thread = Thread(target=server.run)
  server_thread.start()
  run()
