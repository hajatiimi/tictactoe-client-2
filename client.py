import socket
from game import Game

PORT = 8282
        
def connect(host, port):
  client_socket = socket.socket()
  client_socket.connect((host, port))
  return client_socket

class Client():
  def __init__(self):
    self.socket = connect("localhost", PORT)
    self.message_log = []
    self.own_id = ""

  def send(self, message):
    msg = message + "\n"
    print("Sending message {}".format(msg))
    self.message_log.append("-> " + msg)
    self.socket.send(msg.encode())

  def receive(self):
    response = self.socket.recv(1024).decode()
    print("Received message {}".format(response))
    self.message_log.append("<- " + response)
    response = response.split()
    return response

  def start_game(self):
    self.send("GAME-JOIN")
    self.loop()

  def end_game(self, response):
    self.game_on = False
    self.send("GAME-WON ACK")
    print("----------")
    print("GAME OVER!")
    print("----------")

    if starter_id == self.own_id:
      print("\nYou won!")
    else:
      print("\nYou lose!")

    self.print_messages

  def join_successful(self, id): 
    self.own_id = id

    print("Player id: ", id)
    print("Waiting for game to start...")

  def game_ready(self, rows, cols, starter_id):
    print("Game ready!")

    self.game = game(rows, cols)
    self.send("GAME-READY-ACK")

    if starter_id == self.own_id:
      self.first_turn()

  def first_turn(self):
    next_turn_number, row, column = self.game.first_action()
    self.send("TURN {} {} {}".format(srt(next_turn_number).zfill(3), row, column))

  def turn(self, current_turn_number, row, column):
    next_turn_number = int(current_turn_number) + 1
    self.send("TURN-ACK {}".format(current_turn_number))
    self.game.opponent_action(row, column)

    next_turn_number, row, column = self.game.take_action(next_turn_number)
    self.send("TURN {} {} {}".format(str(next_turn_number).zfill(3), row, column))

  def print_messages(self):
    print("\n\nMessages:\n\n")
    [print(x) for x in self.message_log]

  def loop(self):
    self.game_on = True
    
    print("Starting game loop")

    while self.game_on:
      response = self.receive()
      if response:
        game_on = {
          "GAME-JOIN-ACK": lambda r: self.join_successful(r[1]),
          "GAME-READY": lambda r: self.game_ready(r[1], r[2], r[3]),
          "TURN-ACK": lambda r: self.turn(r),
          "GAME-WON": lambda r: self.end_game(r),
        }[response[0]](response)

    print("Game loop ended")

if __name__ == '__main__':
    client = Client()
    client.start_game()