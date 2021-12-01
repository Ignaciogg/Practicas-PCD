# @author: Ignacio Gil Garzón - 22041267

import socket
import threading
import sys
import pickle
import os

class Servidor():
	def __init__(self, host=socket.gethostname(), port = input("Escribe el puerto: ")):
		self.clientes = []
		self.mensajes = []
		print("IP: " + socket.gethostbyname(host))
		self.sock = socket.socket()
		self.sock.bind((str(host), int(port)))
		self.sock.listen(20)
		self.sock.setblocking(False)


		aceptar = threading.Thread(target=self.aceptarC)
		procesar = threading.Thread(target=self.procesarC)

		aceptar.daemon = True
		aceptar.start()

		procesar.daemon = True
		procesar.start()
		
		for thread in threading.enumerate():
			print("Hilo: " + thread.name + "\n" + "PID: "+ str(os.getpid()) +  "\n")
            
        # 3. Que el servidor, imprima y muestre la lista de usuarios (nicknames) conectados al mismo (en ese instante)
		print("Usuarios activos: " + str(threading.activeCount()))

		while True:
			msg = input('SALIR = Q\n')
			if msg == 'Q':

				print("* Hasta luego*")
				self.sock.close()
				sys.exit()
			else:
				pass


	def broadcast(self, msg, cliente):
		self.mensajes.append(pickle.loads(msg))
		print("Mensajes: " + str(pickle.loads(msg)))
		for c in self.clientes:
			try:
				if c != cliente:
					c.send(msg)
					 # 4.  Que el servidor almacene el historial de chat de todos los usuarios conectados durante la sesión
					archivo = open("u22041267.txt", "a")
					archivo.write(str(pickle.loads(msg)+"\n"))
					archivo.close()
			except:
				self.clientes.remove(c)

	def aceptarC(self):
		while True:
			try:
				conn, addr = self.sock.accept()
				print(f"\nConexion aceptada via {conn}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
				for client in self.clientes: 
					data = pickle.dumps(client.username + 'connected')
					self.broadcast(data,client) 
			except:
				pass

	def procesarC(self):
		
		while True:
			if len(self.clientes) > 0:
				for c in self.clientes:
					try:
						data = c.recv(32)
						if data:
							self.broadcast(data,c)
					except:
						pass
	

s = Servidor()