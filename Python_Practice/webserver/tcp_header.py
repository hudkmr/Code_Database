#TCP Header
class tcp(object):
	def __init__(self,srcp,dstp):
		self.srcp = srcp
		self.dstp = dstp
		self.seqn = 0
		self.ackn = 0
		self.offset = 5
		self.reserved = 0
		self.urg = 0
		self.ack = 0
		self.psh = 1
		self.rst = 0
		self.syn = 0 
		self.fin = 0
		self.window = socket.htons(5840)
		self.checksum = 0
		self.urgp = 0
		self.payload = ""
	
	def pack(self, source, destination):
        data_offset = (self.offset << 4) + 0
        flags = self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh << 3) + (self.ack << 4) + (self.urg << 5)
        tcp_header = struct.pack('!HHLLBBHHH',
                     self.srcp,
                     self.dstp,
                     self.seqn,
                     self.ackn,
                     data_offset,
                     flags, 
                     self.window,
                     self.checksum,
                     self.urgp)
        #pseudo header fields
        source_ip = source
        destination_ip = destination
        reserved = 0
        protocol = socket.IPPROTO_TCP
        total_length = len(tcp_header) + len(self.payload)
        # Pseudo header
        psh = struct.pack("!4s4sBBH",
              source_ip,
              destination_ip,
              reserved,
              protocol,
              total_length)
        psh = psh + tcp_header + self.payload
        tcp_checksum = checksum(psh)
        tcp_header = struct.pack("!HHLLBBH",
                  self.srcp,
                  self.dstp,
                  self.seqn,
                  self.ackn,
                  data_offset,
                  flags,
                  self.window)
        tcp_header+= struct.pack('H', tcp_checksum) + struct.pack('!H', self.urgp)
        return tcp_header