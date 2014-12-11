from module import XMPPModule
import halutils
import pyfatafl

class Game():
	self.players = []
	self.xmpp = None
	self.b = None
	self.turn = ""
	self.mod = None

	def __init__(self, mod, p1, p2):
		self.players = [p1, p2]
		self.mod = mod
		self.xmpp = mod.xmpp
		self.xmpp.sendMsg(p2, "You have been challenged to play Hnefatafl by {}, reply with '!hnefatafl accept' to begin!".format(p1))

	def begin():
		# Send initial board state
		self.b = hnefatafl.Board()
		self.turn = False # For now, make the challenger be first
		self._sendBoard()

	def _sendBoard(self)
		for i in players:
			self.xmpp.sendMsg(i, self.b.getPtBoard() + "\n\n" + "It is '{}''s ({}) turn".format(self.players[self.turn]), "white" if self.turn else "black")
		
	def msg(player, string):
		if player != self.players[self.turn]:
			self.xmpp.sendMsg(player, "Sorry, it is not your turn!")
		m = hnefatafl.Move()
		string = "{} {}".format("w" if self.turn else "b", string)
		try:
			m.parse(string, self.b)
		except:
			self.xmpp.sendMsg(player, "Invalid move format, see !help hnefatafl")

		try:
			self.b.move(m)
			self._sendBoard()
		except Exception as e: # TODO: Have been errors
			self.xmpp.sendMsg(player, str(e))
		if self.over:
			for i in self.players:
				self.xmpp.sendMsg(i, "Game over! {} wins!".format(self.b.over))
				del self.mod.sessions[i]
		


# Commented to avoid loading before its ready
class Hnefatafl(XMPPModule):
	sessions = {}

	def recvMsg(self, msg):
		cmd, args = halutils.splitArgList(msg)
		if cmd == "!hnefatafl":
			if args[0] == "challenge":
				if len(args) != 2:
					self.xmpp.reply(msg, "Need to the JID of a target")
					return
				elif arg[1] == msg['body'].bare:
				
					self.xmpp.reply(msg, "You can't challenge yourself...")
				# TODO: Validate JID here
				g = Game(self, msg['from'].bare, args[1])
				self.sessions[msg['from']].bare = g
				self.sessions[args[1]] = g
				self.xmpp.reply(msg, "Challenge sent!")
			elif args[0] == "accept":
				if msg['from'].bare not in self.sessions:
					self.xmpp.reply(msg, "You have not been challenged!")
					return
				self.sessions[msg['from'].bare].begin()

			elif args[0] == "surrender":
				if msg['from'].bare not in self.sessions:
					self.xmpp.reply(msg, "You aren't currently in a session")
					return
				for p in [p for p in self.sessions[msg['from'].bare].players]:
					del self.sessions[p]

		elif msg['from'].bare in sessions:
			self.sessions[msg['from'].bare].msg(msg['from'].bare, msg['body'])

	def help(self, string):
		if string in ["!hnefatafl", "hnefatafl"]:
			return '''
usage: !hnefatafl <command> [arg]

Commands:
  challenge <jid> - Send a challenge to JID
  accept         - Accept a challenge from JID, and begin game
  surrender      - Surrender the game
'''

		return '''
Hnefatafl by XMPP! Play a game against someone through this bot.
 Features:
   !hnefatafl - Command to challenge, accept, and surrender games

Note: This module will ignore any MUC messages, or other indirect messages
Another Note: This will likely be unplayable if not using a monospace font :)
'''
