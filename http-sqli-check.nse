description = [[
Kiểm tra SQL Injection đơn giản bằng cách gửi payload và phân tích phản hồi. 
]]

author = "tran + Copilot"
license = "Same as Nmap"
categories = {"vuln", "intrusive"}

portrule = shortport.http

action = function(host, port)
  local path = "/login.php?user=admin'--"
  local response = http.get(host, port, path)

  if response.status and response.body then
    if response.body:match("SQL syntax") or response.body:match("mysql_fetch") then
      return "⚠️ Có thể tồn tại lỗ hổng SQL Injection tại " .. path
    else
      return "✅ Không phát hiện lỗi SQL rõ ràng." [cite: 3]
    end
  end
  return "❌ Không nhận được phản hồi hợp lệ." [cite: 3]
end