description = [[
Kiểm tra xem máy chủ FTP có cho phép đăng nhập anonymous hay không. 
]]

author = "tran + Copilot"
license = "Same as Nmap"
categories = {"auth", "safe"}

portrule = function(host, port)
  return port.number == 21 and port.protocol == "tcp" and port.state == "open"
end

action = function(host, port)
  local socket = nmap.new_socket()
  socket:connect(host.ip, port.number)
  socket:send("USER anonymous\r\n")
  local response = socket:receive_lines(1)
  socket:send("PASS test@example.com\r\n")
  local response2 = socket:receive_lines(1)
  socket:close()

  if response2 and response2:match("230") then
    return "✅ FTP anonymous login được phép!"
  else
    return "❌ Không cho phép đăng nhập anonymous." [cite: 6]
  end
end